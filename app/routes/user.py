from flask import render_template, redirect, url_for, flash,request 
from flask_login import login_required, current_user
from app.models.book import Book
from app.models.issue import Issue
from flask import Blueprint
from app.models.review import Review
from app import db
from app.models.review import Borrow
from datetime import datetime,timezone

user_bp = Blueprint('user', __name__, template_folder='../templates')

# User dashboard route
@user_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        flash("Admins cannot view user dashboard!", "info")
        return redirect(url_for('admin.admin_dashboard'))

    borrowed_books = Issue.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'user_dashboard.html',
        borrowed_books=borrowed_books
    )



@user_bp.route('/submit_review/<int:book_id>', methods=['POST'])
@login_required
def submit_review(book_id):
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '').strip()

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "warning")
        return redirect(url_for('user.user_dashboard'))

    review = Review(book_id=book_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    flash("Review submitted successfully!", "success")
    return redirect(url_for('user.user_dashboard'))


@user_bp.route('/book/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)



@user_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)

    if book.available_copies <= 0:
        flash("Sorry, this book is currently unavailable.", "warning")

        return redirect(url_for('user.user_dashboard'))
    
    existing = Borrow.query.filter_by(user_id=current_user.id, book_id=book_id, return_date=None).first()
    if existing:
        flash("You have already borrowed this book.", "info")
        return redirect(url_for('user.user_dashboard'))


    borrow = Borrow(user_id=current_user.id, book_id=book_id)
    book.available_copies -= 1
    db.session.add(borrow)
    db.session.commit()
    flash("Book borrowed successfully! Due in 14 days.", "success")
    return redirect(url_for('user.user_dashboard'))

@user_bp.route('/borrowed_books')
@login_required
def view_borrowed_books():
    borrowed_books = Borrow.query.filter_by(user_id=current_user.id).order_by(Borrow.borrow_date.desc()).all()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books)

@user_bp.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrow = Borrow.query.get_or_404(borrow_id)
    if borrow.user_id != current_user.id:
        flash("You are not authorized to return this book.", "danger")
        return redirect(url_for('user.user_dashboard'))

    borrow.return_date = datetime.now(timezone.utc)
    borrow.book.quantity += 1
    db.session.commit()

    flash("Book returned successfully!", "success")
    return redirect(url_for('user.view_borrowed_books'))



