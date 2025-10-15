import threading
import time
from app import create_app
from app.utils.email_utils import send_due_reminder

def schedule_email_reminder(interval_hours=24):
    """
    Run send_due_reminder() in a background thread at the given interval.
    """
    app = create_app()  # create app to get app context

    def run():
        with app.app_context():
            while True:
                try:
                    send_due_reminder()
                except Exception as e:
                    print("Error sending email reminders:", e)
                time.sleep(interval_hours * 3600)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
