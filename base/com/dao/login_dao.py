from base import db
from base.com.vo.login_vo import LoginVO
from base.utils import my_logger

logger = my_logger.get_logger()

class LoginDao:
    def insert_login(self, login_vo):
        try:
            db.session.add(login_vo)
            db.session.commit()
            logger.info(f"Inserted login with ID: {login_vo.login_id}")
            return login_vo.login_id
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inserting login: {str(e)}")
            raise

    def validate_login(self, username, password):
        try:
            user = LoginVO.query.filter_by(login_username=username,
                                           login_password=password).first()
            if user :
                logger.info(f"User {username} validated successfully.")
                return user
            logger.warning(f"Invalid login attempt for user: {username}")
            return None
        except Exception as e:
            logger.error(f"Error validating login: {str(e)}")
            raise