from base.com.dao.register_dao import RegisterDao
from base.com.vo.register_vo import RegisterVo
from base.utils.time_stamp import get_current_timestamp
from base.utils.MyLogger import get_logger

logger = get_logger()

class RegisterService:
    def insert_register_service(self,register_dto_lst):
        try:
            register_vo = RegisterVo()

            register_vo.register_firstname = register_dto_lst.register_firstname
            register_vo.register_lastname = register_dto_lst.register_lastname
            register_vo.register_gender = register_dto_lst.register_gender
            register_vo.register_email = register_dto_lst.register_email
            register_vo.register_username = register_dto_lst.register_username
            register_vo.register_password = register_dto_lst.register_password

            register_vo.register_create_at = get_current_timestamp()
            register_vo.register_modify_at = get_current_timestamp()

            register_dao = RegisterDao()
            register_dao.insert_register(register_vo)

            logger.info('Insert register successfully')
        except Exception as e:
            return str(e)