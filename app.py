from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///emails.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Nécessaire pour utiliser flash() avec Flask

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Initialisation de Flask-Migrate
migrate = Migrate(app, db)

# Modèle de la base de données
class Email(db.Model):

    __tablename__ = 'email'  # Nom de la table dans la base de données

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