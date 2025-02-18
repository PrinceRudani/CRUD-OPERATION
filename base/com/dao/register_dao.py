from base import db
from base.com.vo.login_vo import RegisterVO


class RegisterDAO:
    def insert_register(self, register_vo):
        db.session.add(register_vo)
        db.session.commit()

    def validate_login(self, username, password):
        user = db.session.query(RegisterVO).filter_by(register_username=username).first()
        return user
