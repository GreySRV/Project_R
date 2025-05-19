from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Object
from app.models import Genre
from app.schemas import ObjectSchema
from app.utils.exceptions import APIError

object_bp = Blueprint("objects", __name__)

@object_bp.route("/", methods=["GET"])
def get_all_objects():
    query = db.session.query(Object)

    year = request.args.get("year")
    genre_id = request.args.get("genre_id")

    if year:
        query = query.filter_by(year=year)
    if genre_id:
        query = query.filter_by(genre_id=genre_id)

    objects = query.all()
    return ObjectSchema(many=True).dump(objects)

@object_bp.route("/<int:object_id>", methods=["GET"])
def get_object(object_id):
    obj = db.session.get(Object, object_id)
    if not obj:
        raise APIError("Object not found", 404)
    return ObjectSchema().dump(obj)

@object_bp.route("/", methods=["POST"])
@jwt_required()
def create_object():
    data = request.get_json()
    schema = ObjectSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), 400)

    obj = Object(**validated)
    db.session.add(obj)
    db.session.commit()
    return schema.dump(obj), 201

@object_bp.route("/genre/<int:genre_id>", methods=["GET"])
def get_objects_by_genre(genre_id):
    genre = db.session.get(Genre, genre_id)
    if not genre:
        raise APIError("Genre not found", 404)

    objects = db.session.query(Object).filter_by(genre_id=genre_id).all()
    return ObjectSchema(many=True).dump(objects)
