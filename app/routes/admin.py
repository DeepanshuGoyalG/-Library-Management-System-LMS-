from flask import render_template, redirect, url_for, flash,request,send_file,Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.book import Book
from app.models.review import Borrow
from app.models.issue import Issue
from datetime import datetime,timezone
import pandas as pd
import io
from app.utils.email_utils import send_due_reminder

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


# Admin dashboard route
@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('user.user_dashboard'))

    stats = {
        'books_count': Book.query.count(),
        'users_count': User.query.count(),
        'issued_count': Issue.query.filter_by(status='issued').count(),
        'upload_logs_count': 0  # Or track actual upload logs if you have a model
    }

    return render_template('admin_dashboard.html', stats=stats)

@admin_bp.route('/admin/borrowed_books')
@login_required
def view_all_borrowed_books():
    if current_user.role != 'admin':
        flash('Access denied! Admins only.', 'danger')
        return redirect(url_for('user.user_dashboard'))

    borrowed_books = Borrow.query.order_by(Borrow.borrow_date.desc()).all()
    return render_template('admin_borrowed_books.html', borrowed_books=borrowed_books)

@admin_bp.route('/admin/inventory')
@login_required
def view_inventory():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    books = Book.query.order_by(Book.title).all()
    return render_template('admin_inventory.html', books=books)

@admin_bp.route('/admin/export/borrowed', methods=['GET'])
@login_required
def export_borrowed_books():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    borrowed = Borrow.query.all()
    data = []

    for b in borrowed:
        data.append({
            'Borrow ID': b.id,
            'User': b.user.name,
            'Book': b.book.title,
            'Borrowed On': b.borrow_date.strftime('%Y-%m-%d'),
            'Due Date': b.due_date.strftime('%Y-%m-%d'),
            'Returned On': b.return_date.strftime('%Y-%m-%d') if b.return_date else '',
            'Status': 'Returned' if b.return_date else ('Overdue' if b.is_overdue() else 'Active')
        })

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='BorrowedBooks')

    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name='borrowed_books_report.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@admin_bp.route('/admin/send_reminders')
@login_required
def send_reminders():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))
    overdue_books = Borrow.query.filter(Borrow.return_date.is_(None)).all()
    count = 0
    for b in overdue_books:
        if b.is_overdue():
            try:
                send_due_reminder(b.user.email, b.book.title, b.due_date)
                count += 1
            except Exception as e:
                print("Error sending email reminders:", e)

    flash(f'Sent {count} reminder emails for overdue books.', 'info')
    return redirect(url_for('admin.view_all_borrowed_books'))

@login_required
def manage_books():
    if current_user.role != 'admin':
        flash('Access denied! Admins only.', 'danger')
        return redirect(url_for('user.user_dashboard'))

    books = Book.query.all()
    return render_template('manage_books.html', books=books)


@admin_bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Access denied! Admins only.', 'danger')
        return redirect(url_for('user.user_dashboard'))

    users = User.query.all()
    return render_template('manage_users.html', users=users)

@admin_bp.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'Book "{book.title}" deleted successfully.', 'success')
    return redirect(url_for('admin.manage_books'))
@admin_bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        copies = int(request.form['available_copies'])

        new_book = Book(title=title, author=author, category=category, available_copies=copies)
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{title}" added successfully.', 'success')
        return redirect(url_for('admin.manage_books'))

    return render_template('add_edit_book.html', book=None)

@admin_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.category = request.form['category']
        book.available_copies = int(request.form['available_copies'])
        db.session.commit()
        flash(f'Book "{book.title}" updated successfully.', 'success')
        return redirect(url_for('admin.manage_books'))

    return render_template('add_edit_book.html', book=book)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User "{name}" added successfully.', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('add_edit_user.html', user=None)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('user.user_dashboard'))

    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        flash(f'User "{user.name}" updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('add_edit_user.html', user=user)
