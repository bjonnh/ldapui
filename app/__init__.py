from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']
app.secret_key = os.environ['SECRET_KEY']
app.config['LDAP_PROTOCOL_VERSION'] = 3

from app.auth.storage.ldap import LdapWrap

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.auth.views import home_blueprint
app.register_blueprint(home_blueprint)

from app.auth.views.login import login_blueprint
app.register_blueprint(login_blueprint)

from app.auth.views.password import password_blueprint
app.register_blueprint(password_blueprint)

from app.auth.views.user import user_blueprint
app.register_blueprint(user_blueprint)

from app.auth.views.group import group_blueprint
app.register_blueprint(group_blueprint)

app.register_blueprint(Blueprint('static', __name__, static_folder='static/'))

db.create_all()
