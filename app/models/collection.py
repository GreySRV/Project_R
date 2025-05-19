from app.extensions import db

class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(50), default='My Collection')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Связи
    client = db.relationship("Client", back_populates="collections")
    object_associations = db.relationship(
        "CollectionObject",
        back_populates="collection",
        cascade="all, delete-orphan",
        passive_deletes=True
    )