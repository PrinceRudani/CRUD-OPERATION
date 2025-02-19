from flask import render_template, request

from base import app
from base.com.dao.login_dao import LoginDao
from base.utils import MyLogger

logger = MyLogger.get_logger()


@app.route('/')
def login_page():
    return render_template('login_and_register/login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('register_username')
        password = request.form.get('register_password')
        login_dao = LoginDao()
        validate_user = login_dao.validate_login(username, password)
        if validate_user:
            logger.info("username: {}".format(username))
            return render_template("home.html")
        else:
            error = "Invalid username or password"
            return render_template("login_and_register/login.html",
                                   error=error)
    except Exception as e:
        logger.error("Error occurred during login: {}".format(str(e)))
        return render_template("login_and_register/login.html",
                               error="Something went wrong")
