from flask import render_template, request

from base import app
from base.com.dto.register_dto import RegisterDTO
from base.com.service.register_service import RegisterService
from base.utils.MyLogger import get_logger

logger = get_logger()


@app.route('/load_register', methods=['GET'])
def load_register():
    return render_template('login_and_register/register.html')


@app.route('/insert_register', methods=['POST'])
def register():
    try:
        register_firstname = request.form.get(
            'registerFirstname').strip() or None
        register_lastname = request.form.get(
            'registerLastname').strip() or None
        register_gender = request.form.get('registerGender').strip() or None
        register_email = request.form.get('registerEmail').strip() or None
        register_username = request.form.get(
            'registerUsername').strip() or None
        register_password = request.form.get(
            'registerPassword').strip() or None

        logger.info(
            f'Received form data: {register_firstname}, {register_lastname}, {register_gender}, {register_email}, {register_username}, {register_password}')

        register_dto = RegisterDTO(register_firstname=register_firstname,
                                   register_lastname=register_lastname,
                                   register_gender=register_gender,
                                   register_email=register_email,
                                   register_username=register_username,
                                   register_password=register_password)
        register_dto_lst = register_dto.validate()
        register_service = RegisterService()
        register_service.insert_register_service(register_dto_lst)
        return render_template("login_and_register/login.html")
    except Exception as e:
        logger.error(f'Error in register route: {str(e)}')
        return render_template('login_and_register/register.html',
                               error=str(e))
