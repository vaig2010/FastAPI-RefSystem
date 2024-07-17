from typing import Annotated
from fastapi import APIRouter, Depends
from repository import RefCodeRepository
from schemas import ReferralCode, ReferralCodeAdd, ReferralCodeId

router = APIRouter(prefix="/refcodes")
@router.post("")
async def add_referral_code(code : ReferralCodeAdd = Depends()) -> ReferralCodeId:
    code_id = await RefCodeRepository.add_code(code)
    return {"ok": True, "code_id": code_id}

@router.get("")
async def get_all_codes() -> list[ReferralCode]:
    codes = await RefCodeRepository.get_codes()
    return codes
