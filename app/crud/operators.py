from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Operator
from core.schemas.operator import (
    OperatorCreate,
    OperatorUpdate,
)

from crud.base import BaseCRUD


class OperatorCRUD(BaseCRUD[Operator, OperatorCreate, OperatorUpdate]):

    @staticmethod
    async def get_active_operators(
            session: AsyncSession,
    ) -> Sequence[Operator]:
        try:
            stmt = await session.execute(
                select(Operator)
                .filter(Operator.is_active,
                        Operator.current_load < Operator.max_load_limit
                )
            )
            result = stmt.scalars().all()
            if not result:
                raise HTTPException(status_code=404, detail="Operator not found")
            return result

        except Exception as e:
            raise e


    async def update_load(
            self,
            session: AsyncSession,
            operator_id: int,
            load_change: int,
    ) -> Operator:
        try:
            operator = await self.get_by_id(
                session=session,
                model_id=operator_id,
            )
            if operator:
                new_load = operator.current_load + load_change
                if 0 <= new_load <= operator.max_load_limit:
                    operator.current_load = new_load
                    session.add(operator)
                    await session.commit()
                    await session.refresh(operator)
            return operator

        except Exception as e:
            raise e



crud_operators = OperatorCRUD(Operator)
