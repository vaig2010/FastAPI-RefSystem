from fastapi import APIRouter, Depends, HTTPException
from db.models import User
from auth.fastapi_users import current_user
from users.repository import UserRepository
from referral_codes.repository import RefCodeRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_helper import db_helper
from db.schemas import ReferralCode, UserRead

router = APIRouter(prefix="/my_refcode", tags=["User Referral Code"])


@router.get("/")
async def get_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: UserRead = Depends(current_user),
) -> ReferralCode:
    code = await UserRepository.get_user_refcode(session=session, user_id=user.id)
    if not code:
        raise HTTPException(status_code=404, detail="Referral code not found")
    return code


@router.post("/")
async def create_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
) -> dict:
    try:
        code = await RefCodeRepository.create_user_refcode(
            user_id=user.id, validity_days=30, session=session
        )
        user = await UserRepository.update_users_code_id(
            session=session, user=user, refcode=code
        )
        code_schema = ReferralCode.model_validate(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"refcode": code_schema}


@router.delete("/", status_code=204)
async def delete_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
) -> None:
    code = await UserRepository.get_user_refcode(session=session, user_id=user.id)
    await RefCodeRepository.delete_code(session=session, code=code)
