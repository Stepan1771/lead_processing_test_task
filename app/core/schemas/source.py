from pydantic import (
    BaseModel,
    ConfigDict,
)


class SourceBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class SourceCreate(SourceBase):
    name: str
    is_active: bool


class SourceUpdate(SourceBase):
    name: str | None = None
    is_active: bool | None = None


class SourceResponse(SourceBase):
    id: int
    name: str
    is_active: bool


class SourceContactsResponse(SourceResponse):
    contacts: list = []