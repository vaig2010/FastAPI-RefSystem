
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReferralCodeAdd(BaseModel):
    code: str
    created_date: datetime
    expiration_date: datetime 
    user_id: int
    
class ReferralCode(ReferralCodeAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class ReferralCodeId(BaseModel):
    ok: bool = True
    code_id: int