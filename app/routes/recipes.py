from flask import Blueprint, request, render_template, redirect, url_for, flash
# from app.models import Recipe, Ingredient

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/create', methods=['GET', 'POST'])
def create():
    """
    HTTP Method: GET, POST
    GET: 呈現新增食譜表單。
    POST: 接收欄位 (title, steps, ingredients, image)，儲存至資料庫並重導向至首頁。
    渲染: recipes/create.html
    """
    pass

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    HTTP Method: GET
    顯示單一食譜的內容、圖片、所有必要食材。若 id 找不到則 404。
    渲染: recipes/detail.html
    """
    pass

@recipes_bp.route('/<int:recipe_id>/shopping-list', methods=['GET'])
def shopping_list(recipe_id):
    """
    HTTP Method: GET
    從食譜中提取需要的食材份數，幫助使用者列印或檢視採購清單。
    渲染: recipes/shopping_list.html
    """
    pass

@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit(recipe_id):
    """
    HTTP Method: GET
    提供表單給使用者修改先前的食譜內容。
    渲染: recipes/edit.html
    """
    pass

@recipes_bp.route('/<int:recipe_id>/update', methods=['POST'])
def update(recipe_id):
    """
    HTTP Method: POST
    接收來自編輯表單的資料，覆蓋掉原有的 Recipe Model 後儲存。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    """
    HTTP Method: POST
    從系統中刪除此食譜，結束後返回首頁。
    """
    pass
