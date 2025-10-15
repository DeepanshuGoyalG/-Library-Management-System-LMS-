# app/routes/__init__.py

# Import all route blueprints
from app.routes.main import main_bp
from app.routes.admin import admin_bp
from app.routes.user import user_bp
from app.routes.upload import upload_bp
from app.routes.export import export_bp
from app.auth import auth_bp

all_blueprints = [main_bp, admin_bp, user_bp, upload_bp, export_bp, auth_bp]

