import uuid

from flask import request, flash, render_template, redirect, url_for
from flask_login import current_user, logout_user

from app import db
from app.auth.storage.ldap import manager_ldap
from app.auth.email import send_email
from app.auth.forms.password import PasswordResetForm, EmailResetForm
from app.auth.models.resetcodes import ResetCodes
from app.auth.views.password import password_blueprint


@password_blueprint.route('/reset/pw', methods=['GET', 'POST'])
def reset():
    form = PasswordResetForm()
    if request.method == 'GET':
        if 'authcode' in request.args:
            # User received a link we allow it to change pw
            reset_code = ResetCodes.query.filter_by(code=request.args.get('authcode')).first()
            if not reset_code:
                flash("Reset code is incorrect", "alert")
            else:
                form.authcode.data = request.args.get('authcode')
            return render_template('password/reset.html', form=form)
        else:
            ResetCodes.query.filter_by(code=request.args.get('authcode')).first()

            return render_template('password/email.html', form=EmailResetForm())
    if request.method == 'POST':
        if 'mail' in request.form:
            mail = request.form.get('mail')
            user = manager_ldap.find_user_by_email(mail)
            if user:

                authcode = str(uuid.uuid4())
                # We delete all the old codes

                ResetCodes.query.filter_by(username=str(user['cn']), email=mail).delete()

                reset_code = ResetCodes(username=str(user['cn']), email=mail, code=authcode)
                db.session.add(reset_code)
                db.session.commit()
                send_email(email=mail, code=authcode)

            flash("You will receive an email with the instructions.", "info")
        else:
            reset_code = ResetCodes.query.filter_by(code=request.form.get('authcode')).first()
            if not reset_code:
                flash("Invalid code, please try requesting a new password reset.", "alert")
                return render_template('password/email.html', form=EmailResetForm())

            password = request.form.get('password')
            password2 = request.form.get('password2')
            if password != password2:
                flash("Your passwords are not the same", "warning")
                return render_template('password/reset.html', form=form)

            if password == "":
                flash("Your new password cannot be empty", "danger")
                return render_template('password/reset.html', form=form)

            ret = manager_ldap.change_password(reset_code.username, password)
            if ret:
                ResetCodes.query.filter_by(code=request.form.get('authcode')).delete()
            flash('You have a new password set, please login again', 'info')

        logout_user()
    return redirect(url_for('home.home'))
