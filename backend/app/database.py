import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

logger = logging.getLogger("app.database")

def get_engine():
    db_url = settings.DATABASE_URL
    try:
        if db_url.startswith("sqlite"):
            engine = create_engine(db_url, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(db_url, pool_pre_ping=True)
            # Test connection
            with engine.connect() as conn:
                pass
        return engine
    except Exception as e:
        if settings.DATABASE_FALLBACK_SQLITE:
            logger.warning(f"Could not connect to primary database ({db_url}): {e}. Falling back to SQLite ({settings.SQLITE_DB_PATH})")
            fallback_engine = create_engine(settings.SQLITE_DB_PATH, connect_args={"check_same_thread": False})
            return fallback_engine
        else:
            logger.error(f"Failed to connect to database: {e}")
            raise e

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
