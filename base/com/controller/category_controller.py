from flask import render_template, request, redirect, session
from base import app
from base.com.dto.category_dto import CategoryDTO
from base.com.service.category_service import CategoryService
from base.com.service.login_service import LoginService, static_variables
from base.utils import my_logger
from base.utils.http_exception import BaseCusException

logger = my_logger.get_logger()


@app.route('/load_category')
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def load_category():
    """
    Load category page for adding new category.
    
    Returns:
        str: Rendered HTML template for adding category.
            On success: Returns addCategory.html template with user_name.
            On error: Returns addCategory.html template with error message.
    """
    try:
        user_name = session.get('user_name', 'Guest')
        logger.info('Load category successfully')
        return render_template("category_templates/addCategory.html",
                               user_name=user_name)
    except BaseCusException as e:
        logger.error(f'Error loading category: {e}')
        return render_template("category_templates/addCategory.html",
                               errors=e.get_flash_message())


@app.route('/insert_category', methods=['POST', 'GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def insert_category():
    """
    Insert a new category into the system.
    
    Takes category name and description from form data, validates them,
    and inserts into database through service layer.
    
    Returns:
        str: On success, redirects to view_category page.
             On error, returns addCategory template with error message.
             
    Raises:
        BaseCusException: If category name or description is empty.
    """
    try:
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName').strip() or None,
            'category_description': request.form.get(
                'categoryDescription').strip() or None
        }
        if not data['category_name'] or not data['category_description']:
            # Raise custom exception if fields are empty
            raise BaseCusException(
                "Category name or description cannot be empty", 400,
                "Please fill in both fields.")

        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.add_category_service(category_dto_lst)
        logger.info(
            f'Category inserted successfully: Name -> {category_dto_lst["category_name"]}, Description -> {category_dto_lst["category_description"]}')
        return redirect('/view_category')

    except BaseCusException as e:
        # Only catch the BaseCusException here and show user-facing error message
        logger.error(f'Error inserting category: {str(e)}')
        return render_template('category_templates/addCategory.html',
                               errors=e.get_flash_message())


@app.route('/view_category', methods=['POST', 'GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def view_category():
    """
    Display all categories in the system.
    
    Retrieves all non-deleted categories from database and displays them.
    
    Returns:
        str: Rendered HTML template with list of categories.
             On error, returns template with error message.
    """
    try:
        category_service = CategoryService()
        category_dto_lst = category_service.view_category_service()
        logger.info(f'View category: {category_dto_lst}')
        return render_template('category_templates/viewCategory.html',
                               category_dto_lst=category_dto_lst)

    except BaseCusException as e:
        logger.error(f"Error viewing categories: {e}")
        return render_template('category_templates/viewCategory.html',
                               errors=e.get_flash_message())


@app.route('/delete_category', methods=['POST'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def delete_category():
    """
    Soft delete a category from the system.
    
    Takes category_id from form data and marks the category as deleted.
    
    Returns:
        str: On success, redirects to view_category page.
             On error, returns viewCategory template with error message.
    """
    try:
        category_id = request.form.get('category_id')
        category_service = CategoryService()
        category_service.delete_category_service(category_id)
        return redirect('/view_category')

    except BaseCusException as e:
        logger.error(f"Error deleting category: {e}")
        return render_template('category_templates/viewCategory.html',
                               errors=e.get_flash_message())


@app.route('/edit_category', methods=['GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def edit_category():
    """
    Load category edit form.
    
    Takes category_id from query parameters and loads category data
    into edit form.
    
    Returns:
        str: Rendered HTML template for updating category.
             On error, returns viewCategory template with error message.
    """
    try:
        category_id = request.args.get('category_id')
        category_service = CategoryService()
        category = category_service.edit_category_service(category_id)
        return render_template('category_templates/updateCategory.html',
                               category=category)

    except BaseCusException as e:
        logger.error(f"Error editing category: {e}")
        return render_template('category_templates/viewCategory.html',
                               errors=e.get_flash_message())


@app.route('/update_category', methods=['POST'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def update_category():
    """
    Update an existing category.
    
    Takes category_id, name and description from form data,
    validates them and updates the category in database.
    
    Returns:
        str: On success, redirects to view_category page.
             On error, redirects back to edit form with error message.
             
    Raises:
        BaseCusException: If category name or description is empty.
    """
    category_id = None
    try:
        category_id = int(request.form.get('category_id'))
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName'),
            'category_description': request.form.get('categoryDescription')
        }

        if not data['category_name'] or not data['category_description']:
            # Raise custom exception if fields are empty
            raise BaseCusException(
                "Category name or description cannot be empty", 400,
                "Please fill in both fields.")

        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.update_category_service(category_id, category_dto_lst)
        return redirect('/view_category')

    except BaseCusException as e:
        logger.error(f'Error updating category: {str(e)}')
        return redirect(
            f'/edit_category?category_id={category_id or "error"}&error={e.get_flash_message()}')
