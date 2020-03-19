from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from app.auth.storage.ldap import manager_ldap


def is_admin(func):
    """Decorator that ensures the wrapper is running as an admin"""
    @wraps(func)
    def decorated_view(*args, **kwargs):

        if manager_ldap.is_admin(current_user.username) is False:
            flash('You are not allowed to do that.', 'info')
            return redirect(url_for('home.home'))

        return func(*args, **kwargs)

    return decorated_view

