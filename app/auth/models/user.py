from app import db, LdapWrap
from app.auth.storage.ldap import manager_ldap
from app.helpers.ldap import alnum, sha_password


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))  # Passwords are stored as sha_passwords
    _conn = None
    _authenticated = True

    def __init__(self, username, password):
        self.username = alnum(username)
        self.password = sha_password(password)

    @staticmethod
    def try_login(_username, password):
        """Test if login is possible with those credentials, and store
        the connection in the store."""
        # We test if it is possible to connect
        conn = LdapWrap(_username, password)
        conn.test_connection()

    @property
    def is_admin(self):
        return manager_ldap.is_admin(self.username)

    @property
    def is_authenticated(self):
        return self._authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
