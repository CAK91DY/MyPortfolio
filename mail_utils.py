# mail_utils.py
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# Récupération des variables depuis .env
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_contact_email(name, reply_to, subject, message):
    """
    Envoie un email via Gmail SMTP (avec mot de passe d'application).
    """
    try:
        # Construction du message
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # tu peux mettre une autre adresse si tu veux recevoir ailleurs
        msg["Subject"] = f"[Portfolio] {subject}"
        msg["Reply-To"] = reply_to

        # Contenu texte
        msg.set_content(f"""
        Nouveau message depuis le formulaire de contact :
        
        Nom : {name}
        Email : {reply_to}
        Sujet : {subject}

        Message :
        {message}
        """)

        # Contenu HTML
        msg.add_alternative(f"""
        <h2>Nouveau message depuis ton portfolio</h2>
        <p><strong>Nom :</strong> {name}<br>
        <strong>Email :</strong> {reply_to}<br>
        <strong>Objet :</strong> {subject}</p>
        <p>{message.replace(chr(10), '<br>')}</p>
        """, subtype="html")

        # Connexion au serveur Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()  # sécurise la connexion
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email envoyé avec succès via Gmail")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du mail : {e}")
        return False