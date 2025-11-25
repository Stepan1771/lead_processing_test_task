from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Lead(IntIdPkMixin, Base):
    __tablename__ = 'leads'

    phone_number: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=False,
    )
    contacts = relationship(
        'Contact',
        back_populates='lead',
        cascade='all, delete-orphan'
    )