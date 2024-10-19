import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Charger les variables d'environnement
    load_dotenv()

    # Charger le chemin du fichier d'identification Firebase depuis les variables d'environnement
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Vérifiez que le chemin est défini
    if not cred_path:
        raise ValueError("Le chemin du fichier d'identification Firebase n'est pas défini dans les variables d'environnement")

    # Charger les credentials Firebase à partir du fichier JSON
    cred = credentials.Certificate(cred_path)

    # Initialiser Firebase avec les bonnes credentials
    firebase_admin.initialize_app(cred, {"databaseURL": "https://keysholdings-6b588-default-rtdb.firebaseio.com/"
    })

    # Enregistrer les blueprints
    from app.routes import keys
    app.register_blueprint(keys)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
