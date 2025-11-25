from sqlalchemy.orm import relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Source(IntIdPkMixin, Base):
    __tablename__ = 'sources'

    operators = relationship(
        "SourceOperator",
        backref="source",
    )