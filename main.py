from app import create_app, db
from app.models import init_models
from app.utils.scheduler import schedule_email_reminder



app = create_app()

# Create the database tables
with app.app_context():
    init_models()  # ensure all models are imported
    db.create_all()
    print("✅ Database and tables created successfully!")
    schedule_email_reminder(interval_hours=24)  # check daily
if __name__ == "__main__":
    app.run(debug=True)



