import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.models import Recipe, Ingredient, RecipeIngredient, Tag

recipes_bp = Blueprint('recipes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@recipes_bp.route('/recipes/new')
def new_recipe():
    """
    顯示新增食譜表單
    - 渲染 form.html
    """
    return render_template('form.html', recipe=None)

@recipes_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    建立新食譜
    - 接收表單資料
    - 處理圖片上傳
    - 將資料存入資料庫
    - 成功後重導向至食譜詳情頁
    """
    title = request.form.get('title')
    steps = request.form.get('steps')
    description = request.form.get('description')
    
    # 輸入驗證
    if not title or not steps:
        flash("食譜名稱與步驟為必填欄位！", "danger")
        return redirect(url_for('recipes.new_recipe'))

    # 處理圖片上傳
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = filename

    try:
        recipe = Recipe.create(
            title=title,
            description=description,
            steps=steps,
            image_path=image_path
        )
        flash("食譜建立成功！", "success")
        return redirect(url_for('recipes.detail', id=recipe.id))
    except Exception as e:
        flash("建立食譜時發生錯誤，請稍後再試。", "danger")
        return redirect(url_for('recipes.new_recipe'))

@recipes_bp.route('/recipes/<int:id>')
def detail(id):
    """
    顯示單筆食譜詳情
    - 根據 id 查詢食譜
    - 渲染 detail.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜。", "warning")
        return redirect(url_for('main.index'))
    return render_template('detail.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """
    顯示編輯食譜表單
    - 根據 id 查詢食譜資料並預先填入表單
    - 渲染 form.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜。", "warning")
        return redirect(url_for('main.index'))
    return render_template('form.html', recipe=recipe)

@recipes_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    更新指定食譜
    - 接收表單資料
    - 處理圖片更新
    - 更新資料庫紀錄
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜。", "warning")
        return redirect(url_for('main.index'))

    title = request.form.get('title')
    steps = request.form.get('steps')
    description = request.form.get('description')

    if not title or not steps:
        flash("食譜名稱與步驟為必填欄位！", "danger")
        return redirect(url_for('recipes.edit_recipe', id=id))

    update_data = {
        'title': title,
        'steps': steps,
        'description': description
    }

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            update_data['image_path'] = filename

    try:
        recipe.update(**update_data)
        flash("食譜更新成功！", "success")
        return redirect(url_for('recipes.detail', id=recipe.id))
    except Exception as e:
        flash("更新食譜時發生錯誤。", "danger")
        return redirect(url_for('recipes.edit_recipe', id=id))

@recipes_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜
    - 根據 id 從資料庫移除紀錄
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash("找不到該食譜。", "warning")
        return redirect(url_for('main.index'))
        
    try:
        recipe.delete()
        flash("食譜已成功刪除。", "success")
    except Exception as e:
        flash("刪除食譜時發生錯誤。", "danger")
        
    return redirect(url_for('main.index'))
