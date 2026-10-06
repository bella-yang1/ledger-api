from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    balance: int = 0


class AccountRead(BaseModel):
    id: int
    name: str
    balance: int

    model_config = {"from_attributes": True}