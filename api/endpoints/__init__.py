from fastapi import APIRouter

from api.endpoints import recommendation

router = APIRouter()

router.include_router(recommendation.router, tags=['Popularity-based recommendations'])