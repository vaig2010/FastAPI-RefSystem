from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_helper import db_helper
from models.models import ReferralCode
from referral_codes.repository import RefCodeRepository


async def refcode_by_id(
    code_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ReferralCode:
    code = await RefCodeRepository.get_code_by_id(session=session, code_id=code_id)
    if code is not None:
        return code

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Code {code_id} not found!",
    )
