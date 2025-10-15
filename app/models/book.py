from datetime import datetime,timezone
from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)

    added_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_on = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    issues = db.relationship('Issue', back_populates='book', lazy=True)
    borrows = db.relationship('Borrow', back_populates='book', lazy=True)
    reviews = db.relationship('Review', back_populates='book', lazy=True)

    def is_available(self):
        return self.available_copies > 0

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
