from flask import Blueprint


login_blueprint = Blueprint('login', __name__)

import app.auth.views.login.login
import app.auth.views.login.logout
