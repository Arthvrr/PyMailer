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

# Paramètres d'envoi
smtp_server = "smtp.gmail.com"  # Serveur SMTP de Gmail
smtp_port = 587  # Port SMTP
login = "arthurlouette12@gmail.com"  # Remplacez par votre adresse email
password = "ncyg pdoc ijcn ofod"
subject = "Sujet de l'email"
body = "Ceci est un email envoyé automatiquement."
recipients = ["arthurlouette14@gmail.com"]  # Liste de destinataires

# Appel de la fonction
envoyer_email(smtp_server, smtp_port, login, password, subject, body, recipients)