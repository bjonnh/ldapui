import ldap3
import ldap3.core.exceptions
from flask import flash, redirect, url_for, request, render_template
from flask_login import current_user, login_user

from app import db
from app.auth.forms.login import LoginForm
from app.auth.models.user import User
from app.auth.views.login import login_blueprint
from app.helpers.ldap import sha_password


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home.home'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        try:

            User.try_login(username, password)
        except ldap3.core.exceptions.LDAPBindError:

            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)

        user = User.query.filter_by(username=username, password=sha_password(password)).first()

        if user is None:
            user = User(username, sha_password(password))

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('home.home'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)
