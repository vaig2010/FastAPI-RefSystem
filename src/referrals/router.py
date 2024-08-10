from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.db_helper import db_helper
from models.models import User
from models.schemas import UserRead


router = APIRouter(prefix="/referrals", tags=["Referrals"])


@router.get("/{referrer_id}/")
async def get_referrals(
    referrer_id: int, session: AsyncSession = Depends(db_helper.session_dependency)
) -> list[UserRead]:
    result = await session.execute(select(User).where(User.referrer_id == referrer_id))
    referrals = result.scalars().all()
    if not referrals:
        raise HTTPException(
            status_code=404, detail="No referrals found for this referrer"
        )
    return referrals
