from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import Settings

settings = Settings()


engine = create_engine(settings.DATABASE_URL, echo=True)
SessionDB = sessionmaker(bind=engine)


def get_db_session() -> Session:
    return SessionDB()