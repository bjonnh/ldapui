from flask import url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import redirect

from app.auth.views.login import login_blueprint


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))
