# app.py
from flask import (
    Flask, render_template, session, Blueprint,
    request, redirect, url_for, flash, current_app, abort
)
from flask_babel import Babel, get_locale, _
from urllib.parse import urlparse
from functools import wraps
from sqlalchemy import text
from config import Config
from db import init_db, save_contact_message, engine  # ← on récupère aussi engine
import math
from sqlalchemy import text
from db import engine

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
    """Enregistre le message de contact dans PostgreSQL."""
    # --- Anti-spam (honeypot) ---
    if (request.form.get("company") or "").strip():
        flash(_("Votre message n’a pas été envoyé (filtre anti-spam)."), "error")
        return redirect(url_for("pages.contact"))

    # --- Champs du formulaire ---
    name    = (request.form.get("name") or "").strip()
    email   = (request.form.get("email") or "").strip()
    subject = (request.form.get("subject") or "").strip()
    message = (request.form.get("message") or "").strip()
    consent = bool(request.form.get("consent"))

    # --- Validation ---
    if not all([name, email, subject, message, consent]):
        flash(_("Merci de remplir tous les champs requis."), "error")
        return redirect(url_for("pages.contact"))

    # --- Sauvegarde en base Postgres ---
    saved = save_contact_message(name, email, subject, message, consent)
    if saved:
        flash(_("Merci ! Votre message a bien été enregistré."), "success")
    else:
        flash(_("Votre message n'a pas pu être enregistré."), "error")

    # --- Log interne ---
    current_app.logger.info(
        "Contact form: %s <%s> — %s\n%s", name, email, subject, message
    )
    return redirect(url_for("pages.contact"))


# ---------- LANG SWITCH ----------
def _do_set_lang(lang: str):
    """Change la langue ('fr' ou 'en'), puis redirige vers la page d'origine."""
    lang = (lang or "").lower()
    if lang in ("fr", "en"):
        session["lang"] = lang

    nxt = request.args.get("next") or request.referrer or url_for("pages.index")
    try:
        parsed = urlparse(nxt)
        if parsed.netloc or not nxt.startswith(("/", "?")):
            nxt = url_for("pages.index")
    except Exception:
        nxt = url_for("pages.index")

    return redirect(nxt)

@pages_bp.route("/lang/<lang>", endpoint="set_lang")
def set_lang(lang: str):
    return _do_set_lang(lang)

@pages_bp.route("/language/<lang>", endpoint="set_language")
def set_language(lang: str):
    return _do_set_lang(lang)


# ------------------ Blueprint "admin" ------------------
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    """Décorateur pour protéger les routes admin par session."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_auth"):
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Page de login simple.
    Utilise Config.ADMIN_USER et Config.ADMIN_PASSWORD depuis les variables d'env.
    """
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        if username == Config.ADMIN_USER and password == Config.ADMIN_PASSWORD:
            session["admin_auth"] = True
            flash(_("Connexion réussie."), "success")
            nxt = request.args.get("next") or url_for("admin.messages")
            return redirect(nxt)

        flash(_("Identifiants invalides."), "error")

    return render_template("admin_login.html")
    

@admin_bp.route("/logout")
@admin_required
def logout():
    session.pop("admin_auth", None)
    flash(_("Déconnexion effectuée."), "info")
    return redirect(url_for("admin.login"))

@admin_bp.route("/messages")
@admin_required
def messages():
    # paramètres de pagination
    page = max(1, int(request.args.get("page", 1)))
    per = max(1, min(100, int(request.args.get("per", 20))))
    offset = (page - 1) * per

    # total des lignes
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM contact_messages")).scalar() or 0
        last_page = max(1, math.ceil(total / per)) if total else 1

        # si page > last_page, on revient sur la dernière existante
        if page > last_page:
            return redirect(url_for("admin.messages", page=last_page, per=per))

        rows = conn.execute(
            text("""
                SELECT id, name, email, subject, message, created_at
                FROM contact_messages
                ORDER BY created_at DESC
                LIMIT :limit OFFSET :offset
            """),
            {"limit": per, "offset": offset}
        ).mappings().all()

    return render_template(
        "admin_messages.html",
        rows=rows,
        page=page,
        per=per,
        total=total,
        last_page=last_page,
    )

# ------------------ App factory ------------------
def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # --- Valeurs Babel par défaut ---
    app.config.setdefault("BABEL_DEFAULT_LOCALE", "fr")
    app.config.setdefault("BABEL_DEFAULT_TIMEZONE", "Europe/Paris")
    app.config.setdefault("BABEL_TRANSLATION_DIRECTORIES", "translations")

    # --- Clé secrète (sessions / flash) ---
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-change-me"

    # --- Fonction de sélection de locale ---
    def select_locale():
        lang = session.get("lang")
        if lang in ("fr", "en"):
            return lang
        return request.accept_languages.best_match(["fr", "en"]) or "fr"

    babel.init_app(app, locale_selector=select_locale)

    # --- Variables globales Jinja ---
    @app.context_processor
    def inject_globals():
        return {
            "user": session.get("user"),
            "ep": (request.endpoint or ""),
            "get_locale": lambda: str(get_locale()),
        }

    # --- Blueprints ---
    app.register_blueprint(pages_bp)
    app.register_blueprint(admin_bp)

    # --- Gestion des erreurs ---
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

    # --- Initialisation DB ---
    with app.app_context():
        init_db()

    return app


# ------------------ Entrypoint ------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)