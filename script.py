import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import argparse
import os
from dotenv import load_dotenv

# Initialisation de Flask et SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle pour la table Email
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Email {self.address}>'

# Fonction pour envoyer un email
def envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients):
    try:
        # Configuration du serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Sécurise la connexion
        server.login(login, password)

        # Création de l'email
        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = login
            msg['To'] = recipient
            msg['Subject'] = subject

            # Corps du message
            msg.attach(MIMEText(body, 'plain'))

            # Envoi de l'email
            server.sendmail(login, recipient, msg.as_string())
            print(f"Email envoyé avec succès à {recipient}")

        # Fermeture de la connexion
        server.quit()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Fonction pour récupérer les emails de la base de données
def recuperer_emails():
    try:
        # Utiliser le contexte de l'application pour interagir avec la base de données
        with app.app_context():
            emails = Email.query.all()  # Récupère tous les emails dans la base de données
            return [email.address for email in emails]
    except Exception as e:
        print(f"Erreur lors de la récupération des emails : {e}")
        return []

# Lecture du contenu du fichier to_send.txt
def lire_contenu_fichier(fichier):
    try:
        with open(fichier, 'r') as file:
            return file.read()  # Retourne le contenu du fichier
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
        return ""

load_dotenv()

# Paramètres d'envoi
smtp_server = "smtp.gmail.com"  # Serveur SMTP de Gmail
smtp_port = 587  # Port SMTP
login = "arthurlouette12@gmail.com"  # Remplacez par votre adresse email
password = os.getenv('SMTP_PASSWORD')
subject = "Sujet de l'email"
body = lire_contenu_fichier("message.txt")

def main(subject):
    if subject:  # Vérifier si un sujet a été fourni
        recipients = recuperer_emails()  # Récupère les emails depuis la base de données

        if recipients:
            # Appel de la fonction pour envoyer l'email à tous les destinataires
            envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients)
        else:
            print("Aucun email à envoyer, la liste est vide.")
    else:
        print("Erreur : Aucun objet d'email fourni. L'envoi est annulé.")

# Utilisation d'argparse pour récupérer l'objet de l'email depuis la ligne de commande
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Envoyer des emails avec un objet spécifié.")
    parser.add_argument('subject', type=str, nargs='?', help="L'objet de l'email.")
    args = parser.parse_args()
    
    # Lancer l'envoi des emails si un objet est spécifié, sinon annuler
    main(args.subject)