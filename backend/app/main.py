import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.api.router import api_router
from app.seed.demo_data import seed_demo_data
from app.models.workspace import Workspace

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    # Auto-seed demo data if DB has no workspaces
    db = SessionLocal()
    try:
        count = db.query(Workspace).count()
        if count == 0:
            logger.info("No workspaces found. Auto-seeding realistic e-commerce demo data...")
            seed_demo_data(db)
    except Exception as e:
        logger.warning(f"Startup seed check skipped: {e}")
    finally:
        db.close()

    yield

    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Phase 1 - AI Marketing Automation & Campaign Intelligence Platform API",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global safe exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please check server logs for details."},
    )

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
    }
