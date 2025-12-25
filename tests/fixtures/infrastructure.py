import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import Settings
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models():
    """Create engine per test to avoid event loop issues."""
    engine = create_async_engine(
        url="postgresql+asyncpg://postgres:password@0.0.0.0:5432/pomodoro-test",
        future=True,
        echo=True,
        pool_pre_ping=False,  # Disable pool ping for tests
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def get_db_session(init_models) -> AsyncSession:
    engine = init_models
    async_session = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def db_session(init_models) -> AsyncSession:
    engine = init_models
    async_session = async_sessionmaker(
        engine,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
