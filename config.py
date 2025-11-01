# config.py
from dotenv import load_dotenv; load_dotenv()
import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")