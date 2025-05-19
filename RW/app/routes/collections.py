from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Collection, CollectionObject, Object
from app.schemas import CollectionSchema
from app.utils.exceptions import APIError
from sqlalchemy.exc import SQLAlchemyError # Временно

collection_bp = Blueprint("collections", __name__)

@collection_bp.route("/", methods=["GET"])
@jwt_required()
def get_collections():
    client_id = int(get_jwt_identity())
    collections = db.session.query(Collection).filter_by(client_id=client_id).all()
    return CollectionSchema(many=True).dump(collections)

@collection_bp.route("/", methods=["POST"])
@jwt_required()
def create_collection():
    data = request.get_json()
    name = data.get("name", "My Collection")

    client_id = int(get_jwt_identity())
    collection = Collection(name=name, client_id=client_id)

    db.session.add(collection)
    db.session.commit()

    return CollectionSchema().dump(collection), 201

@collection_bp.route("/<int:collection_id>", methods=["GET"])
@jwt_required()
def get_collection(collection_id):
    client_id = int(get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if not collection or collection.client_id != client_id:
        raise APIError("Collection not found", 404)

    return CollectionSchema().dump(collection)

@collection_bp.route("/<int:collection_id>/add", methods=["POST"])
@jwt_required()
def add_object_to_collection(collection_id):
    data = request.get_json()
    object_id = data.get("object_id")
    if not object_id:
        raise APIError("object_id is required", 400)

    client_id = int(get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if not collection or collection.client_id != client_id:
        raise APIError("Collection not found or access denied", 404)

    obj = db.session.get(Object, object_id)
    if not obj:
        raise APIError("Object not found", 404)

    # Проверка на дубликат
    existing = db.session.query(CollectionObject).filter_by(
        collection_id=collection_id, object_id=object_id
    ).first()

    if existing:
        raise APIError("Object already in collection", 400)

    link = CollectionObject(collection_id=collection_id, object_id=object_id)
    # db.session.add(link)
    # db.session.commit()
    try:
        db.session.add(link)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise APIError(f"DB error: {str(e)}", 500)

    return {"message": "Object added to collection"}, 201
    print(f"client_id={client_id}, collection_id={collection_id}, object_id={object_id}")


@collection_bp.route("/<int:collection_id>", methods=["DELETE"])
@jwt_required()
def delete_collection(collection_id):
    client_id = int(get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if not collection or collection.client_id != client_id:
        raise APIError("Collection not found or access denied", 404)

    db.session.delete(collection)
    db.session.commit()

    return {"message": "Collection deleted"}

@collection_bp.route("/<int:collection_id>/remove", methods=["DELETE"])
@jwt_required()
def remove_object_from_collection(collection_id):
    data = request.get_json()
    object_id = data.get("object_id")

    if not object_id:
        raise APIError("object_id is required", 400)

    client_id = int(get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if not collection or collection.client_id != client_id:
        raise APIError("Collection not found or access denied", 404)

    link = db.session.query(CollectionObject).filter_by(
        collection_id=collection_id,
        object_id=object_id
    ).first()

    if not link:
        raise APIError("Object not found in collection", 404)

    db.session.delete(link)
    db.session.commit()

    return {"message": "Object removed from collection"}

@collection_bp.route("/<int:collection_id>", methods=["PUT"])
@jwt_required()
def rename_collection(collection_id):
    data = request.get_json()
    new_name = data.get("name")

    if not new_name:
        raise APIError("New name is required", 400)

    client_id = int(get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if not collection or collection.client_id != client_id:
        raise APIError("Collection not found or access denied", 404)

    collection.name = new_name
    db.session.commit()

    return CollectionSchema().dump(collection)
