from flask import request, flash, render_template, redirect, url_for
from flask_login import login_required

from app.auth.storage.ldap import manager_ldap
from app.auth.forms.user import EditUserForm
from app.auth.views import ChoiceObj
from app.auth.views.user import user_blueprint
from app.helpers.views import is_admin


@user_blueprint.route('/user/edit', methods=['GET', 'POST'])
@login_required
@is_admin
def edit():
    failed = False

    if request.method == 'GET':
        username = request.args.get('username')
    elif request.method == 'POST':
        username = request.form.get('username')
    else:
        raise ValueError('Invalid')
    groups = [group['cn'] for group in manager_ldap.groups]
    selected_choices = ChoiceObj('groups', manager_ldap.groups_of_user(username))

    form = EditUserForm(obj=selected_choices)
    form.groups.choices = [(c, c) for c in groups]
    if request.method == 'GET':
        form.username.data = request.args.get('username')
        data_user = manager_ldap.get_info_user(request.args.get('username'))
        form.mail.data = data_user['mail']
        form.display_name.data = data_user['display_name']
        form.surname.data = data_user['surname']
        failed = True

    if request.method == 'POST':
        if form.validate():
            username = request.form.get('username')
            pw = request.form.get('password')
            pw2 = request.form.get('password2')
            mail = request.form.get('mail')
            surname = request.form.get('surname')
            display_name = request.form.get('display_name')

            if pw != "" and pw == pw2:
                ret = manager_ldap.update_user_password(username, pw)
                if ret:
                    flash('User {} has a new password set'.format(username), 'info')
                    failed = False
                else:
                    failed = True

            if not failed:
                ret = manager_ldap.update_groups_of_user(username, form.groups.data)

                if ret:
                    flash(
                        'User {} modified'.format(username),
                        'info')
                    failed = False
                else:
                    flash(
                        'User {} cannot have its groups updated'.format(username),
                        'alert')
                    failed = True

            if not failed:
                ret = manager_ldap.update_user_mail(username, mail)
                ret &= manager_ldap.update_user_surname(username, surname)
                ret &= manager_ldap.update_user_display_name(username, display_name)

                if ret:
                    failed = False
                else:
                    flash(
                        'User {} cannot have its details updated'.format(username),
                        'alert')
                    failed = True

    if failed:
        return render_template('user/edit.html', form=form, groupsselected=request.form.get('groups'))
    else:
        return redirect(url_for('home.home'))
