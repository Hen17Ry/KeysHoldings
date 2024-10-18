from flask import render_template, request, jsonify, Blueprint, current_app, abort
from marshmallow import ValidationError
from datetime import datetime
from app.model.newletter import NewsletterSchema
from app.model.blog import BlogSchema
from firebase_admin import firestore

keys = Blueprint('main', __name__)

db = firestore.client()


@keys.route('/')
def index():
    return render_template('index.html')

@keys.route('/conn')
def connexion():
    return render_template('connexion.html')


@keys.route('/blog')
def blog():
    return render_template('blog.html')

@keys.route('/blog-details')
def blogdetails():
    return render_template('blog-details.html')

@keys.route('/portfolio-details')
def portfolio():
    return render_template('portfolio-details.html')

@keys.route('/service-details')
def service():
    return render_template('service-details.html')

@keys.route('/add-blog')
def addblog():
    return render_template('addblog.html')


@keys.route('/subscribe', methods=['POST'])
def subscribe():
    schema = NewsletterSchema()
    try:
        data = request.get_json(force=True)  # Force le traitement des données JSON
        print(data)  # Pour déboguer, vérifiez si les données sont reçues

        # Validation des données
        data = schema.load(data)

        # Ajout de la date actuelle
        data['date'] = datetime.now().isoformat()

        # Stockage dans Firestore
        db.collection('newsletters').add({
            'email': data['email'],
            'date': data['date']
        })

        return jsonify({"message": "Subscription successful!"}), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        print(str(e))  # Imprimez l'erreur pour le débogage
        return jsonify({"error": str(e)}), 500


@keys.route('/add_blog', methods=['POST'])
def add_blog():
    # Exemple de schéma, vous pouvez ajuster selon vos besoins
    schema = BlogSchema()

    try:
        # Charger et valider les données
        blog_data = schema.load(request.json)
        
        # Ajouter la date actuelle
        blog_data['date'] = datetime.now()

        # Ajouter le document dans Firestore
        db.collection('blogs').add(blog_data)  # 'blogs' est le nom de la collection
        
        # Répondre avec les données du blog créé
        return jsonify(blog_data), 201  # 201 pour Created

    except ValidationError as err:
        return jsonify(err.messages), 400  # 400 pour Bad Request
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 500 pour Internal Server Error
    
@keys.route('/get_blogs', methods=['GET'])
def get_blogs():
    # Récupérer toutes les entrées de la collection 'blogs'
    blogs_ref = db.collection('blogs')
    blogs = blogs_ref.stream()

    # Créer une liste pour stocker les données des blogs
    all_blogs = []
    
    # Extraire les données de chaque document
    for blog in blogs:
        blog_data = blog.to_dict()
        blog_data['id'] = blog.id  # Ajouter l'ID du document pour référence
        all_blogs.append(blog_data)

    # Retourner les données sous forme de JSON
    return jsonify(all_blogs)

@keys.route('/blog-details/<string:blog_id>', methods=['GET'])
def get_blog(blog_id):
    try:
        # Récupérer la référence au document du blog
        blog_ref = db.collection('blogs').document(blog_id)
        blog = blog_ref.get()
        
        # Vérifier si le blog existe
        if blog.exists:
            # Convertir les données du blog en dictionnaire et ajouter l'ID
            blog_data = blog.to_dict()
            blog_data['id'] = blog.id
            return jsonify(blog_data), 200
        else:
            return jsonify({'error': 'Blog non trouvé'}), 404
            
    except Exception as e:
        # Gérer les exceptions et renvoyer un message d'erreur
        print(f"Erreur: {e}")
        return jsonify({'error': 'Erreur lors de la récupération du blog'}), 500

@keys.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        # Rechercher l'admin dans Firestore
        admin_ref = db.collection('admin').where('email', '==', email).get()
        if not admin_ref:
            return jsonify({'error': 'Aucun compte trouvé avec cet email!'}), 404

        admin_data = admin_ref[0].to_dict()
        # Comparer le mot de passe
        if admin_data.get('password') == password:  # Vérifiez la façon dont vous stockez les mots de passe
            return jsonify({'message': 'Connexion réussie!'}), 200
        else:
            return jsonify({'error': 'Mot de passe incorrect!'}), 401

    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
        return jsonify({'error': 'Une erreur est survenue. Veuillez réessayer.'}), 500