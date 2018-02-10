from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g
from ..models import User
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password=''):
    user = User.verify_auth_token(email_or_token)
    if user is None:
        user = User.query.filter_by(email=email_or_token).first()
        if not user:
            return False
        else:
            if not user.verify_password(password):
                return False
    g.current_user = user
    return True


@auth.error_handler
def unauthrized():
    return jsonify(error='Unauthorized access'), 404


@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.current_user.gen_auth_token(600)
    return jsonify(token=token.decode('ascii'), duration=600)
