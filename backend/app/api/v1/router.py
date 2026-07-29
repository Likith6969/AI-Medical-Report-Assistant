from fastapi import APIRouter
from app.api.v1.endpoints import auth, reports, chat, dashboard, analytics


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports Analysis"])
api_router.include_router(chat.router, prefix="/assistant", tags=["AI Health Assistant"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Patient Dashboard"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Model Analytics"])





