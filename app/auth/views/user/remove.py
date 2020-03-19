from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.user import RemoveUserForm
from app.auth.views.user import user_blueprint
from app.helpers.views import is_admin


@user_blueprint.route('/user/remove', methods=['GET', 'POST'])
@login_required
@is_admin
def remove():
    form = RemoveUserForm()
    if request.method == 'GET':
        form.username.data = request.args.get('username')

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        ret = manager_ldap.remove_user(username)
        if ret is not None:
            flash(
                'User {} removed'.format(username),
                'danger')
            return redirect(url_for('home.home'))

    return render_template('user/remove.html', form=form)
