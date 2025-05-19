from marshmallow import Schema, fields

class RatingSchema(Schema):
    object_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    rated_at = fields.DateTime(dump_only=True)
