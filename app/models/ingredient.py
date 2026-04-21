from . import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationships
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient', cascade="all, delete-orphan")

    @classmethod
    def get_or_create(cls, name):
        ingredient = cls.query.filter_by(name=name).first()
        if not ingredient:
            ingredient = cls(name=name)
            db.session.add(ingredient)
            db.session.commit()
        return ingredient


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), nullable=False)
    
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(50), nullable=True)
    
    # Relationships
    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')

    @classmethod
    def add_to_recipe(cls, recipe_id, ingredient_name, quantity=None, unit=None):
        ingredient = Ingredient.get_or_create(ingredient_name)
        assoc = cls(recipe_id=recipe_id, ingredient_id=ingredient.id, quantity=quantity, unit=unit)
        db.session.add(assoc)
        db.session.commit()
        return assoc
