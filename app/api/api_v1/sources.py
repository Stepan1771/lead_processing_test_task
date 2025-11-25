from fastapi import APIRouter

from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.sources,
    tags=["Sources"],
)