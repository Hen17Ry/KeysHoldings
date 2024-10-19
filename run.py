from app import create_app
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir de .env
load_dotenv()

# Créer l'application Flask
app = create_app()

if __name__ == "__main__":
    app.run()
