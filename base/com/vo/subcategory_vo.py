from base import db

class SubcategoryVO(db.Model):
    __tablename__ = 'sub_category_table'
    subcategory_category_id = db.Column('subcategory_category_id',
                                                    db.Integer, db.ForeignKey('category_table.category_id', ondelete="CASCADE"), nullable=False)
    sub_category_id = db.Column('sub_category_id', db.Integer, primary_key=True, autoincrement=True)
    sub_category_name = db.Column('sub_category_name', db.String(100), nullable=False)
    sub_category_description = db.Column('sub_category_description', db.String(1000), nullable=False)
    is_delete = db.Column('is_delete', db.Boolean, nullable=False, default=False)
    create_at = db.Column('create_at', db.Integer, nullable=True)
    modify_at = db.Column('modify_at', db.Integer, nullable=True)

    def as_dict(self):
        return {
            'subcategory_category_id': self.subcategory_category_id,
            'sub_category_id': self.sub_category_id,
            'sub_category_name': self.sub_category_name,
            'sub_category_description': self.sub_category_description,
            'is_delete': self.is_delete,
            'create_at': self.create_at,
            'modify_at': self.modify_at,
        }
db.create_all()