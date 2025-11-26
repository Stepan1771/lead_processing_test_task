from typing import (
    List,
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
    Path,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from core.db import db_helper
from core.schemas.contact import (
    ContactResponse,
    ContactCreate,
)

from crud.contacts import crud_contacts
from crud.ditribution import distribution_service

router = APIRouter(
    prefix=settings.api.v1.contacts,
    tags=["Contacts"],
)


@router.get(
    "/all",
    response_model=List[ContactResponse],
    summary="Получить все обращения",
    status_code=status.HTTP_200_OK,
)
async def get_all_contacts(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    contacts = await crud_contacts.get_all(
        session=session,
    )
    return [
        ContactResponse.model_validate(contact)
        for contact in contacts
    ]


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    summary="Получить обращение по id",
    status_code=status.HTTP_200_OK,
)
async def get_contact_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        contact_id: int = Path(..., description="id обращения"),
):
    operator = await crud_contacts.get_by_id(
        session=session,
        model_id=contact_id,
    )
    return ContactResponse.model_validate(operator)


@router.post(
    "/create",
    response_model=ContactResponse,
    summary="Создание обращения",
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        create_schema: ContactCreate,
):
    contact = await crud_contacts.create(
        session=session,
        create_schema=create_schema,
    )
    return ContactResponse.model_validate(contact)


@router.post(
    "/{contact_id}/distribute",
    response_model=dict,
    summary="Распределить обращение",
    status_code=status.HTTP_200_OK,
)
async def distribute_contact(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        contact_id: int = Path(..., description="id обращения"),
):
    contact = await crud_contacts.get_by_id(
        session=session,
        model_id=contact_id,
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    if contact.is_distributed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contact already distributed"
        )

    operator = await distribution_service.distribute_contact(
        session=session,
        contact=contact,
    )

    if operator:
        return {
            "contact_id": contact_id,
            "operator_id": operator.id,
            "operator_name": operator.name,
            "success": True,
            "message": f"Contact assigned to operator {operator.name}"
        }
    else:
        return {
            "contact_id": contact_id,
            "operator_id": None,
            "success": False,
            "message": "No available operators found"
        }


@router.post(
    "/distribution/run",
    response_model=List[dict],
    summary="Автоматическое распределение",
    status_code=status.HTTP_200_OK,
)
async def distribute_all_undistributed_contacts(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    return await distribution_service.distribute_all_undistributed(
        session=session,
    )


@router.get(
    "/undistributed",
    response_model=List[ContactResponse],
    summary="Получить нераспределенные обращения с пагинацией",
    status_code=status.HTTP_200_OK,
)
async def get_undistributed_contacts(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        skip: int = 0,
        limit: int = 100,
):
    contacts = await crud_contacts.get_undistributed(
        session=session,
    )
    return contacts[skip:skip + limit]