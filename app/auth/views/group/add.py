from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.group import AddGroupForm
from app.auth.views import ChoiceObj
from app.auth.views.group import group_blueprint
from app.helpers.views import is_admin


@group_blueprint.route('/group/add', methods=['GET', 'POST'])
@login_required
@is_admin
def add():
    accounts = [account['cn'] for account in manager_ldap.users]
    selected_choices = ChoiceObj('members', request.form.get('members'))
    form = AddGroupForm(obj=selected_choices)
    form.members.choices = [(c, c) for c in accounts]

    if request.method == 'POST':
        name = request.form.get('name')

        if manager_ldap.name_exists(name):
            flash('User or Group {} already exists'.format(name), 'alert')
        elif form.validate():

            description = request.form.get('description')

            ret = manager_ldap.add_group(name, description, form.members.data)

            if ret is False:
                flash(
                    'Group {} cannot be added'.format(name),
                    'alert')
            else:
                return redirect(url_for('home.home'))

    return render_template('group/add.html', form=form, membersselected=request.form.get('members'))