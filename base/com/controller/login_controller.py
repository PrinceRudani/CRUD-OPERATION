from flask import render_template, request, jsonify, redirect, url_for, \
    make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from base.com.dao.login_dao import LoginDao
from base.com.service.login_service import LoginService
from base.utils import my_logger
from base import app
from base.config.static_variables import StaticVariables

logger = my_logger.get_logger()


@app.route('/')
def load_login_page():
    return render_template('login_and_register/login.html')


@app.route('/home', methods=['POST', 'GET'])
def load_home_page():
    if request.method == 'POST':
        try:
            username = request.form.get('register_username')
            password = request.form.get('register_password')

            login_dao = LoginDao()
            validate_user = login_dao.validate_login(username, password)

            if validate_user:
                user_data = validate_user.as_dict()
                if 'login_id' not in user_data:
                    raise ValueError(
                        "User ID is missing in database response.")

                if user_data['login_role'] != 'ADMIN':
                    raise ValueError(
                        "Access denied. Admin privileges required.")

                login_service = LoginService()
                access_token = login_service.generate_token(
                    user_data['login_id'],
                    user_data['login_username'],
                    user_data['login_role'])
                refresh_token = create_refresh_token(identity=username)
                logger.info(
                    f"Access & Refresh token created for user: {username} - "
                    f"Access "
                    f"Token: {access_token}\n, Refresh Token: {refresh_token}")
                return redirect(url_for('admin_home_page'))

            else:
                raise ValueError("Invalid username or password.")

        except Exception as e:
            logger.error(f"Error in load_home_page: {e}")
            return render_template("login_and_register/login.html",
                                   error=str(e))

    return render_template('login_and_register/login.html')


@app.route('/admin/home', methods=['GET'])
@LoginService.login_required(role="ADMIN")
def admin_home_page():
    return render_template('home.html')
