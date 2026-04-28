from flask import Blueprint, render_template, request, redirect, url_for

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/tags')
def list_tags():
    """
    顯示所有標籤列表與管理介面
    - 查詢所有標籤
    - 渲染 tags.html
    """
    pass

@tags_bp.route('/tags', methods=['POST'])
def create_tag():
    """
    建立新標籤
    - 接收表單欄位 `name`
    - 存入資料庫
    - 重導向至 /tags
    """
    pass

@tags_bp.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """
    刪除指定標籤
    - 根據 id 從資料庫移除標籤及其與食譜的關聯
    - 重導向至 /tags
    """
    pass
