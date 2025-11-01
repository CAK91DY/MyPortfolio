# contact/routes.py
from flask import Blueprint

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.get("/ping")
def ping():
    return {"ok": True}