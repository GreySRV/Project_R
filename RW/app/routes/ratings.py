from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Rating, Object
from app.schemas import RatingSchema
from app.utils.exceptions import APIError

rating_bp = Blueprint("ratings", __name__)

@rating_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_ratings():
    client_id = int(get_jwt_identity())
    ratings = db.session.query(Rating).filter_by(client_id=client_id).all()
    return RatingSchema(many=True).dump(ratings)

@rating_bp.route("/", methods=["POST"])
@jwt_required()
def rate_object():
    client_id = int(get_jwt_identity())
    data = request.get_json()

    schema = RatingSchema()
    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), 400)

    object_id = validated["object_id"]
    rating_value = validated["rating"]

    if rating_value < 1 or rating_value > 10:
        raise APIError("Rating must be between 1 and 10", 400)

    obj = db.session.get(Object, object_id)
    if not obj:
        raise APIError("Object not found", 404)

    # Проверка: существует ли рейтинг
    rating = db.session.query(Rating).filter_by(
        client_id=client_id, object_id=object_id
    ).first()

    if rating:
        rating.rating = rating_value
    else:
        rating = Rating(client_id=client_id, object_id=object_id, rating=rating_value)
        db.session.add(rating)

    db.session.commit()
    return schema.dump(rating), 201

@rating_bp.route("/<int:object_id>", methods=["DELETE"])
@jwt_required()
def delete_rating(object_id):
    client_id = int(get_jwt_identity())

    rating = db.session.query(Rating).filter_by(
        client_id=client_id, object_id=object_id
    ).first()

    if not rating:
        raise APIError("Rating not found", 404)

    db.session.delete(rating)
    db.session.commit()
    return {"message": "Rating deleted"}
