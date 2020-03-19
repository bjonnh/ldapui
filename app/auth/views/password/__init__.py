from flask import Blueprint


password_blueprint = Blueprint('password', __name__)

import app.auth.views.password.reset
