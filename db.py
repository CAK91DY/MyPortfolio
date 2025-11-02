# db.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from config import Config

DATABASE_URL = Config.DATABASE_URL
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquant. Définis-le dans .env (local) et dans Render → Environment.")

# --- Normalize URL + SSL only for non-local hosts ---
url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
parsed = urlparse(url)

# Host considered local?
host = (parsed.hostname or "").lower()
is_local = host in ("localhost", "127.0.0.1", "::1", "")

# Merge/adjust query params
query = dict(parse_qsl(parsed.query))
if not is_local:
    # On Render/remote: enforce SSL
    query.setdefault("sslmode", "require")
else:
    # On local: make sure ssl isn't forced
    if "sslmode" in query:
        query.pop("sslmode")

url = urlunparse(parsed._replace(query=urlencode(query)))

# Connection (pool_pre_ping avoids stale connections on Render)
engine = create_engine(url, pool_pre_ping=True)

def init_db():
    """Crée la table messages de contact si elle n'existe pas, + index."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                subject VARCHAR(255),
                message TEXT NOT NULL,
                consent BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_contact_messages_created_at
            ON contact_messages (created_at DESC);
        """))

def save_contact_message(name: str, email: str, subject: str, message: str, consent: bool = True) -> bool:
    """Insère un message de contact et renvoie True/False."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO contact_messages (name, email, subject, message, consent)
                    VALUES (:name, :email, :subject, :message, :consent)
                """),
                {"name": name, "email": email, "subject": subject, "message": message, "consent": consent}
            )
        return True
    except SQLAlchemyError:
        return False