from datetime import datetime,timezone
from app import db

class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # ✅ Local time
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='issued')  # issued / returned

    user = db.relationship('User', back_populates='issues')
    book = db.relationship('Book', back_populates='issues')