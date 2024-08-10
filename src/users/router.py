from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from security.fastapi_users import current_user

from .repository import UserRepository
from referral_codes.repository import RefCodeRepository
from models.models import User
from models.db_helper import db_helper
from models.schemas import ReferralCode, UserRead, ReferralCodeId

router = APIRouter(prefix="/my_refcode", tags=["User Referral Code"])


@router.get("/")
async def get_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: UserRead = Depends(current_user),
) -> ReferralCode:
    code = await RefCodeRepository.get_refcode_by_user(session=session, user=user)
    if not code:
        raise HTTPException(status_code=404, detail="Referral code not found")
    return code


@router.post("/")
async def create_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
) -> ReferralCode:
    if user.refcode_id is not None:
        raise HTTPException(status_code=400, detail="Referral code already exists")
    try:
        code = await RefCodeRepository.create_user_refcode(
            validity_days=30, session=session
        )
        user = await UserRepository.update_users_refcode_id(
            session=session, user=user, refcode_id=code.id
        )
        code_schema = ReferralCode.model_validate(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return code_schema


@router.delete("/")
async def delete_user_refcode(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
) -> ReferralCodeId:
    code = await RefCodeRepository.get_refcode_by_user(session=session, user=user)
    if code is None:
        raise HTTPException(status_code=404, detail="Referral code not found")
    await RefCodeRepository.delete_code(session=session, code=code)
    return {"ok": True, "code_id": code.id}
