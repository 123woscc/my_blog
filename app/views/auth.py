from flask import Blueprint, request, session, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user

from ..models import User
from ..forms import LoginForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
