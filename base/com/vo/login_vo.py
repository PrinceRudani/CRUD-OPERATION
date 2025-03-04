from base import db

class LoginVO(db.Model):
    __tablename__ = 'login_table'
    __table_args__ = {'extend_existing': True}  # Avoid redefinition errors

    login_id = db.Column('login_id', db.Integer, primary_key=True, autoincrement=True)
    login_username = db.Column('login_username', db.String(255), unique=True, nullable=False)
    login_password = db.Column('login_password', db.String(1000), nullable=False)
    login_role = db.Column('login_role', db.String(255), nullable=False)
    login_status = db.Column('login_status', db.Boolean, nullable=False, default=False)
    create_at = db.Column('create_at', db.Integer, nullable=False)
    modify_at = db.Column('modify_at', db.Integer, nullable=True)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'login_status': self.login_status,
            'create_at': self.create_at,
            'modify_at': self.modify_at,
        }

db.create_all()