from app.extensions import db

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    client_id = db.Column(
        db.Integer, 
        db.ForeignKey('clients.id', ondelete="CASCADE"), 
        primary_key=True
    )
    object_id = db.Column(
        db.Integer, 
        db.ForeignKey('objects.id', ondelete="CASCADE"), 
        primary_key=True
    )
    rating = db.Column(db.Integer)
    rated_at = db.Column(db.DateTime, server_default=db.func.now())

    # Связи
    client = db.relationship(
        "Client", 
        back_populates="ratings"
    )
    object = db.relationship(
        "Object", 
        back_populates="ratings"
    )

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 10', name='check_rating_range'),
    )