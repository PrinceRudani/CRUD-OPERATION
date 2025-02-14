from flask_jwt_extended import create_refresh_token

from flask_jwt_extended import create_refresh_token
from flask import jsonify


def refresh_token(username):
    try:
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            "refresh_token": refresh_token,
            "status": "success"
        }), 200

    except Exception as e:
        # Handle any potential errors during token creation
        return jsonify({
            "error": "Failed to generate refresh token",
            "details": str(e)
        }), 500


def login_required(self):
    pass

def logout(self):
    pass













# from flask import render_template, request, redirect
#
# from base import app
# from base.com.dao.register_dao import RegisterDAO
# from base.com.vo.register_vo import RegisterVO
#
#
# @app.route('/')
# def home():
#     return render_template("login/login.html")
#
#
# @app.route('/load_register')
# def load_register():
#     return render_template("login/register.html")
#
#
# @app.route('/insert_register', methods=["POST"])
# def add_register():
#     register_firstname = request.form.get("firstname")
#     register_lastname = request.form.get("lastname")
#     register_username = request.form.get("username")
#     register_password = request.form.get("password")
#     register_dao = RegisterDAO()
#     register_vo = RegisterVO()
#     register_vo.register_firstname = register_firstname
#     register_vo.register_lastname = register_lastname
#     register_vo.register_username = register_username
#     register_vo.register_password = register_password
#     register_dao.insert_register(register_vo)
#     return redirect('/view_register')
#
#
# @app.route('/view_register')
# def welcome():
#     register_dao = RegisterDAO()
#     register_vo_lst = register_dao.view_register()
#     return render_template("login/login.html", register_vo_lst=register_vo_lst)
