# contact/models.py
from datetime import datetime
from contact.models import db

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)