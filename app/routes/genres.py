from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Genre
from app.schemas import GenreSchema
from app.utils.exceptions import APIError

genre_bp = Blueprint("genres", __name__)

@genre_bp.route("/", methods=["GET"])
def get_all_genres():
    genres = db.session.query(Genre).all()
    return GenreSchema(many=True).dump(genres)

@genre_bp.route("/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    genre = db.session.get(Genre, genre_id)
    if not genre:
        raise APIError("Genre not found", 404)
    return GenreSchema().dump(genre)

@genre_bp.route("/", methods=["POST"])
@jwt_required()
def create_genre():
    data = request.get_json()
    schema = GenreSchema()

    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), 400)

    genre = Genre(**validated)
    db.session.add(genre)
    db.session.commit()

    return schema.dump(genre), 201
