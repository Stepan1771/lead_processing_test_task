from sqlalchemy.orm import relationship

from core.models.mixins import IntIdPkMixin
from core.models import Base


class Source(IntIdPkMixin, Base):
    __tablename__ = 'sources'

    operators = relationship(
        "SourceOperator",
        back_populates="source",
    )