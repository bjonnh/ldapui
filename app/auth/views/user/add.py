from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.user import AddUserForm
from app.auth.views import ChoiceObj
from app.auth.views.user import user_blueprint
from app.helpers.views import is_admin


@user_blueprint.route('/user/add', methods=['GET', 'POST'])
@login_required
@is_admin
def add():
    groups = [group['cn'] for group in manager_ldap.groups]
    selected_choices = ChoiceObj('groups', request.form.get('groups'))
    form = AddUserForm(obj=selected_choices)
    form.groups.choices = [(c, c) for c in groups]

    if request.method == 'POST':
        username = request.form.get('username')

        if manager_ldap.name_exists(username):
            flash('User or group {} already exists'.format(username), 'alert')
        elif form.validate():
            pw = request.form.get('password')
            pw2 = request.form.get('password2')
            mail = request.form.get('mail')
            first_name = request.form.get('first_name')
            surname = request.form.get('surname')
            display_name = first_name + " " + surname

            if pw == pw2:
                ret = manager_ldap.add_user(username, pw, mail, display_name, surname)
                if ret is not None:
                    ret2 = manager_ldap.update_groups_of_user(username, form.groups.data)

                    if ret2 is not None:
                        flash(
                            'User {} added'.format(username),
                            'info')
                        return redirect(url_for('home.home'))
                    else:
                        flash(
                            'User {} cannot have its groups updated'.format(username),
                            'alert')
                else:
                    flash(
                        'User {} cannot be added'.format(username),
                        'alert')

    return render_template('user/add.html', form=form, groupsselected=request.form.get('groups'))
