import os
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()

class Config:
    # Sécurité et session
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Babel (localisation)
    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"
    BABEL_TRANSLATION_DIRECTORIES = "translations"

    # Base de données (PostgreSQL local ou Render)
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Admin (authentification simple)
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Cak1dy*1991")