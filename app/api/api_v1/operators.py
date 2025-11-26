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
from core.schemas.operator import (
    OperatorResponse,
    OperatorCreate,
)

from crud.operators import crud_operators


router = APIRouter(
    prefix=settings.api.v1.operators,
    tags=["Operators"],
)


@router.get(
    "/all",
    response_model=List[OperatorResponse],
    summary="Получить всех операторов",
    status_code=status.HTTP_200_OK,
)
async def get_all_operators(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    operators = await crud_operators.get_all(
        session=session,
    )
    return [
        OperatorResponse.model_validate(operator)
        for operator in operators
    ]


@router.get(
    "/{operator_id}",
    response_model=OperatorResponse,
    summary="Получить оператора по id",
    status_code=status.HTTP_200_OK,
)
async def get_operator_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        operator_id: int = Path(..., description="id оператора"),
):
    operator = await crud_operators.get_by_id(
        session=session,
        model_id=operator_id,
    )
    return OperatorResponse.model_validate(operator)


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
