from flask import Blueprint, render_template, request, redirect, url_for, flash

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/recipes/new')
def new_recipe():
    """
    顯示新增食譜表單
    - 渲染 form.html
    """
    pass

@recipes_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    建立新食譜
    - 接收表單資料 (包含 title, steps, ingredients, tags, image)
    - 處理圖片上傳
    - 將資料存入資料庫
    - 成功後重導向至首頁或該食譜詳情頁
    """
    pass

@recipes_bp.route('/recipes/<int:id>')
def detail(id):
    """
    顯示單筆食譜詳情
    - 根據 id 查詢食譜及其關聯之食材與標籤
    - 渲染 detail.html
    """
    pass

@recipes_bp.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """
    顯示編輯食譜表單
    - 根據 id 查詢食譜資料並預先填入表單
    - 渲染 form.html
    """
    pass

@recipes_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    更新指定食譜
    - 接收表單資料
    - 處理圖片更新 (若有)
    - 更新資料庫紀錄
    - 成功後重導向至食譜詳情頁
    """
    pass

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜
    - 根據 id 從資料庫移除紀錄及其關聯
    - 刪除對應的圖片檔案
    - 成功後重導向至首頁
    """
    pass
