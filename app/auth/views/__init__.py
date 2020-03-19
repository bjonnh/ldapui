from flask import request, render_template, g, Blueprint
from flask_login import current_user

from app import login_manager
from app.auth.forms.password import PasswordChangeForm
from app.auth.models.user import User
from app.auth.storage.ldap import manager_ldap

login_manager.login_view = "login.login"


@login_manager.user_loader
def load_user(_id):
    user = User.query.get(int(_id))
    if user is not None:
        return user
    else:
        return None


home_blueprint = Blueprint('home', __name__)


@home_blueprint.before_request
def get_current_user():
    g.user = current_user


@home_blueprint.route('/')
@home_blueprint.route('/home')
def home():
    form = PasswordChangeForm(request.form)
    return render_template('home.html', form=form,
                           groups=manager_ldap.groups,
                           users=manager_ldap.users)


class ChoiceObj(object):
    def __init__(self, name, choices):
        # this is needed so that BaseForm.process will accept the object for the named form,
        # and eventually it will end up in SelectMultipleField.process_data and get assigned
        # to .data
        setattr(self, name, choices)
