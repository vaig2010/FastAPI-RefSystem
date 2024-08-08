from sqlalchemy import select, delete, update
from db.models import User, ReferralCode
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import ReferralCodeBase
from sqlalchemy.orm import selectinload, joinedload

class UserRepository:
    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user_model = result.scalars().first()
        return user_model

    @classmethod
    async def get_user_refcode(
        cls, session: AsyncSession, user_id: int
    ) -> ReferralCode:
        query = select(ReferralCode).options(selectinload(ReferralCode.user)).filter(ReferralCode.user_id == user_id)
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model

    @classmethod
    async def update_users_code_id(
        cls, session: AsyncSession, user: User, refcode: ReferralCode
    ) -> User:
        query = update(User).where(User.id == user.id).values(code_id=refcode.id)
        await session.execute(query)
        await session.commit()
        return user