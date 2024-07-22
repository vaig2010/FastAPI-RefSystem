from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReferralCodeBase(BaseModel):
    code: str
    created_date: datetime
    expiration_date: datetime
    user_id: int


class ReferralCode(ReferralCodeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ReferralCodeId(BaseModel):
    ok: bool = True
    code_id: int


class ReferralCodeUpdatePartial(BaseModel):
    code: str | None = None
    created_date: datetime | None = None
    expiration_date: datetime | None = None
    user_id: int | None = None
