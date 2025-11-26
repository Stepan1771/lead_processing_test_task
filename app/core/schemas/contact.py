from pydantic import (
    BaseModel,
    ConfigDict,
)


class ContactBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class ContactCreate(ContactBase):
    lead_id: int
    source_id: int


class ContactUpdate(ContactBase):
    operator_id: int | None = None
    status: str | None = None
    is_distributed: bool | None = None


class ContactResponse(ContactBase):
    id: int
    lead_id: int
    source_id: int
    operator_id: int | None
    status: str
    is_distributed: bool


class ContactRelations(ContactResponse):
    lead: dict | None = None
    source: dict | None = None
    operator: dict | None = None