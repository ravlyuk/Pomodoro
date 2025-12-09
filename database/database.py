from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

settings = Settings()


engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def get_db_session():
    return Session()
