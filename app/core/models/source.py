from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Source(IntIdPkMixin, Base):
    __tablename__ = 'sources'

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    contacts = relationship(
        "Contact",
        back_populates="source",
    )