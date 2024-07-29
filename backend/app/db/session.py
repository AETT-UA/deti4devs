from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(settings.POSTGRES_URI)
SessionLocal = sessionmaker(autoflush=False, bind=engine)