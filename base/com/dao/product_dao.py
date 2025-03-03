from base import db
from base.com.vo.category_vo import CategoryVO
from base.com.vo.product_vo import ProductVO
from base.com.vo.subcategory_vo import SubcategoryVO


class ProductDAO:
    """Data Access Object class for Product related database operations."""

    @staticmethod
    def ajax_product(sub_category_vo):
        """Get list of non-deleted subcategories for a given category ID."""
        sub_category_vo_lst = SubcategoryVO.query.filter_by(
            subcategory_category_id=sub_category_vo.subcategory_category_id).filter(
            SubcategoryVO.is_delete == False).all()
        return sub_category_vo_lst

    @staticmethod
    def insert_product(product_vo):
        """Add a new product to the database."""
        db.session.add(product_vo)
        db.session.commit()

    @staticmethod
    def view_product():
        """Get list of all non-deleted products with their category and subcategory info."""
        product_vo_lst = (
            db.session.query(ProductVO, SubcategoryVO, CategoryVO)
            .join(SubcategoryVO,
                  SubcategoryVO.sub_category_id == ProductVO.product_sub_category_id)
            .join(CategoryVO,
                  CategoryVO.category_id == ProductVO.product_category_id)
            .filter(CategoryVO.is_delete == False,
                    ProductVO.is_delete == False,
                    SubcategoryVO.is_delete == False).all())
        return product_vo_lst
