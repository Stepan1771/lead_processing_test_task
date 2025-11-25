from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class SourceOperator(IntIdPkMixin, Base):
    __tablename__ = 'sources_operators'

    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('sources.id'),
        nullable=False,
    )
    operator_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('operators.id'),
        nullable=False,
    )
    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    source = relationship('Source', back_populates='operators')
    operator = relationship('Operator', back_populates='sources')