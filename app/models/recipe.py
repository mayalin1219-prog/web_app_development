from datetime import datetime
from . import db
from .tag import recipe_tags_assoc

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    
    # Relationships
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary=recipe_tags_assoc, back_populates='recipes')

    @classmethod
    def create(cls, title, steps, description=None, image_path=None):
        recipe = cls(title=title, steps=steps, description=description, image_path=image_path)
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
