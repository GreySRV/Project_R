from app.extensions import db

class CollectionObject(db.Model):
    __tablename__ = 'collection_objects'
    
    collection_id = db.Column(
        db.Integer, 
        db.ForeignKey('collections.id', ondelete="CASCADE"), 
        primary_key=True
    )
    object_id = db.Column(
        db.Integer, 
        db.ForeignKey('objects.id', ondelete="CASCADE"), 
        primary_key=True
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Связи
    collection = db.relationship(
        "Collection", 
        back_populates="object_associations"
    )
    object = db.relationship(
        "Object", 
        back_populates="collection_associations"
    )