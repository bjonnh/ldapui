import flask_wtf
import wtforms
from wtforms.validators import InputRequired


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', [InputRequired()])
    password = wtforms.PasswordField('Password', [InputRequired()])
