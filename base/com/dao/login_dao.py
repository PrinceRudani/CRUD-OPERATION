from base import db
from base.com.vo.login_vo import LoginVO
from base.utils import MyLogger

logger = MyLogger.get_logger()


class LoginDao:
    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()
        return login_vo.login_id

    def validate_login(self, username, password):
        try:
            user = LoginVO.query.filter_by(login_username=username).first()
            if user and user.login_password == password:
                return user
            return None
        except Exception as e:
            logger.error(f'Error validating login: {str(e)}')
            raise