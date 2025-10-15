import os
import pandas as pd
from app import db
from app.models.book import Book
from app.models.user import User

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_excel(file_path, upload_type):
    df = pd.read_excel(file_path)

    if upload_type == 'books':
        for _, row in df.iterrows():
            book = Book(
                title=row['title'],
                author=row['author'],
                category=row.get('category', 'Uncategorized'),
                available_copies=row.get('available_copies', 1)
            )
            db.session.add(book)

    elif upload_type == 'users':
        for _, row in df.iterrows():
            user = User(
                name=row['name'],
                email=row['email'],
                role=row.get('role', 'user')
            )
            db.session.add(user)

    db.session.commit()
