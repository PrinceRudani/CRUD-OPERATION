from base import db
from base.com.vo.category_vo import CategoryVO
from base.com.vo.subcategory_vo import SubcategoryVO
from base.utils.time_stamp import get_current_timestamp


class SubCategoryDAO:
    @staticmethod
    def insert_sub_category(sub_category_vo):
        db.session.query(SubcategoryVO).filter_by(
            sub_category_name=sub_category_vo.sub_category_name).first()
        db.session.add(sub_category_vo)
        db.session.commit()

    @staticmethod
    def view_sub_category():
        sub_category_vo_lst = (db.session.query(CategoryVO, SubcategoryVO)
                               .join(SubcategoryVO,
                                     CategoryVO.category_id == SubcategoryVO.subcategory_category_id)
                               .filter(SubcategoryVO.is_delete == False,
                                       CategoryVO.is_delete == False)
                               .all())
        print(sub_category_vo_lst)
        return sub_category_vo_lst

    @staticmethod
    def delete_sub_category(sub_category_id):
        sub_category = db.session.query(SubcategoryVO).get(sub_category_id)
        sub_category.modify_at = get_current_timestamp()
        sub_category.is_delete = True
        db.session.commit()

    @staticmethod
    def edit_sub_category(sub_category_id):
        sub_category_vo = db.session.query(SubcategoryVO).filter_by(
            sub_category_id=sub_category_id).first()
        category_vo_lst = (db.session.query(CategoryVO)
                           .filter(CategoryVO.is_delete == False)
                           .all())
        return sub_category_vo, category_vo_lst

    @staticmethod
    def update_sub_category(sub_category_vo):
        sub_category = db.session.merge(sub_category_vo)
        db.session.commit()
        return sub_category