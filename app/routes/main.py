from flask import render_template, Blueprint
from flask_login import login_required, current_user
from flask import request, jsonify
from app.models.book import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user)



@main_bp.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
        results = [{'id': b.id, 'title': b.title, 'author': b.author} for b in books]
    else:
        results = []
    return jsonify(results)
