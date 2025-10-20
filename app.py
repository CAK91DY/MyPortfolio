# app.py
from flask import Flask, render_template, session, Blueprint, abort
from config import Config
from contact.models import db
from auth import auth_bp
from contact import contact_bp
from flask_migrate import Migrate
from flask import send_from_directory

# ------------------ Données démo (pour /projets) ------------------
PROJECTS = [
    {
        "slug": "sqlforge",
        "title": "SQLForge — plateforme d’exercices SQL",
        "summary": "Application Flask avec éditeur SQL, vérification automatique et suivi de progression.",
        "image": "/static/img/projets/projets01.jpeg",
        "stack": "Flask, SQLite/MySQL, CodeMirror",
        "problem": "Former vite et bien aux requêtes SQL.",
        "solution": "Éditeur + vérification auto + suivi progression.",
        "impact": "+40% de rétention apprenants",
        "features": ["Éditeur SQL en ligne", "Tests unitaires d'exercices", "Progression apprenant"],
        "tags": ["Flask", "Python", "SQL"],
        "link": "#",
        "repo": "#",
    },
    {
        "slug": "jobhub",
        "title": "JobHub — agrégateur d’offres",
        "summary": "Search unifié (Meilisearch), normalisation multi-sources, filtres et UI responsive.",
        "image": "/static/img/projets/projets02.jpeg",
        "stack": "Flask, Meilisearch, APIs",
        "problem": "Multiples sites, recherche longue & redondante.",
        "solution": "Normalisation multi-sources + index unique.",
        "impact": "Temps de recherche ÷ 3",
        "features": ["Index Meilisearch", "Normalisation JSON", "Filtres facettés"],
        "tags": ["API", "Indexing", "UX"],
        "link": "#",
        "repo": "#",
    },
    {
        "slug": "airflow-pipeline",
        "title": "Pipeline Airflow → DWH",
        "summary": "Ingestion quotidienne d’API, tests de qualité, chargement Snowflake et reporting.",
        "image": "/static/img/projets/airflow.png",
        "stack": "Airflow, Python, Snowflake",
        "problem": "Ingestion & qualité de données quotidiennes.",
        "solution": "Orchestration + tests + chargement Snowflake.",
        "impact": "Fiabilité 99.5%",
        "features": ["Schedules DAG", "Tests de qualité", "Charge Snowflake"],
        "tags": ["Airflow", "ELT", "Snowflake"],
        "link": "#",
        "repo": "#",
    },

     {
        "slug": "airflow-pipeline",
        "title": "Pipeline Airflow → DWH",
        "summary": "Ingestion quotidienne d’API, tests de qualité, chargement Snowflake et reporting.",
        "image": "/static/img/projets/airflow.png",
        "stack": "Airflow, Python, Snowflake",
        "problem": "Ingestion & qualité de données quotidiennes.",
        "solution": "Orchestration + tests + chargement Snowflake.",
        "impact": "Fiabilité 99.5%",
        "features": ["Schedules DAG", "Tests de qualité", "Charge Snowflake"],
        "tags": ["Airflow", "ELT", "Snowflake"],
        "link": "#",
        "repo": "#",
    },
]


def get_project_or_404(slug: str):
    for p in PROJECTS:
        if p["slug"] == slug:
            return p
    abort(404)


# ------------------ Blueprint "pages" ------------------
pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/", endpoint="index")
def index():
    return render_template("index.html")

@pages_bp.route("/projets", endpoint="projets")
def projets():
    return render_template("projets.html", projects=PROJECTS)

@pages_bp.route("/projets/<slug>", endpoint="projet_detail")
def projet_detail(slug):
    project = get_project_or_404(slug)
    return render_template("projet_detail.html", project=project)

@pages_bp.route("/services", endpoint="services")
def services():
    return render_template("services.html")

@pages_bp.route("/apropos", endpoint="apropos")
def apropos():
    return render_template("apropos.html")


# Sert le PDF en téléchargement (Content-Disposition: attachment)
@pages_bp.route("/cv", endpoint="cv")
def download_cv():
    return send_from_directory(
        directory="static/docs",
        path="CV_Christophe_CAKPO.pdf",
        as_attachment=True,
        download_name="CV_Christophe_CAKPO.pdf",
        mimetype="application/pdf",
    )


# ------------------ App factory ------------------
def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)  # Assure-toi que SQLALCHEMY_DATABASE_URI = "sqlite:///datacraft.db"

    # DB + Migrations
    db.init_app(app)
    Migrate(app, db)  # Flask-Migrate branché ici

    # user dispo dans tous les templates
    @app.context_processor
    def inject_user():
        return {"user": session.get("user")}

    # Blueprints
    app.register_blueprint(auth_bp)     # ex: auth.login_google / auth.logout
    app.register_blueprint(contact_bp)  # ex: contact.form (url_prefix="/contact")
    app.register_blueprint(pages_bp)    # pages.* (index, projets, etc.)

    # Handlers (optionnels)
    @app.errorhandler(404)
    def not_found(e):
        try:
            return render_template("404.html"), 404
        except Exception:
            return "Page non trouvée", 404

    return app


# --------------- Entrypoint ---------------
app = create_app()

if __name__ == "__main__":
    # Debug utile si besoin :
    # print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    app.run(debug=True)