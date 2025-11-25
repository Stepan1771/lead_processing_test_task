from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from core.db import db_helper
from core.schemas.operator import OperatorResponse, OperatorCreate

from crud.operators import crud_operators


router = APIRouter(
    prefix=settings.api.v1.operators,
    tags=["Operators"],
)


@router.get(
    "/all",
    summary="Получить всех операторов",
    status_code=status.HTTP_200_OK,
)
async def get_all_operators():
    pass


@router.post(
    "/create",
    response_model=OperatorResponse,
    summary="Создание оператора",
    status_code=status.HTTP_201_CREATED,
)
async def create_operator(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        create_schema: OperatorCreate,
):
    operator = await crud_operators.create(
        session=session,
        create_schema=create_schema,
    )
    return OperatorResponse.model_validate(operator)


@router.post(
    "/manage",
    summary="Управление лимитом нагрузки и активностью оператора",
)
async def manage():
    pass


@router.delete(
    "/delete",
    summary="Удаление оператора",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_operator(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    operator_id: str = Path(..., description="operator id"),
):
    pass
