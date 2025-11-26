from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Source
from core.schemas.source import SourceCreate, SourceUpdate
from crud.base import BaseCRUD


class SourceCRUD(BaseCRUD[Source, SourceCreate, SourceUpdate]):
    pass



crud_sources = SourceCRUD(Source)
