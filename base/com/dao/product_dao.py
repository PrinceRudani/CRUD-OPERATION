from base import db
from base.com.vo.category_vo import CategoryVO
from base.com.vo.product_vo import ProductVO
from base.com.vo.subcategory_vo import SubcategoryVO


class ProductDAO:
    @staticmethod
    def ajax_product(sub_category_vo):
        sub_category_vo_lst = SubcategoryVO.query.filter_by(
            subcategory_category_id=sub_category_vo.subcategory_category_id).filter(
            SubcategoryVO.is_delete == False).all()
        return sub_category_vo_lst

    @staticmethod
    def insert_product(product_vo):
        db.session.add(product_vo)
        db.session.commit()

    @staticmethod
    def view_product():
        product_vo_lst = (
            db.session.query(ProductVO, SubcategoryVO, CategoryVO)
            .join(SubcategoryVO,
                  SubcategoryVO.sub_category_id == ProductVO.product_sub_category_id)
            .join(CategoryVO,
                  CategoryVO.category_id == ProductVO.product_category_id)
            .filter(CategoryVO.is_delete == False,
                    ProductVO.is_delete == False,
                    SubcategoryVO.is_delete == False)
            .all()
        )
        return product_vo_lst

    @staticmethod
    def delete_product(product_id):
        product_vo = db.session.query(ProductVO).get(product_id)
        product_vo.is_delete = True
        db.session.commit()

    @staticmethod
    def edit_product(product_id):
        product_vo_lst = db.session.query(ProductVO).filter_by(
            product_id=product_id).first()
        sub_category_vo_lst = db.session.query(SubcategoryVO).all()
        category_vo_lst = db.session.query(CategoryVO).all()

        return product_vo_lst, category_vo_lst, sub_category_vo_lst

    @staticmethod
    def update_product(product_vo):
        db.session.merge(product_vo)
        db.session.commit()

    @staticmethod
    def product_name_from_product_id(product_id):
        return db.session.query(ProductVO).filter_by(
            product_id=product_id).first()
