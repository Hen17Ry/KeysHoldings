from marshmallow import Schema, fields, validate
from datetime import datetime

class NewsletterSchema(Schema):
    id = fields.Integer(required=False)  # ID de la newsletter
    email = fields.Email(required=True, validate=validate.Email())  # Champ email valide et requis
    date = fields.DateTime(required=False, default=datetime.utcnow)  # Date et heure de l'inscription
