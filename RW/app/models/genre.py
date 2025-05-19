from app.extensions import db

class Genre(db.Model):
    __tablename__ = 'genres'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200), default='No description')

    # Связь
    objects = db.relationship(
        "Object",
        back_populates="genre",
        cascade="all, delete-orphan",
        passive_deletes=True
    )