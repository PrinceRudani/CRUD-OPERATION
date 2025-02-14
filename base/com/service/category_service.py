from base.com.dao.category_dao import CategoryDAO
from base.com.dto.category_dto import CategoryDTO
from base.com.vo.category_vo import CategoryVO
from base.utils.time_stamp import get_current_timestamp
from base.utils.MyLogger import get_logger

logger = get_logger()


class CategoryService:

    def add_category_service(self, category_dto_lst):
        try:
            create_at = get_current_timestamp()
            modify_at = get_current_timestamp()

            category_vo = CategoryVO()
            category_vo.category_name = category_dto_lst['category_name']
            category_vo.category_description = category_dto_lst['category_description']

            category_vo.create_at = create_at
            category_vo.modify_at = modify_at

            category_dao = CategoryDAO()
            new_category = category_dao.insert_category(category_vo)
            logger.info('Insert category successfully')
            return new_category

        except Exception as e:
            raise RuntimeError(f"Error in add_category_service: {str(e)}")

    def view_category_service(self):
        try:
            category_dao = CategoryDAO()
            category_vo_lst = category_dao.view_category()
            logger.info(
                'view category successfully {} '.format(category_vo_lst))
            return category_vo_lst
        except Exception as e:
            raise RuntimeError(f"Error in view_category_service: {str(e)}")

    def delete_category_service(self, category_id):
        try:
            category_dao = CategoryDAO()
            category_vo = CategoryVO()
            modify_at = get_current_timestamp()
            category_vo.modify_at = modify_at
            category_dao.delete_category(category_id)
            logger.info(
                'delete category successfully : {}'.format(category_id))
        except Exception as e:
            raise RuntimeError(f"Error in delete_category_service: {str(e)}")

    def edit_category_service(self, category_id):
        try:
            category_dao = CategoryDAO()
            category_vo = category_dao.edit_category(category_id)

            logger.info('edit category successfully : {}'.format(category_id))
            return category_vo
        except Exception as e:
            raise RuntimeError(f"Error in edit_category_service: {str(e)}")

    def update_category_service(self, category_id, category_dto_lst):
        """
        Service function to update a category.
        """
        try:
            create_at = get_current_timestamp()
            modify_at = get_current_timestamp()

            category_vo = CategoryVO()
            category_vo.category_id = category_id
            category_vo.category_name = category_dto_lst['category_name']
            category_vo.category_description = category_dto_lst['category_description']

            category_vo.create_at = create_at
            category_vo.modify_at = modify_at

            category_dao = CategoryDAO()
            updated_category = category_dao.update_category(
                category_id,
                category_vo.category_name,
                category_vo.category_description
            )
            logger.info(
                f'Update category successfully: ID -> {category_vo.category_id}, '
                f'Name -> {category_vo.category_name}, Description -> {category_vo.category_description}'
            )
            return updated_category
        except Exception as e:
            logger.error(f"Error in update_category_service: {str(e)}")
            raise RuntimeError(f"Error in update_category_service: {str(e)}")
