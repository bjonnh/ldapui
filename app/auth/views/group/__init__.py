from flask import Blueprint


group_blueprint = Blueprint('group', __name__)

import app.auth.views.group.add
import app.auth.views.group.edit
import app.auth.views.group.remove
