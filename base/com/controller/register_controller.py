from flask import render_template, request

from base.com.service.login_service import LoginService
from base.com.service.register_service import RegisterService
from base.com.dto.register_dto import RegisterDTO
from base.utils import my_logger
from base import app

logger = my_logger.get_logger()


@app.route('/load_register', methods=['GET'])
# @LoginService.login_required(role="ADMIN")
def load_register():
    """
    Handle GET request to load the registration page.
    
    Returns:
        rendered registration page template
    """
    return render_template('login_and_register/register.html')


@app.route('/insert_register', methods=['POST'])
# @LoginService.login_required(role="ADMIN")
def register():
    """
    Handle POST request to process user registration.
    
    Gets registration form data from request, validates it using RegisterDTO,
    and creates new user account via RegisterService.
    
    Form Parameters:
        registerFirstname (str): User's first name
        registerLastname (str): User's last name
        registerGender (str): User's gender
        registerEmail (str): User's email address
        registerUsername (str): Desired username
        registerPassword (str): Account password
        
    Returns:
        On success: Rendered login page with success message
        On error: Rendered registration page with error message
        
    Raises:
        Exception: If validation fails or database operations fail
    """
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

        return render_template("login_and_register/login.html",
                               message="Registration Successful")

    except Exception as e:
        logger.error(f'Error in register route: {str(e)}')
        return render_template('login_and_register/register.html',
                               error=str(e))
