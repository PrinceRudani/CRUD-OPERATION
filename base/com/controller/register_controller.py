from flask import render_template, request

from base import app
from base.com.dto.register_dto import RegisterDTO
from base.com.service.register_service import RegisterService


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':

            register_firstname = request.form.get('register_firstname').strip() or None
            register_lastname = request.form.get('register_lastname').strip() or None
            register_gender = request.form.get('register_gender').strip() or None
            register_email = request.form.get('register_email').strip() or None
            register_username = request.form.get('register_username').strip() or None
            register_password = request.form.get('register_password').strip() or None
            register_dto = RegisterDTO(register_firstname=register_firstname,
                                       register_lastname=register_lastname,
                                       register_gender=register_gender,
                                       register_email=register_email,
                                       register_username=register_username,
                                       register_password=register_password)
            register_dto_lst = register_dto.validate()
            register_service = RegisterService()
            register_service.insert_register_service(register_dto_lst)
            return render_template("home.html")
        else:
            return render_template('login_and_register/register.html')
    except Exception as e:
        return render_template('login_and_register/register.html',
                               errors=str(e))
