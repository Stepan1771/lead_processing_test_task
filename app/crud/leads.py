from core.models import Lead
from core.schemas.lead import (
    LeadCreate,
    LeadUpdate,
)
from crud.base import BaseCRUD


class LeadCRUD(BaseCRUD[Lead, LeadCreate, LeadUpdate]):
    pass



crud_leads = LeadCRUD(Lead)