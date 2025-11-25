from sqlalchemy import Boolean, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Operator(IntIdPkMixin, Base):
    __tablename__ = 'operators'

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        index=True,
        default=True,
    )
    limit: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
    )

    sources = relationship(
        "SourceOperator",
        back_populates="operator",
    )

    __table_args__ = (
        Index('ix_active_operators', 'is_active'),
    )