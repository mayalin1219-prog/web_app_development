from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 實例
# 我們會在 app.py 中引入這個實例並與 Flask App 綁定：db.init_app(app)
db = SQLAlchemy()

# 將所有 models 在這裡一起 expose 出來
from .recipe import Recipe
from .ingredient import Ingredient, RecipeIngredient
from .tag import Tag, recipe_tags_assoc
