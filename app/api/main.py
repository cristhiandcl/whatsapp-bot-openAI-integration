"""API endpoints Router Module"""

from fastapi import APIRouter

from app.api.routes import jarvis, connection

api_router = APIRouter()
api_router.include_router(jarvis.router, prefix="/webhook", tags=["Jarvis"])
api_router.include_router(connection.router, prefix="/merli", tags=["Connection"])
