import flask_wtf
import wtforms
from wtforms.validators import InputRequired

from app.auth.forms import MultiCheckboxField


class AddUserForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', [InputRequired()])
    password = wtforms.PasswordField('Password', [InputRequired()])
    password2 = wtforms.PasswordField('Password (again)', [InputRequired()])
    mail = wtforms.StringField('Email', [InputRequired()])
    first_name = wtforms.StringField('First name', [InputRequired()])
    surname = wtforms.StringField('Surname', [InputRequired()])
    groups = MultiCheckboxField(None)


class EditUserForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', [InputRequired()])
    password = wtforms.PasswordField('Password', [])
    password2 = wtforms.PasswordField('Password (again)', [])
    mail = wtforms.StringField('Email', [InputRequired()])
    display_name = wtforms.StringField('Display name', [InputRequired()])
    surname = wtforms.StringField('Surname', [InputRequired()])
    groups = MultiCheckboxField(None)


class RemoveUserForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', [InputRequired()])
