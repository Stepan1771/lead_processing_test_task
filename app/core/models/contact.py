from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Contact(IntIdPkMixin, Base):
    __tablename__ = 'contacts'

    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('leads.id'),
        nullable=False,
        index=True,
    )
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('sources.id'),
        nullable=False,
        index=True,
    )
    operator_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('operators.id'),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default='new',
        nullable=False,
    )
    is_distributed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


    lead = relationship(
        'Lead',
        back_populates='contacts',
    )
    source = relationship(
        'Source', back_populates='contacts',
    )
    operator = relationship(
        'Operator',
        back_populates='contacts',
    )