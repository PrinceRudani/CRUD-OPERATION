from flask import render_template, request, jsonify
from base.utils import MyLogger
from base import app

users = {"register_username": "prince@123",
         "register_password": "prince123"}
logger = MyLogger.get_logger()


@app.route('/')
def login_page():
    return render_template('login_and_register/login.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('register_username')
        password = request.form.get('register_password')
        if username == users["register_username"] and password == users["register_password"]:
            logger.info(
                "Login successful. username -> {}, password -> {}".format(
                    username,
                    password))
            return render_template("home.html")
        else:
            logger.warning(
                "Invalid credentials attempt. username -> {}".format(username))
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error(f"An error occurred during login: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500
