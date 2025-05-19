from app.models import Rating
from app.extensions import db
from sqlalchemy import func

def get_average_rating(object_id: int) -> float | None:
    result = db.session.query(func.avg(Rating.rating)).filter_by(object_id=object_id).scalar()
    return round(result, 2) if result else None

def get_user_rating(client_id: int, object_id: int) -> Rating | None:
    return db.session.query(Rating).filter_by(client_id=client_id, object_id=object_id).first()

def rate_object(client_id: int, object_id: int, rating_value: int):
    rating = get_user_rating(client_id, object_id)
    if rating:
        rating.rating = rating_value
    else:
        rating = Rating(client_id=client_id, object_id=object_id, rating=rating_value)
        db.session.add(rating)
    db.session.commit()
