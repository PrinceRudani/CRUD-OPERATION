from typing import Optional


class SubcategoryDTO:
    def __init__(self, sub_category_name: Optional[str] = None,
                 sub_category_description: Optional[str] = None):
        self.sub_category_name = sub_category_name
        self.sub_category_description = sub_category_description

    def validate(self):
        if not self.sub_category_description or not self.sub_category_name:
            raise Exception(
                "subcategory_name and sub_category_description cannot be None or "
                "empty")
        return self

    def __repr__(self):
        return (f"SubcategoryDto(, subcategory_name={self.sub_category_name}, "
                f"subcategory_id={self.sub_category_description})")
