from datetime import datetime, timezone
from datetime import timedelta
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError
from typing import Optional
from fastapi_users import schemas, models
from core.config import settings


class ReferralCodeBase(BaseModel):
    code: str
    created_date: Optional[datetime] = Field(
        default_factory=settings.time_func.datetime_now
        )
    expiration_date: Optional[datetime] = Field(
        default_factory=settings.time_func.datetime_expiration
    )


class ReferralCode(ReferralCodeBase):
    id: int
    #user: "UserRead"
    model_config = ConfigDict(from_attributes=True)


class ReferralCodeId(BaseModel):
    ok: bool = True
    code_id: int


class ReferralCodeUpdatePartial(BaseModel):
    code: Optional[str] = None
    created_date: datetime | None = None
    expiration_date: datetime | None = None
    user_id: Optional[int] = None


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    # refcode_id: Optional[int] = None
    referrer_id: Optional[int] = None
    referral_code: Optional[ReferralCode] = None


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    # refcode_id: Optional[int] = None
    referrer_id: Optional[int] = None
    code: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    # refcode_id: Optional[int] = None
    referrer_id: Optional[int] = None
