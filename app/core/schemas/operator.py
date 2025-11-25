from pydantic import BaseModel, ConfigDict


class OperatorBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class OperatorCreate(OperatorBase):
    is_active: bool
    limit: int


class OperatorUpdate(OperatorBase):
    pass


class OperatorResponse(OperatorBase):
    id: int
    is_active: bool
    limit: int
