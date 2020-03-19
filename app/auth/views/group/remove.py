from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.group import RemoveGroupForm
from app.auth.views.group import group_blueprint
from app.helpers.views import is_admin


@group_blueprint.route('/group/remove', methods=['GET', 'POST'])
@login_required
@is_admin
def remove():
    form = RemoveGroupForm()
    if request.method == 'GET':
        form.name.data = request.args.get('name')

    if request.method == 'POST' and form.validate():
        name = request.form.get('name')
        ret = manager_ldap.remove_group(name)
        if ret is not None:
            flash(
                'Group {} removed'.format(name),
                'danger')
            return redirect(url_for('home.home'))

    return render_template('group/remove.html', form=form)
