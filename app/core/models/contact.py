from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins.int_id_pk import IntIdPkMixin
from core.models.base import Base


class Contact(IntIdPkMixin, Base):
    __tablename__ = 'contacts'

    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('leads.id'),
        nullable=False,
    )
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

    lead = relationship('Lead', back_populates='contacts')
    source = relationship('Source')
    operator = relationship('Operator')