from marshmallow import Schema, fields

class BlogSchema(Schema):
    id = fields.Int(dump_only=True)  # ID, seulement en mode lecture
    image = fields.Str(required=True)  # Chemin de l'image, requis
    title = fields.Str(required=True)  # Titre du blog, requis
    date = fields.DateTime(dump_only=True)  # Date, seulement en mode lecture
    summary = fields.Str(required=True)  # Résumé, requis
    description = fields.Str(required=True)  # Description, requis
