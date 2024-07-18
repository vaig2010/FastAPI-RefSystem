from fastapi import APIRouter, Depends
from users.repository import UserRepository
from users.schemas import CreateUser, User
from db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_all_users(session: AsyncSession = Depends(db_helper.session_dependency)) -> list[User]:
    codes = await UserRepository.get_users(session=session)
    return codes

@router.post("/")
async def add_user(session: AsyncSession = Depends(db_helper.session_dependency), 
                   user: CreateUser = Depends()
                   ):
    user_id = await UserRepository.add_user(session=session, user=user)
    return {"ok": True, "user_id": user_id}
