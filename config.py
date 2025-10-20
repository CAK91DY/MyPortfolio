# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clé secrète pour les sessions
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key_12345")

    # Base de données SQLite locale
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "datacraft.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False