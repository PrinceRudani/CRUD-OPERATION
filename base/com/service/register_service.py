from base.com.dao.login_dao import LoginDao
from base.com.dao.register_dao import RegisterDao
from base.com.vo.login_vo import LoginVO
from base.com.vo.register_vo import RegisterVo
from base.utils.time_stamp import get_current_timestamp
from base.utils.my_logger import get_logger

logger = get_logger()

class RegisterService:
    def insert_register_service(self, register_dto_lst):
        try:
            # Create LoginVO object to insert login information
            login_vo = LoginVO()
            login_vo.login_username = register_dto_lst.register_username
            login_vo.login_password = register_dto_lst.register_password

            # # Hash the password using SHA-256
            #
            # hashed_password = hashlib.sha256(
            #     register_dto_lst.register_password.encode()).hexdigest()
            # login_vo.login_password = hashed_password

            login_vo.login_role = 'ADMIN'
            login_dao = LoginDao()
            login_id = login_dao.insert_login(login_vo)

            register_vo = RegisterVo()
            register_vo.register_firstname = register_dto_lst.register_firstname
            register_vo.register_lastname = register_dto_lst.register_lastname
            register_vo.register_gender = register_dto_lst.register_gender
            register_vo.register_email = register_dto_lst.register_email
            register_vo.register_login_id = login_id
            register_vo.create_at = get_current_timestamp()
            register_vo.modify_at = get_current_timestamp()

            # Insert user data into RegisterDao
            register_dao = RegisterDao()
            register_dao.insert_register(register_vo)

            logger.info('Registration successful and data inserted into database.')
        except Exception as e:
            logger.error(f'Error inserting register: {str(e)}')
            raise
