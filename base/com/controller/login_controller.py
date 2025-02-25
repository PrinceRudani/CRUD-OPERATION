from flask import render_template, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from base.com.dao.login_dao import LoginDao
from base.utils import MyLogger
from base import app

import jwt
logger = MyLogger.get_logger()


@app.route('/')
def loginpage():
    return render_template('login_and_register/login.html')

@app.route('/home')
def home_page():
    return render_template('home.html')
@app.route('/login', methods=['POST'])
def loginrequired():
    try:
        username = request.form.get('register_username')
        password = request.form.get('register_password')
        login_dao = LoginDao()
        validate_user = login_dao.validate_login(username, password)
        if validate_user:
            user_data = validate_user.as_dict()
            access_token_ = create_access_token(identity=user_data)
            refresh_token = create_refresh_token(identity=username)
            return render_template('home.html')
        else:
            raise Exception("Invalid username or password.")
    except Exception as e:
        return render_template("login_and_register/login.html", error=str(e))
