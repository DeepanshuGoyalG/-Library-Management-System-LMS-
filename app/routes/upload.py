import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.utils.file_utils import allowed_file, process_excel


upload_bp = Blueprint('upload', __name__, template_folder='../templates')

@upload_bp.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def upload_excel():
    if current_user.role != 'admin':
        flash('Access denied! Admins only.', 'danger')
        return redirect(url_for('user.user_dashboard'))

    if request.method == 'POST':
        file = request.files.get('file')
        upload_type = request.form.get('upload_type')  # 'books' or 'users'

        if not file or file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(request.url)

        if upload_type not in ['books', 'users']:
            flash('Invalid upload type!', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = file.filename
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)

            try:
                process_excel(save_path, upload_type)
                flash(f'{upload_type.capitalize()} uploaded successfully!', 'success')
            except Exception as e:
                flash(f'Error processing file: {e}', 'danger')

            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid file type. Only .xlsx allowed.', 'danger')

    return render_template('upload_excel.html')
