#MySQL password : Ubuntu120803

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import OperationalError
import pymysql

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('mysql+pymysql://Arthvrr:Ubuntu120803@Arthvrr.mysql.pythonanywhere-services.com/Arthvrr$default','sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Nécessaire pour utiliser flash() avec Flask

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Modèle de la base de données
class Email(db.Model):

    __tablename__ = 'email'  # Nom de la table dans la base de données

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Email {self.address}>'


@app.before_request
def check_db_connection():
    """Test de la connexion à la base de données avant chaque requête."""
    try:
        # Exécuter une requête simple pour tester la connexion à la base de données
        db.session.execute('SELECT 1')  # Cela renvoie 1 si la connexion fonctionne
    except OperationalError as e:
        # En cas d'erreur, on ferme et réinitialise la session
        db.session.remove()
        db.engine.dispose()
        flash(f"Erreur de connexion à la base de données : {e}. Veuillez réessayer.", "error")

# Route pour la page d'accueil (index)
@app.route('/')
def index():
    return render_template('index.html')  # Rendre le fichier index.html

# Route pour ajouter un email via un formulaire
@app.route('/add_email', methods=['POST'])
def add_email():
    email_address = request.form['email']
    if Email.query.filter_by(address=email_address).first():
        flash("Cet email existe déjà.", "error")  # Message d'erreur
        return redirect(url_for('index'))  # Rediriger vers la même page
    
    # Ajouter l'email dans la base de données
    new_email = Email(address=email_address)
    db.session.add(new_email)
    db.session.commit()

    flash("Email ajouté avec succès", "success")  # Message de succès
    return redirect(url_for('index'))  # Rediriger vers la même page

# Route pour supprimer un email
@app.route('/delete_email', methods=['POST'])
def delete_email():
    email_address = request.form['email']
    email_to_delete = Email.query.filter_by(address=email_address).first()
    
    if not email_to_delete:
        flash("Cet email n'existe pas dans le listing.", "error")  # Message d'erreur
        return redirect(url_for('index'))  # Rediriger vers la même page
    
    db.session.delete(email_to_delete)
    db.session.commit()
    
    flash("Email supprimé avec succès.", "success")  # Message de succès
    return redirect(url_for('index'))  # Rediriger vers la même page

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