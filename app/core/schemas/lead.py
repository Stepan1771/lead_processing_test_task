from pydantic import BaseModel, ConfigDict


class LeadBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class LeadCreate(LeadBase):
    email: str


class LeadUpdate(LeadBase):
    email: str | None = None


class LeadResponse(LeadBase):
    id: int
    email: str


class LeadContactsResponse(LeadResponse):
    contacts: list = []
