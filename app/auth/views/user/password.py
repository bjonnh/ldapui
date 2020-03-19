from flask import request, redirect, url_for, flash
from flask_login import current_user, logout_user

from app.auth.storage.ldap import manager_ldap
from app.auth.views.user import user_blueprint


@user_blueprint.route('/user/pw', methods=['GET', 'POST'])
def password():
    if current_user is None and request.method == 'GET':
        return redirect(url_for('home.home'))
    username = current_user.username
    if request.method == 'POST':
        pw = request.form.get('password')
        pw2 = request.form.get('password2')
        if pw != pw2:
            flash('Your passwords are not the same', 'warning')
            return redirect(url_for('home.home'))

        if pw == '':
            flash('Your new password cannot be empty', 'danger')
            return redirect(url_for('home.home'))

        ret = manager_ldap.change_password(username, pw)
        if ret:
            flash('You have a new password set, please login again', 'info')
            logout_user()
        else:
            flash('Failure to change your password', 'danger')
    return redirect(url_for('home.home'))
