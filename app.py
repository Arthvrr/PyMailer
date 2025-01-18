from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'  # Utilise SQLite pour une base de données simple
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Modèle de la base de données
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Email {self.address}>'

# Route pour la page d'accueil (index)
@app.route('/')
def index():
    return render_template('index.html')  # Rendre le fichier index.html

# Route pour ajouter un email via un formulaire
@app.route('/add_email', methods=['POST'])
def add_email():
    email_address = request.form['email']
    if Email.query.filter_by(address=email_address).first():
        return jsonify({"message": "Cet email existe déjà."}), 400  # Vérifier si l'email existe déjà dans la DB
    
    # Ajouter l'email dans la base de données
    new_email = Email(address=email_address)
    db.session.add(new_email)
    db.session.commit()

    return jsonify({"message": "Email ajouté avec succès"}), 200

# Route pour afficher tous les emails (facultatif)
@app.route('/emails', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    return jsonify([email.address for email in emails])

# Route pour supprimer un email
@app.route('/delete_email', methods=['POST'])
def delete_email():
    email_address = request.form['email']
    email_to_delete = Email.query.filter_by(address=email_address).first()
    
    if not email_to_delete:
        return jsonify({"message": "Cet email n'existe pas dans le listing."}), 404  # Email non trouvé
    
    db.session.delete(email_to_delete)
    db.session.commit()
    
    return jsonify({"message": "Email supprimé avec succès."}), 200

if __name__ == '__main__':
    with app.app_context():
        try:
            # Créer la base de données si elle n'existe pas
            db.create_all()
            print("Base de données créée avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création de la base de données : {e}")

    # Démarrer l'application Flask
    app.run(debug=True)