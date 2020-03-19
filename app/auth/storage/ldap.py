import ldap3
import ldap3.utils.conv
from app.helpers.ldap import alnum, sha_password
import os


class LdapWrap:
    _conn = None
    _manager_conn = None
    _server = None
    _username = None
    _password = None
    _dc = os.environ['DC']
    _ou = os.environ['OU']
    _manager_user = os.environ['MANAGER_USER']
    _manager_path = os.environ['MANAGER_PATH']
    _manager_pw = os.environ['MANAGER_PW']
    UID = 0
    GID = 1

    USER_OBJECTCLASS = ['inetOrgPerson', 'posixAccount', 'shadowAccount',
                        'person', 'organizationalPerson']
    GROUP_OBJECTCLASS = ['posixGroup']

    def __init__(self, user, password):
        self._server = ldap3.Server(os.environ['LDAP_HOST'], port=int(os.environ['LDAP_PORT']))
        self._username = user
        self._password = password

    def manager_conn(self, reset = False):
        if reset:
            self._manager_conn = None
        if self._manager_conn is None:
            self._manager_conn = ldap3.Connection(
                self._server,
                'cn={},{}'.format(self._manager_user,
                                  self._manager_path),
                self._manager_pw, auto_bind=True)

        return self._manager_conn

    @property
    def conn(self):
        if self._conn is None:
            self._conn = ldap3.Connection(self._server,
                                          'cn={},{}'.format(
                                              alnum(self._username), self._ou),
                                          self._password, auto_bind=True)
        return self._conn

    def test_connection(self):
        return self.conn

    def is_admin(self, username):
        data = self.search(self._ou,
                           "(&(objectClass=posixGroup)(cn=Administrators))")
        if len(data) == 0:
            return False
        if "memberUid" not in data[0]:
            return False
        return username in data[0]['memberUid']

    @property
    def groups(self):
        data = self.search(self._ou,
                           "(objectClass=posixGroup)")

        groups = []
        for group in data:
            gid_number = group['gidNumber'][0]
            cn = group['cn'][0]

            members = []
            if 'memberUid' in group:
                members = group['memberUid']

            description = ""
            if 'description' in group:
                description = group['description']

            groups.append({'gidNumber': gid_number, 'cn': cn, 'members': members, 'description': description})
        return groups

    @property
    def users(self):
        data = self.search(self._ou,
                           "(objectClass=posixAccount)")

        users = []

        for user in data:
            uid_number = user['uidNumber'][0]
            cn = user['cn'][0]
            display_name = user['displayName'][0]

            if "mail" in user:
                mail = user["mail"][0]
            else:
                mail = ""

            users.append({'uidNumber': uid_number,
                          'cn': cn,
                          'displayName': display_name,
                          'mail': mail})

        return users

    def add_user(self, username, password, mail, display_name, surname):

        # Ensure user doesn't already exist
        try:
            self.get_uid_by_cn(username)

            raise ValueError("User already exists")
        except ValueError:
            pass

        cn = 'cn={},{}'.format(alnum(username),
                               self._ou)

        param = {'homeDirectory': '/bin/false',
                 'uid': alnum(username),
                 'sn': surname,
                 'gidNumber': self._get_next_gid(),
                 'cn': self.safe_string(username),
                 'uidNumber': self._get_next_uid(),
                 'displayName': display_name,
                 'mail': mail,
                 'userPassword': sha_password(password)}

        res = self.add(
            cn,
            self.USER_OBJECTCLASS,
            param)

        return res

    def add_group(self, name, description, members=None):
        if members is None:
            members = []

        # Ensure user doesn't already exist
        try:
            self.get_gid_by_cn(name)

            raise ValueError("Group already exists")
        except ValueError:
            pass

        cn = 'cn={},{}'.format(alnum(name),
                               self._ou)

        param = {'cn': alnum(name),
                 'gidNumber': self._get_next_gid(),
                 'description': description}

        res = self.add(
            cn,
            self.GROUP_OBJECTCLASS,
            param)

        for member in members:
            res &= self.add_member_to_group(name, member)

        return res

    def remove_element(self, name):
        cn = "cn={},{}".format(alnum(name),
                               self._ou)

        res = self.delete(cn)
        return res

    def remove_user(self, name):
        """First, remove the user from all groups, then remove the user"""
        try:
            self.get_uid_by_cn(name)
        except ValueError:
            return False

        for group in self.groups:
            self.remove_member_from_group(group['cn'], name)

        return self.remove_element(name)

    def remove_group(self, name):
        try:
            self.get_gid_by_cn(name)
        except ValueError:
            return False

        return self.remove_element(name)

    def add_member_to_group(self, group_name, user_name):
        self.get_gid_by_cn(self.safe_string(group_name))
        self.get_uid_by_cn(self.safe_string(user_name))

        res = self.modify('cn={}, ou=Users,{}'.format(
            self.safe_string(
                group_name),
            self._dc),
                {'memberUid': [(ldap3.MODIFY_ADD,
                               [self.safe_string(user_name)])]})

        return res

    def remove_member_from_group(self, group_name, user_name):
        self.get_gid_by_cn(self.safe_string(group_name))
        self.get_uid_by_cn(self.safe_string(user_name))

        res = self.modify('cn={}, ou=Users,{}'.format(
            self.safe_string(
                group_name),
            self._dc),
                {'memberUid': [(ldap3.MODIFY_DELETE,
                               [self.safe_string(user_name)])]})

        return res

    def update_groups_of_user(self, username, groups):
        user_new_ldap_groups = set(groups)

        user_current_ldap_groups = set(self.groups_of_user(username))
        ret = True

        for group in list(user_current_ldap_groups-user_new_ldap_groups):
            ret &= self.remove_member_from_group(group, username)

        for group in list(user_new_ldap_groups-user_current_ldap_groups):
            ret &= self.add_member_to_group(group, username)

        return ret

    def update_users_of_group(self, name, _users):
        users = [self.safe_string(user) for user in _users]
        ret = self.modify('cn={},{}'.format(
            alnum(name),
            self._ou),
            {'memberUid': [(ldap3.MODIFY_REPLACE,
                            users)]})
        return ret

    def find_user_by_email(self, mail):
        data = self.search(
            self._ou,
            '(&(objectClass=posixAccount)(mail={}))'.format(mail))
        try:
            user = {'cn': data[0]['cn']}
            return user
        except IndexError:
            return False

    def groups_of_user(self, username):
        return [group['cn'] for group in self.groups if username in list(group['members'])]

    def users_of_group(self, name):
        data = self.search(self._ou,
                           "(&(objectClass=posixGroup)(cn={}))".format(self.safe_string(name)))
        if 'memberUid' in data[0]:
            return data[0]['memberUid']
        else:
            return []

    def name_exists(self, name):
        """Verifies that a name isn't already used for a user or a group"""
        try:
            self.get_uid_by_cn(name)
            res_user = True
        except ValueError:
            res_user = False

        try:
            self.get_gid_by_cn(name)
            res_group = True
        except ValueError:
            res_group = False

        return res_user or res_group

    def get_info_user(self, username):
        data = self.search(
            self._ou,
            '(&(objectClass=posixAccount)(cn={}))'.format(username))
        if len(data) == 0:
            return False
        if "mail" in data[0]:
            mail = data[0]["mail"]
        else:
            mail = ""
        return {'mail': mail,
                'display_name': data[0]['displayName'],
                'surname': data[0]['sn']}

    def get_info_group(self, username):
        data = self.search(
            self._ou,
            '(&(objectClass=posixGroup)(cn={}))'.format(username))
        members = []
        if 'memberUid' in data[0]:
            members = data[0]['memberUid']
        return {'description': data[0]['description'],
                'gid': data[0]['gidNumber'],
                'members': members,
                'cn': data[0]['cn']}

    def get_gid_by_cn(self, name):
        """Find the uid of a group named 'name', returns None if
        it doesn't exist"""
        try:
            return self.search(
                self._ou,
                '(&(objectClass=posixGroup)(cn={}))'.format(
                        name))[0]['gidNumber'].value
        except IndexError:
            raise ValueError("Group {} doesn't exist.".format(name))

    def get_uid_by_cn(self, username):
        """Find the uid of a user named 'name', returns None if
              it doesn't exist"""
        try:
            return self.search(
                self._ou,
                '(&(objectClass=posixAccount)(cn={}))'.format(
                        username))[0]['uidNumber'].value
        except IndexError:
            raise ValueError("User {} doesn't exist.".format(username))

    def add(self, base, query, param, retry=3):
        if retry==0:
            raise ValueError("Sorry impossible to connect to add")
        try:
            out = self.manager_conn().add(base, query, param)
        except ldap3.core.exceptions.LDAPSocketOpenError:
            # Reset the connection
            self.manager_conn(True)
            return self.add(base, query, param, retry-1)
        return out

    def modify(self, base, param, retry=3):
        if retry==0:
            raise ValueError("Sorry impossible to connect to modify")
        try:
            out = self.manager_conn().modify(base, param)
        except ldap3.core.exceptions.LDAPSocketOpenError:
            # Reset the connection
            self.manager_conn(True)
            return self.modify(base, param, retry-1)
        return out

    def delete(self, base, retry=3):
        if retry==0:
            raise ValueError("Sorry impossible to connect to delete")
        try:
            out = self.manager_conn().delete(base)
        except ldap3.core.exceptions.LDAPSocketOpenError:
            # Reset the connection
            self.manager_conn(True)
            return self.delete(base, retry-1)
        return out

    def search(self, base, query, retry=3):
        if retry==0:
            raise ValueError("Sorry impossible to connect to search")
        try:
            self.manager_conn().search(base, query, attributes=[
                ldap3.ALL_ATTRIBUTES,
                ldap3.ALL_OPERATIONAL_ATTRIBUTES])
        except ldap3.core.exceptions.LDAPSocketOpenError:
            # Reset the connection
            self.manager_conn(True)
            return self.search(base, query, retry-1)
        return self.manager_conn().entries

    def change_password(self, username, password):
        self.get_uid_by_cn(self.safe_string(username))

        res = self.modify('cn={},{}'.format(
            alnum(username),
            self._ou),
                {'userPassword': [(ldap3.MODIFY_REPLACE,
                                   [sha_password(password)])]})

        return res

    def change_entry(self, name, value, entry):
        res = self.modify('cn={},{}'.format(
            alnum(name),
            self._ou),
                {entry: [(ldap3.MODIFY_REPLACE,
                          [value])]})

        return res

    def update_user_mail(self, username, mail):
        return self.change_entry(username, mail, 'mail')

    def update_user_display_name(self, username, display_name):
        return self.change_entry(username, display_name, 'displayName')

    def update_user_surname(self, username, surname):
        return self.change_entry(username, surname, 'sn')

    def update_group_description(self, name, description):
        return self.change_entry(name, description, 'description')

    def _get_next_id(self, uid_type=None):
        """Generate the next id. Use LdapWrap.UID or LdapWrap.GID as 'uidType' to
        specify what you want"""
        if uid_type is None or uid_type == self.UID:
            uid_type = 'uidNumber'
        else:
            uid_type = 'gidNumber'

        # We modify the id first to be sure it isn't going to be stolen by
        # another process

        mod = {uid_type: [(ldap3.MODIFY_INCREMENT, 1)]}

        self.modify('cn=NextFreeUnixId,{}'.format(self._dc), mod)

        # Grabbing the current value
        val = self.search(self._dc, '(cn=NextFreeUnixId)')
        if len(val)==0:
            return 2000
        return val[0][uid_type].value - 1

    def _get_next_uid(self):
        """Get the next available UID"""
        return self._get_next_id(self.UID)

    def _get_next_gid(self):
        """Get the next available GID"""
        return self._get_next_id(self.GID)

    @staticmethod
    def safe_string(string):
        return ldap3.utils.conv.escape_filter_chars(string)

manager_ldap = LdapWrap("", "")
