import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Babel
    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Paris"
    BABEL_TRANSLATION_DIRECTORIES = "translations"

    # DB
    DATABASE_URL = os.getenv("DATABASE_URL")