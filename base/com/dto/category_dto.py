from marshmallow import Schema, fields


class CategoryDTO(Schema):
    category_name = fields.Str(required=True,error_messages={"required":"Category Name is required."})
    category_description = fields.Str(required=True,error_messages={"required":"Category Description is required."})
