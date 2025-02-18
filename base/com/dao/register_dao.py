from base import db
from base.com.vo.register_vo import RegisterVo

class RegisterDao:
    def insert_register(self,register_vo):
        db.session.add(register_vo)
        db.session.commit()
        return register_vo