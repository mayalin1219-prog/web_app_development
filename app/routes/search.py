from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    """
    顯示搜尋與推薦頁面及結果
    - 接收 GET 參數: keyword (關鍵字), ingredients (食材清單)
    - 若有參數則進行資料庫查詢，回傳符合的食譜列表
    - 若無參數則僅顯示搜尋表單
    - 渲染 search.html
    """
    pass
