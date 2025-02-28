from flask import make_response
from flask import render_template, request, redirect, url_for

from base import app
from base.com.dao.login_dao import LoginDao
from base.com.service.login_service import LoginService
from base.custom_enum.static_variables import StaticVariables
from base.utils import my_logger

logger = my_logger.get_logger()
static_variables = StaticVariables()


@app.route('/')
def load_login_page():
    return render_template('login_and_register/login.html')


@app.route('/home', methods=['POST', 'GET'])
def load_home_page():
    if request.method == 'POST':
        try:
            username = request.form.get('register_username').strip() or None
            password = request.form.get('register_password').strip() or None

            login_dao = LoginDao()
            validate_user = login_dao.validate_login(username, password)

            if validate_user:
                user_data = validate_user.as_dict()
                if user_data['login_role'] not in ['ADMIN', 'USER']:
                    raise ValueError("Invalid user role")

                login_service = LoginService()
                access_token, refresh_token = login_service.generate_token(
                    user_data['login_id'],
                    user_data['login_username'],
                    user_data['login_role'])

                target_page = 'admin_home_page' \
                    if user_data['login_role'] == 'ADMIN' \
                    else 'user_home_page'
                response = redirect(url_for(target_page))
                response.set_cookie(static_variables.TOKEN_ACCESS_KEY,
                                    access_token, max_age=int(
                        static_variables.ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                                    httponly=True)
                response.set_cookie(static_variables.TOKEN_REFRESH_KEY,
                                    refresh_token, max_age=int(
                        static_variables.REFRESH_TOKEN_EXPIRE_MINUTES) * 60,
                                    httponly=True)
                logger.info(
                    f"Access & Refresh token created for user: {username} - "
                    f"Access Token: {access_token}, Refresh Token: {refresh_token}")

                return response

            else:
                raise ValueError("Invalid username or password.")


        except ValueError as e:
            logger.error(f"Error: {e}")
            return render_template("login_and_register/login.html",
                                   error="Invalid username, password, or user role.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return render_template("login_and_register/login.html",
                                   error="An error occurred. Please try again later.")

    return render_template('login_and_register/login.html',
                           error="login is required. Please login to continue.")


@app.route('/admin/home', methods=['GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def admin_home_page():
    access_token = request.cookies.get(static_variables.TOKEN_ACCESS_KEY)
    logger.info(f"Admin accessing home page with token: {access_token}")

    response = make_response(render_template('home.html'))
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@app.route('/user/home', methods=['GET'])
@LoginService.login_required(role=static_variables.USER_ROLE)
def user_home_page():
    logger.info("User accessing home page")

    response = make_response(render_template('user_home_page.html'))
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@app.route('/logout')
def logout():
    response = redirect(url_for('load_login_page'))
    response.delete_cookie(static_variables.TOKEN_ACCESS_KEY)
    response.delete_cookie(static_variables.TOKEN_REFRESH_KEY)

    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    logger.info("User logged out successfully")
    return response
