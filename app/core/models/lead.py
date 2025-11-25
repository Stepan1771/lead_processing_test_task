from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Lead(IntIdPkMixin, Base):
    __tablename__ = 'leads'

    phone_number: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=False,
    )