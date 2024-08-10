from models.schemas import (
    ReferralCode,
    ReferralCodeBase,
    ReferralCodeId,
    ReferralCodeUpdatePartial,
)
from typing import Annotated
from pydantic import EmailStr
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Path, HTTPException

from models.db_helper import db_helper
from referral_codes.repository import RefCodeRepository
from .dependencies import refcode_by_id


router = APIRouter(prefix="/refcodes", tags=["Referral Codes"])


@router.post("/")
async def add_referral_code(
    code: ReferralCodeBase,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ReferralCodeId:
    code_id = await RefCodeRepository.add_code(
        session=session,
        code=code,
    )
    return {"ok": True, "code_id": code_id}


@router.get("/")
async def get_all_codes(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ReferralCode]:
    codes = await RefCodeRepository.get_codes(
        session=session,
    )
    return codes


@router.get("/{code_id}/")
async def get_code_by_id(
    code: ReferralCode = Depends(refcode_by_id),
) -> ReferralCode:
    return code


@router.put("/{code_id}/")
async def update_code_by_id(
    code_update: ReferralCodeBase,
    session: AsyncSession = Depends(db_helper.session_dependency),
    code: ReferralCode = Depends(refcode_by_id),
):
    code = await RefCodeRepository.update_code(
        session=session, code=code, code_update=code_update
    )
    return code


@router.patch("/{code_id}/")
async def update_code_by_id_partial(
    code_update: ReferralCodeUpdatePartial,
    session: AsyncSession = Depends(db_helper.session_dependency),
    code: ReferralCode = Depends(refcode_by_id),
):
    code = await RefCodeRepository.update_code(
        session=session, code=code, code_update=code_update, partial=True
    )
    return code


@router.delete("/{code_id}/", status_code=204)
async def delete_code_by_id(
    code: ReferralCode = Depends(refcode_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await RefCodeRepository.delete_code(session=session, code=code)


@router.post("/by_email/")
async def get_code_by_email(
    session: AsyncSession = Depends(db_helper.session_dependency),
    email: str | Annotated[EmailStr, Path()] = "user@example.com",
):

    code_model = await RefCodeRepository.get_code_by_email(session=session, email=email)
    if not code_model:
        raise HTTPException(
            status_code=404, detail="Referral code not found for this email"
        )
    return {"refcode": code_model}
