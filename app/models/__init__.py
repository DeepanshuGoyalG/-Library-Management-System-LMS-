from app.models.user import User
from app.models.book import Book
from app.models.issue import Issue
from app.models.review import Review, Borrow

# Optional helper to initialize models
def init_models():
    """Import all models so they are registered with SQLAlchemy"""
    # All models are already imported above, so this can remain empty
    pass
