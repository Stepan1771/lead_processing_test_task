from sqlalchemy import (
    Boolean,
    Integer,
    String,
    JSON,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Operator(IntIdPkMixin, Base):
    __tablename__ = 'operators'

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )
    max_load_limit: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )
    current_load: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    competencies: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    contacts = relationship(
        "Contact",
        back_populates="operator",
    )

