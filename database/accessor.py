from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import AsyncGenerator

from settings import Settings

settings = Settings()


engine = create_async_engine(
    url=settings.DATABASE_URL, echo=True, future=True, pool_pre_ping=True
)

AsyncSessonFactory = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessonFactory() as session:
        yield session
