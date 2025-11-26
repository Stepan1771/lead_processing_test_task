from typing import (
    Annotated,
    List,
)

from fastapi import (
    APIRouter,
    Depends,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from core.db import db_helper
from core.schemas.source import (
    SourceResponse,
    SourceCreate,
)

from crud.sources import crud_sources


router = APIRouter(
    prefix=settings.api.v1.sources,
    tags=["Sources"],
)


@router.get(
    "/all",
    response_model=List[SourceResponse],
    summary="Получить все источники",
    status_code=status.HTTP_200_OK,
)
async def get_all_sources(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    sources = await crud_sources.get_all(
        session=session,
    )
    return [
        SourceResponse.model_validate(source)
        for source in sources
    ]


@router.get(
    "/{source_id}",
    response_model=SourceResponse,
    summary="Получить источник по id",
    status_code=status.HTTP_200_OK,
)
async def get_source_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        source_id: int = Path(..., description="id источника"),
):
    source = await crud_sources.get_by_id(
        session=session,
        model_id=source_id,
    )
    return SourceResponse.model_validate(source)


@router.post(
    "/create",
    response_model=SourceResponse,
    summary="Создание источника (бота)",
    status_code=status.HTTP_201_CREATED,
)
async def create_source(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        create_schema: SourceCreate
):
    source = await crud_sources.create(
        session=session,
        create_schema=create_schema,
    )
    return SourceResponse.model_validate(source)