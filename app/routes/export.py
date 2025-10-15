import os
import pandas as pd
from flask import Blueprint, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.book import Book
from app.models.user import User
from app.models.issue import Issue

export_bp = Blueprint('export', __name__, template_folder='../templates')

@export_bp.route('/admin/export/<string:datatype>')
@login_required
def export_data(datatype):
    if current_user.role != 'admin':
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('user.user_dashboard'))

    # Path to save generated report temporarily
    output_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f'{datatype}_report.xlsx')

    # Prepare data based on export type
    if datatype == 'books':
        data = Book.query.all()
        df = pd.DataFrame([{
            'ID': b.id,
            'Title': b.title,
            'Author': b.author,
            'Category': b.category,
            'Quantity': b.available_copies  # instead of b.quantity

        } for b in data])

    elif datatype == 'users':
        data = User.query.all()
        df = pd.DataFrame([{
            'ID': u.id,
            'Name': u.name,
            'Email': u.email,
            'Role': u.role
        } for u in data])

    elif datatype == 'issues':
        data = Issue.query.all()
        df = pd.DataFrame([{
            'ID': i.id,
            'Book ID': i.book_id,
            'User ID': i.user_id,
            'Borrow Date': i.borrow_date.strftime('%Y-%m-%d') if i.borrow_date else None,
            'Due Date': i.due_date.strftime('%Y-%m-%d') if i.due_date else None,
            'Return Date': i.return_date.strftime('%Y-%m-%d') if i.return_date else None,

            'Status': i.status
        } for i in data])

    else:
        flash("Invalid export type!", "warning")
        return redirect(url_for('admin.admin_dashboard'))

    # Save to Excel
    df.to_excel(output_file, index=False)
    flash(f'{datatype.capitalize()} data exported successfully!', 'success')

    # Send file for download
    return send_file(output_file, as_attachment=True)
