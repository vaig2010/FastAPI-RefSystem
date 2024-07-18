from fastapi import APIRouter, Depends
from users.schemas import User


router = APIRouter(prefix="/users", tags=["Users"])


# @router.get("")
# async def get_all_users() -> list[User]:
#     codes = await RefCodeRepository.get_codes()
#     return codes

