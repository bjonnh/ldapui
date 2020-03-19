import flask_wtf
import wtforms
from wtforms.validators import InputRequired


class PasswordChangeForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password', [])
    password2 = wtforms.PasswordField('Password (again)', [])


class PasswordResetForm(flask_wtf.FlaskForm):
    authcode = wtforms.HiddenField('Authcode', [InputRequired()])
    password = wtforms.PasswordField('Password', [])
    password2 = wtforms.PasswordField('Password (again)', [])


class EmailResetForm(flask_wtf.FlaskForm):
    mail = wtforms.StringField('Email', [InputRequired()])
