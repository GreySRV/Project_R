from marshmallow import Schema, fields

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    login = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
