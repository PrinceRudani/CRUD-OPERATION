from base import db

class RegisterVo(db.Model):
    __tablename__ = "register_table"
    register_id = db.Column("register_id", db.Integer, autoincrement=True, primary_key=True)
    register_firstname = db.Column("register_firstname", db.String(255), nullable=False)
    register_lastname = db.Column("register_lastname", db.String(255), nullable=False)
    register_gender = db.Column("register_gender", db.String(255), nullable=False)
    register_email = db.Column("register_email", db.String(255), nullable=False)
    register_password = db.Column("register_password", db.String(255), nullable=False)
    is_delete = db.Column('is_delete', db.Boolean, nullable=False, default=False)
    create_at = db.Column('create_at', db.Integer, nullable=False)
    modify_at = db.Column('modify_at', db.Integer, nullable=True)

    def as_dict(self):
        return {
            "register_id": self.register_id,
            "register_firstname": self.register_firstname,
            "register_lastname": self.register_lastname,
            "register_gender": self.register_gender,
            "register_email": self.register_email,
            "register_password": self.register_password,
            "is_delete": self.is_delete,
            "create_at": self.create_at,
            "modify_at": self.modify_at,
        }

db.create_all()