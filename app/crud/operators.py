from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Operator
from core.schemas.operator import OperatorCreate, OperatorUpdate
from crud.base import BaseCRUD


class OperatorCRUD(BaseCRUD[Operator, OperatorCreate, OperatorUpdate]):

    @staticmethod
    async def create(
            session: AsyncSession,
            create_schema: OperatorCreate,
    ) -> Operator:
        try:
            operator = Operator(
                is_active=create_schema.is_active,
                limit=create_schema.limit,
            )
            session.add(operator)
            await session.commit()
            await session.refresh(operator)
            return operator

        except Exception as e:
            raise e


crud_operators = OperatorCRUD(Operator)
