from . import db

# Association Table for Many-to-Many relationship between Recipes and Tags
recipe_tags_assoc = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    recipes = db.relationship('Recipe', secondary=recipe_tags_assoc, back_populates='tags')

    @classmethod
    def get_or_create(cls, name):
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
        return tag

    @classmethod
    def get_all(cls):
        return cls.query.all()
