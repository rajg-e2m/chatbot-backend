from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Async Database Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync Database Engine (for tools or legacy code)
# Fallback to DATABASE_URL but stripped of +asyncpg if SYNC_DATABASE_URL is empty
_sync_url = settings.SYNC_DATABASE_URL
if not _sync_url and settings.DATABASE_URL:
    _sync_url = settings.DATABASE_URL.replace("+asyncpg", "")

if _sync_url:
    sync_engine = create_engine(
        _sync_url,
        echo=settings.DEBUG,
        future=True
    )

    # Sync Session Factory
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=sync_engine
    )
else:
    SessionLocal = None

Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """Dependency for getting sync database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
