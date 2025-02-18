from base import db
from base.com.vo.category_vo import CategoryVO
from base.utils.time_stamp import get_current_timestamp


class CategoryDAO:
    def insert_category(self, category_vo):
        db.session.add(category_vo)
        db.session.commit()
        return category_vo

    def view_category(self):
        category_vo_lst = CategoryVO.query.filter(
            CategoryVO.is_delete == False).all()
        # print(category_vo_lst)
        return category_vo_lst

    def delete_category(self, category_id):
        category = db.session.query(CategoryVO).get(category_id)
        category.modify_at = get_current_timestamp()
        category.is_delete = True
        db.session.commit()

    def edit_category(self, category_id):
        return db.session.query(CategoryVO).filter_by(
            category_id=category_id).first()

    def update_category(self, category_id, category_name,
                        category_description):
        """
        Updates a category in the database.
        """
        category = db.session.query(CategoryVO).get(category_id)
        category.category_name = category_name
        category.category_description = category_description
        category.modify_at = get_current_timestamp()

        db.session.commit()
        return category
