from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Lead(IntIdPkMixin, Base):
    __tablename__ = 'leads'

    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    contacts = relationship(
        'Contact',
        back_populates='lead',
    )