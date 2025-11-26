from typing import Dict

from pydantic import (
    BaseModel,
    ConfigDict,
)


class OperatorBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class OperatorCreate(OperatorBase):
    name: str
    is_active: bool = True
    max_load_limit: int = 10
    competencies: Dict[str, float] = {}



class OperatorUpdate(OperatorBase):
    name: str | None = None
    is_active: bool | None = None
    max_load_limit: int | None = None
    competencies: Dict[str, float] | None = None


class OperatorResponse(OperatorBase):
    id: int
    name: str
    is_active: bool
    max_load_limit: int
    current_load: int

class OperatorContactsResponse(OperatorResponse):
    contacts: list = []