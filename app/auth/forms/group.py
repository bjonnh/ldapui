import flask_wtf
import wtforms
from wtforms.validators import InputRequired

from app.auth.forms import MultiCheckboxField


class AddGroupForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name', [InputRequired()])
    description = wtforms.StringField('Description', [InputRequired()])
    members = MultiCheckboxField(None)


class EditGroupForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name', [InputRequired()])
    description = wtforms.StringField('Description', [InputRequired()])
    members = MultiCheckboxField(None)


class RemoveGroupForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name', [InputRequired()])
