from base import db


class RegisterVO(db.Model):
    __tablename__ = 'register_table'
    register_id = db.Column('register_id', db.Integer, primary_key=True, autoincrement=True)
    register_firstname = db.Column('register_firstname', db.String(255), nullable=False)
    register_lastname = db.Column('register_lastname', db.String(255), nullable=False)
    register_username = db.Column('register_username', db.String(255), unique=True, nullable=False)
    register_password = db.Column('register_password', db.String(16), nullable=False)

    def as_dict(self):
        return {'register_id': self.register_id, 'register_firstname': self.register_firstname,
                'register_lastname': self.register_lastname, 'register_username': self.register_username,
                'register_password': self.register_password}


db.create_all()
