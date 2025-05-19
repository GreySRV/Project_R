from app.extensions import db

class Object(db.Model):
    __tablename__ = 'objects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id', ondelete="SET NULL"))

    # Связи
    genre = db.relationship("Genre", back_populates="objects")
    ratings = db.relationship(
        "Rating",
        back_populates="object",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    collection_associations = db.relationship(
        "CollectionObject",
        back_populates="object",
        cascade="all, delete-orphan",
        passive_deletes=True
    )