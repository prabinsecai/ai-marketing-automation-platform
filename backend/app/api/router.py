from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.workspaces import router as workspaces_router
from app.api.v1.products import router as products_router
from app.api.v1.audiences import router as audiences_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.strategy import router as strategy_router
from app.api.v1.content import router as content_router
from app.api.v1.approvals import router as approvals_router
from app.api.v1.ai_logs import router as ai_logs_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.demo import router as demo_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(workspaces_router)
api_router.include_router(products_router)
api_router.include_router(audiences_router)
api_router.include_router(campaigns_router)
api_router.include_router(strategy_router)
api_router.include_router(content_router)
api_router.include_router(approvals_router)
api_router.include_router(ai_logs_router)
api_router.include_router(dashboard_router)
api_router.include_router(demo_router)
