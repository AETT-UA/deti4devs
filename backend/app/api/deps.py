from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal


# Dependency that sets up a database transaction for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()