from app import db
from datetime import datetime, timedelta,timezone

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Integer)  # 1 to 5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    book = db.relationship('Book', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')



class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=14))
    return_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='borrows')
    book = db.relationship('Book', back_populates='borrows')

    def is_overdue(self):
        return not self.return_date and datetime.now(timezone.utc)> self.due_date
