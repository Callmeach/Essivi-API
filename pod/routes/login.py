from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request, jsonify, abort, make_response, current_app
from werkzeug.security import check_password_hash

from ..models.utilisateur import Utilisateur

login_bp = Blueprint("login_bp", __name__)

@login_bp.post('/users/login')
def login():
    try:
        data = request.get_json()
        if not data:
            return {
                'message': 'Please, provide user details',
                'data': None,
                'error': 'Bad request'
            }, 400
        if not data or not data.get('email') or not data.get('password'):
            # return 401 if any email or / password and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm = "Login required !!"'}
            )
        user = Utilisateur.query.filter_by(email = data.get('email')).first()
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm = "User does not exist !!"'}
            )
        if check_password_hash(user.password, data.get('password')):
            try:
                # generates the JWT Token
                token = jwt.encode(
                    {
                        'id': user.id,
                        'exp': datetime.utcnow() + timedelta(minutes = 59)
                    },
                    current_app.config['SECRET_KEY'],
                    algorithm="HS256"
                )
                return make_response(jsonify(
                    {
                        'token': token
                    }
                ),201)
            except Exception as e:
                return {
                    "error": "Something went wong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token, wrong password",
            "data": None,
            "error": "Unauthorized"
        },404
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None,
        }, 500