# app.py
from flask import (
    Flask, render_template, session, Blueprint,
    request, redirect, url_for, flash, current_app
)
from flask_babel import Babel, get_locale, _
from urllib.parse import urlparse
from config import Config
from mail_utils import send_contact_email
# from auth import auth_bp   # ← décommente si tu utilises vraiment ce blueprint

# ------------------ Extensions ------------------
babel = Babel()

# ------------------ Blueprint "pages" ------------------
pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/", endpoint="index")
def index():
    return render_template("index.html")

@pages_bp.route("/projets", endpoint="projets")
def projets():
    return render_template("projets.html")

@pages_bp.route("/competences", endpoint="competences")
def competences():
    return render_template("competences.html")

@pages_bp.route("/experiences", endpoint="experiences")
def experiences():
    return render_template("experiences.html")

# ---------- CONTACT ----------
@pages_bp.get("/contact", endpoint="contact")
def contact():
    return render_template("contact.html")

@pages_bp.post("/contact/submit", endpoint="contact_submit")
def contact_submit():
    # Honeypot anti-spam
    if (request.form.get("company") or "").strip():
        flash(_("Votre message n’a pas été envoyé (filtre anti-spam)."), "error")
        return redirect(url_for("pages.contact"))

    name    = (request.form.get("name") or "").strip()
    email   = (request.form.get("email") or "").strip()
    subject = (request.form.get("subject") or "").strip()
    message = (request.form.get("message") or "").strip()
    consent = request.form.get("consent")

    if not all([name, email, subject, message, consent]):
        flash(_("Merci de remplir tous les champs requis."), "error")
        return redirect(url_for("pages.contact"))

    # Envoi via l’API Brevo (mail_utils)
    ok = send_contact_email(name, email, subject, message)
    if ok:
        flash(_("Merci ! Votre message a bien été envoyé."), "success")
    else:
        flash(_("Une erreur est survenue lors de l’envoi de votre message."), "error")

    current_app.logger.info("Contact form: %s <%s> — %s\n%s", name, email, subject, message)
    return redirect(url_for("pages.contact"))

# ---------- LANG SWITCH (fonction commune) ----------
def _do_set_lang(lang: str):
    """
    Change la langue ('fr' ou 'en'), puis redirige vers la page d'origine.
    Cette fonction est utilisée par 2 endpoints alias : set_lang et set_language.
    """
    lang = (lang or "").lower()
    if lang in ("fr", "en"):
        session["lang"] = lang

    # Sécurise la redirection
    nxt = request.args.get("next") or request.referrer or url_for("pages.index")
    try:
        parsed = urlparse(nxt)
        # n'autorise que les redirections internes
        if parsed.netloc or not nxt.startswith(("/", "?")):
            nxt = url_for("pages.index")
    except Exception:
        nxt = url_for("pages.index")

    return redirect(nxt)

# Endpoint “officiel”
@pages_bp.route("/lang/<lang>", endpoint="set_lang")
def set_lang(lang: str):
    return _do_set_lang(lang)

# Alias pour compatibilité avec tes templates existants
@pages_bp.route("/language/<lang>", endpoint="set_language")
def set_language(lang: str):
    return _do_set_lang(lang)

# ------------------ App factory ------------------
def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Valeurs par défaut utiles à Babel
    app.config.setdefault("BABEL_DEFAULT_LOCALE", "fr")
    app.config.setdefault("BABEL_DEFAULT_TIMEZONE", "Europe/Paris")
    app.config.setdefault("BABEL_TRANSLATION_DIRECTORIES", "translations")

    # Clé secrète pour flash / sessions (mets-la dans Config/.env en prod)
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-change-me"

    # --- Fonction de sélection de locale (session > header navigateur > fr) ---
    def select_locale():
        lang = session.get("lang")
        if lang in ("fr", "en"):
            return lang
        return request.accept_languages.best_match(["fr", "en"]) or "fr"

    # Flask-Babel v4 : on passe locale_selector ici
    babel.init_app(app, locale_selector=select_locale)

    # Variables globales Jinja
    @app.context_processor
    def inject_globals():
        return {
            "user": session.get("user"),
            "ep": (request.endpoint or ""),
            # expose get_locale() pour <html lang="{{ get_locale() }}">
            "get_locale": lambda: str(get_locale()),
        }

    # Enregistre les blueprints nécessaires
    # app.register_blueprint(auth_bp)   # si tu l’utilises
    app.register_blueprint(pages_bp)

    @app.errorhandler(404)
    def not_found(e):
        try:
            return render_template("404.html"), 404
        except Exception:
            return _("Page non trouvée"), 404

    @app.errorhandler(500)
    def server_error(e):
        current_app.logger.exception("Erreur serveur")
        return _("Une erreur interne est survenue."), 500

    return app

# ------------------ Entrypoint ------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)