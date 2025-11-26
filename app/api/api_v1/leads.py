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
from core.schemas.lead import (
    LeadCreate,
    LeadResponse,
)

from crud.leads import crud_leads


router = APIRouter(
    prefix=settings.api.v1.leads,
    tags=["Leads"],
)


@router.get(
    "/all",
    response_model=List[LeadResponse],
    summary="Получить всех лидов",
    status_code=status.HTTP_200_OK,
)
async def get_all_leads(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    leads = await crud_leads.get_all(
        session=session,
    )
    return [
        LeadResponse.model_validate(lead)
        for lead in leads
    ]


@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    summary="Получить лида по id",
    status_code=status.HTTP_200_OK,
)
async def get_lead_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        lead_id: int = Path(..., description="id лида"),
):
    lead = await crud_leads.get_by_id(
        session=session,
        model_id=lead_id,
    )
    return LeadResponse.model_validate(lead)


@router.post(
    "/create",
    response_model=LeadResponse,
    summary="Создание лида",
    status_code=status.HTTP_201_CREATED,
)
async def create_lead(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        create_schema: LeadCreate,
):
    lead = await crud_leads.create(
        session=session,
        create_schema=create_schema,
    )
    return LeadResponse.model_validate(lead)