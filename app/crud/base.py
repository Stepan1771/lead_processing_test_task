from typing import Sequence, Generic, TypeVar, Type

from fastapi import HTTPException
from starlette import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model


    async def get_all(
        self,
        session: AsyncSession,
    ) -> Sequence[ModelType]:
        try:
            stmt = await session.execute(
                select(self.model)
                .order_by(self.model.id)
            )
            result = stmt.scalars().all()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not found",
                )
            return result

        except Exception as e:
            raise e


    async def get_by_id(
            self,
            session: AsyncSession,
            model_id: int,
    ) -> ModelType:
        try:
            stmt = await session.execute(
                select(self.model)
                .filter_by(id=model_id)
            )
            result = stmt.scalar_one_or_none()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ID '{model_id}' not found",
                )
            return result
        except Exception as e:
            raise e


    async def delete(
            self,
            session: AsyncSession,
            model_id: int,
    ):
        try:
            result = await self.get_by_id(
                session=session,
                model_id=int(model_id),
            )

            await session.delete(result)
            await session.commit()
            return HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            raise e