from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    處理首頁 (食譜列表)
    - 取得所有食譜資料 (支援分頁)
    - 渲染 index.html
    """
    pass
