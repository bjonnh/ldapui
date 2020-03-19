import ldap3
import ldap3.utils.hashed
import re

alnum_pattern = re.compile('[\W_]+', re.UNICODE)


def sha_password(value):
    return ldap3.utils.hashed.hashed(ldap3.utils.hashed.HASHED_SHA, value)


def alnum(string):
    return alnum_pattern.sub('', string)
