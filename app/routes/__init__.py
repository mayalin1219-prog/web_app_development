from flask import Blueprint

# 將會在此建立這兩個藍圖
# 我們會在 app.py 中註冊： 
# app.register_blueprint(main_bp)
# app.register_blueprint(recipes_bp, url_prefix='/recipes')

# 此處不直接實例化，由內部模組自行 expose
from .main import main_bp
from .recipes import recipes_bp
