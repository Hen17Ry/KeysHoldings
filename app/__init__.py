import os
import firebase_admin
from firebase_admin import credentials
from flask import Flask
from dotenv import load_dotenv
import base64
import json

def create_app():
    app = Flask(__name__)

    # Charger les variables d'environnement
    load_dotenv()

    # Chemin ou contenu des credentials Firebase
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    firebase_credentials_base64 = os.getenv('FIREBASE_CREDENTIALS')

    if cred_path:
        # Utiliser le fichier JSON en local
        cred = credentials.Certificate(cred_path)
    elif firebase_credentials_base64:
        # Décoder la variable d'environnement encodée en base64 sur Vercel
        decoded_credentials = base64.b64decode(firebase_credentials_base64)
        cred_dict = json.loads(decoded_credentials)
        cred = credentials.Certificate(cred_dict)
    else:
        raise ValueError("Les informations d'identification Firebase ne sont pas définies")

    # Initialiser Firebase
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://keysholdings-6b588-default-rtdb.firebaseio.com/"
    })

    # Enregistrer les blueprints
    from app.routes import keys
    app.register_blueprint(keys)

    return app
