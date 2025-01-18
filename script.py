import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Lecture du contenu du fichier to_send.txt
def lire_contenu_fichier(fichier):
    try:
        with open(fichier, 'r') as file:
            return file.read()  # Retourne le contenu du fichier
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
        return ""

recipients = []
# Lecture des adresses emails depuis emails.txt et ajout dans la liste recipients
def lire_emails(fichier):
    try:
        with open(fichier, 'r') as file:
            # Ajoute chaque email dans la liste recipients
            for email in file.readlines():
                recipients.append(email.strip())  # Enlever les espaces blancs et les sauts de ligne
    except Exception as e:
        print(f"Erreur lors de la lecture des emails depuis {fichier}: {e}")


# Paramètres d'envoi
smtp_server = "smtp.gmail.com"  # Serveur SMTP de Gmail
smtp_port = 587  # Port SMTP
login = "arthurlouette12@gmail.com"  # Remplacez par votre adresse email
password = "ncyg pdoc ijcn ofod"
subject = "Sujet de l'email"
body = lire_contenu_fichier("to_send.txt")
lire_emails('emails.txt')


def main():
    if recipients:
        # Appel de la fonction pour envoyer l'email à tous les destinataires
        envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients)
    else:
        print("Aucun email à envoyer, la liste est vide.")