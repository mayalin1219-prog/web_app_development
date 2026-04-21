from flask import Blueprint, request, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP Method: GET
    顯示首頁，依照最新建立時間列出所有的食譜。
    渲染: index.html
    """
    pass

@main_bp.route('/search')
def search():
    """
    HTTP Method: GET
    處理搜尋邏輯，參數可包含 `q` (菜名關鍵字) 或 `ingredients` (手邊有的食材用以做推薦)。
    渲染: search.html
    """
    pass
