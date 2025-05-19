from app.extensions import db
from app.models import Collection, CollectionObject
from app.models import CollectionObject, Object

def get_collections_by_user(client_id: int):
    return db.session.query(Collection).filter_by(client_id=client_id).all()

def create_collection(client_id: int, name: str):
    collection = Collection(name=name, client_id=client_id)
    db.session.add(collection)
    db.session.commit()
    return collection

def add_object_to_collection(collection_id: int, object_id: int):
    association = CollectionObject(collection_id=collection_id, object_id=object_id)
    db.session.add(association)
    db.session.commit()

def get_collection_ids_with_object(client_id: int, object_id: int) -> list[int]:
    results = db.session.query(CollectionObject.collection_id).join(Collection).filter(
        Collection.client_id == client_id,
        CollectionObject.object_id == object_id
    ).all()
    return [row[0] for row in results]

def get_collection_by_id(collection_id: int) -> Collection | None:
    return db.session.query(Collection).get(collection_id)

def get_objects_in_collection(collection_id: int):
    return db.session.query(Object).join(CollectionObject).filter(
        CollectionObject.collection_id == collection_id
    ).all()

def remove_object_from_collection(collection_id: int, object_id: int):
    association = db.session.query(CollectionObject).filter_by(
        collection_id=collection_id,
        object_id=object_id
    ).first()
    if association:
        db.session.delete(association)
        db.session.commit()
