from app.core.config import settings
from .base_class import Base
from .session import engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy import inspect

def init_db() -> None:
    if not settings.PRODUCTION:
        # Create schema if not exists
        with engine.connect() as conn:
            trans = conn.begin()
            inspector = inspect(engine)
            if settings.SCHEMA_NAME not in inspector.get_schema_names():
                try:
                    conn.execute(CreateSchema(settings.SCHEMA_NAME))
                    trans.commit()
                except Exception as e:
                    print(e)
                    trans.rollback()
                    
        # Create tables
        Base.metadata.reflect(bind=engine, schema=settings.SCHEMA_NAME)
        Base.metadata.create_all(bind=engine, checkfirst=True)