# contact/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from contact.models import db, ContactMessage

# === Configuration ===
contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

MAX_SUBJECT_LEN = 255
MAX_EMAIL_LEN = 255
MAX_NAME_LEN = 120


# === Fonctions utilitaires ===
def _clean(s: str | None) -> str:
    """Nettoie une chaîne en supprimant espaces et None."""
    return (s or "").strip()

def _is_spam_honeypot(form) -> bool:
    """Détection simple anti-bot : champ 'company' doit rester vide."""
    return bool(_clean(form.get("company")))

def _valid_minimal_email(email: str) -> bool:
    """Validation très simple d'email (pas de regex lourde)."""
    return "@" in email and "." in email and len(email) <= MAX_EMAIL_LEN


# === Routes ===
@contact_bp.route("/", methods=["GET", "POST"], endpoint="form")
def contact_form():
    """Formulaire de contact simple avec validation et enregistrement en DB."""
    if request.method == "POST":
        # --- Anti-spam honeypot ---
        if _is_spam_honeypot(request.form):
            flash("Spam détecté. Message ignoré.", "warning")
            return redirect(url_for("contact.form"))

        # --- Nettoyage & extraction des champs ---
        subject = _clean(request.form.get("subject"))[:MAX_SUBJECT_LEN]
        message = _clean(request.form.get("message"))
        name    = _clean(request.form.get("name"))[:MAX_NAME_LEN]
        email   = _clean(request.form.get("email"))[:MAX_EMAIL_LEN]

        # --- Validation ---
        if not subject or not message:
            flash("Veuillez renseigner le sujet et le message.", "warning")
            return redirect(url_for("contact.form"))

        if not email:
            flash("Veuillez renseigner votre adresse email.", "warning")
            return redirect(url_for("contact.form"))

        if not _valid_minimal_email(email):
            flash("Adresse email invalide.", "warning")
            return redirect(url_for("contact.form"))

        # --- Enregistrement en base ---
        try:
            msg = ContactMessage(
                subject=subject,
                message=message,
                sender_name=name or None,
                sender_email=email,
            )
            db.session.add(msg)
            db.session.commit()
            flash("✅ Message envoyé avec succès. Réponse sous 24h ouvrées.", "success")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERREUR CONTACT] {e}")  # utile en debug
            flash("Une erreur est survenue lors de l’envoi. Réessayez plus tard.", "warning")

        return redirect(url_for("contact.form"))

    # --- Méthode GET ---
    return render_template("contact.html")


@contact_bp.route("/messages", endpoint="messages")
def list_messages():
    """Affiche la liste des messages reçus."""
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("messages.html", messages=msgs)