from app.models import Object
from app.extensions import db
from app.schemas.object import ObjectSchema

def get_all_objects():
    objects = db.session.query(Object).all()
    return ObjectSchema(many=True).dump(objects)

def get_object_by_id(object_id: int):
    obj = db.session.get(Object, object_id)
    if not obj:
        return None
    return ObjectSchema().dump(obj)
