from fastapi import APIRouter, Depends
from db.db_helper import db_helper
from referral_codes.repository import RefCodeRepository
from referral_codes.schemas import ReferralCode, ReferralCodeBase, ReferralCodeId
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/refcodes", tags=["Referral Codes"])

@router.post("")
async def add_referral_code(session: AsyncSession = Depends(db_helper.session_dependency), 
                            code: ReferralCodeBase = Depends()) -> ReferralCodeId:
    code_id = await RefCodeRepository.add_code(session=session , data=code, )
    return {"ok": True, "code_id": code_id}

@router.get("")
async def get_all_codes(session: AsyncSession = Depends(db_helper.session_dependency), ) -> list[ReferralCode]:
    codes = await RefCodeRepository.get_codes(session=session ,)
    return codes

