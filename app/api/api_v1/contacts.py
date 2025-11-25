from fastapi import APIRouter

from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.contacts,
    tags=["Contacts"],
)


@router.post(
    "/create",
    summary="Создание обращения",
)
async def create_contact():
    pass