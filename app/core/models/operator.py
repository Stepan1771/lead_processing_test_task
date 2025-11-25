from sqlalchemy import Boolean, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Operator(IntIdPkMixin, Base):
    __tablename__ = 'operators'

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        index=True,
        default=True,
    )
    limit: Mapped[int] = mapped_column(
        Integer,
        null=False,
        default=10,
    )

    sources = relationship(
        "SourceOperator",
        backref="operator",
    )

    __table_args__ = (
        Index('ix_active_operators', 'is_active'),
    )