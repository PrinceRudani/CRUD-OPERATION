from flask import render_template, request, redirect, session

from base import app
from base.com.dto.category_dto import CategoryDTO
from base.com.service.category_service import CategoryService
from base.com.service.login_service import LoginService
from base.utils import my_logger

logger = my_logger.get_logger()


@app.route('/load_category')
def load_category():
    """load category"""
    try:
        user_name = session.get('user_name', 'Guest')
        logger.info('load category successfully')
        return render_template("category_templates/addCategory.html",
                               user_name=user_name)
    except Exception as e:
        logger.error(f'Error loading category: {e}')
        return render_template("category_templates/addCategory.html",
                               errors=str(e))

@app.route('/insert_category', methods=['POST', 'GET'])
@LoginService.login_required(role="ADMIN")
def insert_category():

    try:
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName').strip() or None,
            'category_description': request.form.get('categoryDescription').strip() or None
        }
        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.add_category_service(category_dto_lst)
        logger.info(
            f'Category inserted successfully: Name -> {category_dto_lst["category_name"]},'
            f' Description -> {category_dto_lst["category_description"]}')
        return redirect('/view_category')

    except Exception as e:
        logger.error(f'Error inserting category: {str(e)}')
        return render_template('category_templates/addCategory.html',
                               errors="Any field can not be empty.")


@app.route('/view_category', methods=['POST', 'GET'])
@LoginService.login_required(role="ADMIN")
def view_category():
    """view category with error hand"""
    try:
        category_service = CategoryService()
        category_dto_lst = category_service.view_category_service()
        logger.info(f'view category : {category_dto_lst}')
        return render_template('category_templates/viewCategory.html',
                               category_dto_lst=category_dto_lst)
    except Exception as e:
        logger.error(f"Error viewing categories: {e}")
        return render_template('category_templates/viewCategory.html')


@app.route('/delete_category', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def delete_category():
    """delete category"""
    try:
        category_id = request.form.get('category_id')
        category_service = CategoryService()
        category_service.delete_category_service(category_id)
        return redirect('/view_category')
    except Exception as e:
        logger.error(f'Error deleting category: {e}')
        return render_template('category_templates/viewCategory.html')


@app.route('/edit_category', methods=['GET'])
@LoginService.login_required(role="ADMIN")
def edit_category():
    try:
        category_id = request.args.get('category_id')
        category_service = CategoryService()
        category = category_service.edit_category_service(category_id)
        return render_template('category_templates/updateCategory.html',
                               category=category)
    except Exception as e:
        logger.error(f'Error editing category: {e}')
        return render_template('category_templates/viewCategory.html')


@app.route('/update_category', methods=['POST'])
@LoginService.login_required(role="ADMIN")
def update_category():
    category_id = None
    try:
        category_id = int(request.form.get('category_id'))
        category_dto = CategoryDTO()
        data = {
            'category_name': request.form.get('categoryName'),
            'category_description': request.form.get('categoryDescription')
        }
        category_dto_lst = category_dto.load(data)
        category_service = CategoryService()
        category_service.update_category_service(category_id, category_dto_lst)
        return redirect('/view_category')

    except Exception as e:
        logger.error(f'Error updating category: {str(e)}')
        return redirect(
            f'/edit_category?category_id={category_id or "error"}&error={str(e)}')
