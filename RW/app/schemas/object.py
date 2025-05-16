from marshmallow import Schema, fields
from .genre import GenreSchema

class ObjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    year = fields.Int()
    description = fields.Str()
    genre_id = fields.Int(allow_none=True)
    genre = fields.Nested(GenreSchema, dump_only=True)