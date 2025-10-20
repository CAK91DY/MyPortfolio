# auth/routes.py
from flask import Blueprint, session, redirect, url_for, flash

# Blueprint d’authentification (même si on ne gère plus de login externe)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- Connexion/Déconnexion simples pour tests ou placeholders ---
@auth_bp.route("/login-demo")
def login_demo():
    """Connexion fictive pour tests (aucun Google Login)."""
    session["user"] = {
        "name": "Christophe CAKPO",
        "email": "cakpochristophes91@gmail.com",
        "provider": "demo",
    }
    flash("Connecté en mode démo.", "success")
    return redirect(url_for("pages.index"))


@auth_bp.route("/logout")
def logout():
    """Déconnexion simple."""
    session.pop("user", None)
    flash("Déconnecté.", "info")
    return redirect(url_for("pages.index"))