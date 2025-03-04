from marshmallow import Schema, fields, validates, ValidationError
import re


class CategoryDTO(Schema):
    category_name = fields.Str(required=True, error_messages={
        "required": "Category Name is required."})
    category_description = fields.Str(required=True, error_messages={
        "required": "Category Description is required."})

    @validates('category_name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError(
                'Category name must be at least 3 characters long')
        if len(value) > 100:
            raise ValidationError('Category name cannot exceed 100 characters')
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValidationError(
                'Category name can only contain letters, numbers and spaces')

    @validates('category_description')
    def validate_description(self, value):
        if len(value) < 10:
            raise ValidationError(
                'Category description must be at least 10 characters long')
        if len(value) > 200:
            raise ValidationError(
                'Category description cannot exceed 200 characters')
        if not re.match(r'^[a-zA-Z\s.,!?]+$', value):
            raise ValidationError(
                'Category description can only contain letters, numbers, spaces and basic punctuation')
