from fastapi import APIRouter
from starlette import status

from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.sources,
    tags=["Sources"],
)


@router.post(
    "/create",
    summary="Создание источника (бота)",
    status_code=status.HTTP_201_CREATED,
)
async def create_source():
    pass