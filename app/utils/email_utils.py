from flask_mail import Message
from app import mail,db
from app.models.issue import Issue
from app.models.book import Book
from flask import current_app
from datetime import datetime, timedelta,timezone

def send_due_reminder():
    with current_app.app_context():
        # Define reminder threshold (e.g., 3 days before due)
        reminder_date = datetime.now(timezone.utc) + timedelta(days=3)

        # Get all issued books not yet returned
        issues = Issue.query.filter(Issue.status=='issued').all()

        for issue in issues:
            user_email = issue.user.email
            book_title = issue.book.title
            if not user_email or not book_title:
                continue
            if issue.return_date is None and issue.issue_date.date() <= reminder_date.date():
                msg = Message(
                    subject=f"Reminder: Book '{book_title}' Due Soon",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[user_email],
                    body=f"Dear {issue.user.name},\n\n"
                         f"Your borrowed book '{book_title}' is due on {issue.return_date.strftime('%Y-%m-%d') if issue.return_date else 'soon'}.\n"
                         "Please return it on time.\n\nLibrary Management System"
                )

                mail.send(msg)


