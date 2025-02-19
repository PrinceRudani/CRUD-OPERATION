from base import db
from base.com.vo.login_vo import LoginVO

class LoginDao:
    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()
        return login_vo.login_id

    def validate_login(self, username, password):
        user = LoginVO.query.filter_by(login_username=username,
                                       login_password=password).first()
        return user