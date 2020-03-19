from flask import Blueprint


user_blueprint = Blueprint('user', __name__)

import app.auth.views.user.add
import app.auth.views.user.edit
import app.auth.views.user.password
import app.auth.views.user.remove
