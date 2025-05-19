from marshmallow import Schema, fields
from .object import ObjectSchema

class CollectionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    # вложенные объекты (только на чтение)
    objects = fields.Nested(ObjectSchema, many=True, dump_only=True)
