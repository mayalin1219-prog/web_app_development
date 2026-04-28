from flask import Blueprint, render_template, request, session, redirect, url_for

shopping_list_bp = Blueprint('shopping_list', __name__)

@shopping_list_bp.route('/shopping-list')
def view_list():
    """
    顯示採購清單
    - 從 session 或資料庫中取得已選定的待煮食譜
    - 彙總這些食譜所需的食材與數量
    - 渲染 shopping_list.html
    """
    pass

@shopping_list_bp.route('/shopping-list/add', methods=['POST'])
def add_to_list():
    """
    將食譜加入待煮清單 (以供生成採購清單)
    - 接收 recipe_id
    - 將紀錄存入 session 或使用者的暫存表
    - 重導向回原頁面或採購清單頁
    """
    pass
