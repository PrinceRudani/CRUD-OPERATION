from flask import render_template, request, redirect, url_for, make_response

from base import app
from base.com.dao.login_dao import LoginDao
from base.com.service.login_service import LoginService
from base.custom_enum.static_variables import StaticVariables
from base.utils import my_logger

logger = my_logger.get_logger()
static_variables = StaticVariables()


@app.route('/')
def load_login_page():
    """Render the login page."""
    return render_template('login_and_register/login.html')


@app.route('/home', methods=['POST', 'GET'])
def load_home_page():
    """
    Handle login form submission and redirect to appropriate home page.
    
    On POST:
    - Validates username/password
    - Generates access and refresh tokens
    - Redirects to admin or user home page based on role
    - Sets httponly cookies with tokens
    
    On GET:
    - Returns login page with error message
    
    Returns:
        Response object with redirect or rendered template
    """
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

                target_page = 'admin_home_page' if user_data[
                                                       'login_role'] == 'ADMIN' else 'user_home_page'
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
                    f"Access & Refresh token created for user: {username}")

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
    """
    Render admin home page for authenticated admin users.
    
    Requires valid admin role token.
    Sets cache control headers to prevent page caching.
    
    Returns:
        Response with rendered admin home template
    """
    logger.info("Admin accessing home page")
    response = make_response(render_template('home.html'))
    # Set cache control headers to prevent caching of the page
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/user/home', methods=['GET'])
@LoginService.login_required(role=static_variables.USER_ROLE)
def user_home_page():
    """
    Render user home page for authenticated regular users.
    
    Requires valid user role token.
    Sets cache control headers to prevent page caching.
    
    Returns:
        Response with rendered user home template
    """
    logger.info("User accessing home page")
    response = make_response(render_template('user_home_page.html'))
    # Set cache control headers to prevent caching of the page
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/logout')
def logout():
    """
    Handle user logout.
    
    - Clears access and refresh token cookies
    - Redirects to login page
    - Sets cache control headers
    
    Returns:
        Response object with redirect to login page
    """
    response = redirect(url_for('load_login_page'))

    response.set_cookie(static_variables.TOKEN_ACCESS_KEY, '', expires=0,
                        path='/', httponly=True)
    response.set_cookie(static_variables.TOKEN_REFRESH_KEY, '', expires=0,
                        path='/', httponly=True)

    logger.info("User logged out successfully")
    # Set headers to ensure login page is not cached
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
