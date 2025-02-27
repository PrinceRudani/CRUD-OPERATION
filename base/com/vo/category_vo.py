from base import db

class CategoryVO(db.Model):
    __tablename__ = 'category_table'
    category_id = db.Column('category_id', db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column('category_name', db.String(100), nullable=False)
    category_description = db.Column('category_description', db.String(200), nullable=False)
    is_delete = db.Column('is_delete', db.Boolean, nullable=False, default=False)
    create_at = db.Column('create_at', db.Integer, nullable=False)
    modify_at = db.Column('modify_at', db.Integer, nullable=True)

    def as_dict(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'category_description': self.category_description,
            'is_delete': self.is_delete,
            'create_at': self.create_at,
            'modify_at': self.modify_at,
        }

db.create_all()