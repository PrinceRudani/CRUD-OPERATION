from base import db
from base.utils.my_logger import get_logger

logger = get_logger()

class RegisterDao:
    def insert_register(self, register_vo):
        try:
            db.session.add(register_vo)
            db.session.commit()
            logger.info(f'Successfully inserted register_vo: {register_vo.as_dict()}')
        except Exception as e:
            logger.error(f'Error inserting register_vo: {str(e)}')
            db.session.rollback()
            raise