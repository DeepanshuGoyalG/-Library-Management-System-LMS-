from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get base directory path
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security Key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'library.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------- New Settings for Step 5 (Excel Uploads) ----------
    # Folder where uploaded Excel files will be saved
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    # Allowed file extensions (currently only Excel files)
    ALLOWED_EXTENSIONS = {'xlsx'}


    # Flask-Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')   # your Gmail
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')   # app password
    MAIL_DEFAULT_SENDER = ('Library Admin', os.environ.get('EMAIL_USER'))
    
