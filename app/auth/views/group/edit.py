from flask import request, flash, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.group import EditGroupForm
from app.auth.views import ChoiceObj
from app.auth.views.group import group_blueprint
from app.helpers.views import is_admin



@group_blueprint.route('/group/edit', methods=['GET', 'POST'])
@login_required
@is_admin
def edit():
    failed = False
    if request.method == 'GET':
        name = request.args.get('name')
    elif request.method == 'POST':
        name = request.form.get('name')
    else:
        raise ValueError('Invalid')

    accounts = [account['cn'] for account in manager_ldap.users]
    selected_choices = ChoiceObj('members', manager_ldap.users_of_group(name))
    form = EditGroupForm(obj=selected_choices)
    form.members.choices = [(c, c) for c in accounts]

    if request.method == 'GET':
        form.name.data = request.args.get('name')
        data_group = manager_ldap.get_info_group(request.args.get('name'))
        form.description.data = data_group['description']
        failed = True

    if request.method == 'POST':
        if form.validate():
            name = request.form.get('name')
            description = request.form.get('description')

            ret = manager_ldap.update_users_of_group(name, form.members.data)

            if ret:
                flash(
                    'Group {} modified'.format(name),
                    'info')
                failed = False
            else:
                flash(
                    'Group {} cannot have its members updated'.format(name),
                    'urgent')
                failed = True
            if not failed:
                ret = manager_ldap.update_group_description(name, description)
                if ret:
                    failed = False

                else:
                    flash(
                        'Group {} cannot have its description updated'.format(name),
                        'urgent')
                    failed = True

    if failed:
        return render_template('group/edit.html', form=form, groupsselected=request.form.get('groups'))
    else:
        return redirect(url_for('home.home'))
