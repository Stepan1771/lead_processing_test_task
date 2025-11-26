from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Contact
from core.schemas.contact import (
    ContactCreate,
    ContactUpdate,
)

from crud.base import BaseCRUD


class ContactCRUD(BaseCRUD[Contact, ContactCreate, ContactUpdate]):

    @staticmethod
    async def get_undistributed(
            session: AsyncSession,
    ) -> Sequence[Contact]:
        try:
            stmt = await session.execute(
                select(Contact)
                .filter(Contact.is_distributed == False,
                        Contact.operator_id == None
                )
            )
            result = stmt.scalars().all()
            if not result:
                raise HTTPException(status_code=404)
            return result

        except Exception as e:
            raise e

    async def assign_operator(
            self,
            session: AsyncSession,
            contact_id: int,
            operator_id: int,
    ) -> Contact | None:
        """Назначить оператора на обращение."""
        contact = await self.get_by_id(
            session=session,
            model_id=contact_id,
        )
        if contact and not contact.operator_id:
            contact.operator_id = operator_id
            contact.is_distributed = True
            contact.status = "in_progress"
            session.add(contact)
            await session.commit()
            await session.refresh(contact)
        return contact


crud_contacts = ContactCRUD(Contact)