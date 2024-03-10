from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings

engine = create_engine(settings.DATABASE_URL)


def get_session():
    """
    A function that returns a session object.

    Returns:
        Session: The session object.
    """
    try:
        with Session(engine) as session:  # pragma: no cover
            session.begin()
            yield session
    except Exception:
        return ""