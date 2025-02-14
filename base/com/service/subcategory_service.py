from base.com.dao.subcategory_dao import SubCategoryDAO
from base.com.vo.subcategory_vo import SubcategoryVO
from base.utils.MyLogger import get_logger
from base.utils.time_stamp import get_current_timestamp


class SubcategoryService:
    def insert_subcategory_service(self, subcategory_category_id, subcategory_dto_lst):
        create_at = get_current_timestamp()
        modify_at = get_current_timestamp()

        sub_category_vo = SubcategoryVO()
        sub_category_vo.subcategory_category_id = subcategory_category_id
        sub_category_vo.sub_category_name = subcategory_dto_lst.sub_category_name
        sub_category_vo.sub_category_description = subcategory_dto_lst.sub_category_description
        sub_category_vo.create_at = create_at
        sub_category_vo.modify_at = modify_at

        sub_category_dao = SubCategoryDAO()
        sub_category_dao.insert_sub_category(sub_category_vo)

    def view_subcategory_service(self):
        sub_category_dao = SubCategoryDAO()
        sub_category_vo_lst = sub_category_dao.view_sub_category()
        return sub_category_vo_lst

    def delete_subcategory_service(self, sub_category_id):
        modify_at = get_current_timestamp()
        sub_category_vo = SubcategoryVO()
        sub_category_vo.modify_at = modify_at
        sub_category_dao = SubCategoryDAO()
        sub_category_dao.delete_sub_category(sub_category_id)

    def edit_subcategory_service(self, sub_category_id):
        sub_category_dao = SubCategoryDAO()

        sub_category, category_vo_lst = sub_category_dao.edit_sub_category(
            sub_category_id)
        return sub_category, category_vo_lst

    def update_subcategory_service(self, sub_category_id, subcategory_category_id, subcategory_dto_lst):

        modify_at = get_current_timestamp()

        sub_category_vo = SubcategoryVO()
        sub_category_vo.sub_category_id = sub_category_id
        sub_category_vo.subcategory_category_id = subcategory_category_id
        sub_category_vo.sub_category_name = subcategory_dto_lst.sub_category_name
        sub_category_vo.sub_category_description = subcategory_dto_lst.sub_category_description

        sub_category_vo.modify_at = modify_at

        sub_category_dao = SubCategoryDAO()
        sub_category_dao.update_sub_category(sub_category_vo)
