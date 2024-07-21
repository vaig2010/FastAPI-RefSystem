from typing import Optional
from fastapi_users import schemas, models
from pydantic import EmailStr

class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    code_id: Optional[int] | None = None


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    code_id: Optional[int] | None = None


class UserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    code_id: Optional[int] | None = None
