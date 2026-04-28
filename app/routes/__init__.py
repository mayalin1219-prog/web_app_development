# app/routes/__init__.py
# 初始化路由模組，此處可匯出各個 blueprints 以供 app.py 註冊

from .main import main_bp
from .recipes import recipes_bp
from .search import search_bp
from .tags import tags_bp
from .shopping_list import shopping_list_bp

def register_blueprints(app):
    """
    將所有 Blueprint 註冊至 Flask app
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(shopping_list_bp)
