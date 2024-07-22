from sqlalchemy import select, delete, update
from db.models import User, ReferallCode
from sqlalchemy.ext.asyncio import AsyncSession
from referral_codes.schemas import ReferralCodeBase


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
    ) -> ReferallCode:
        query = select(ReferallCode).where(User.id == user_id)
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model

    @classmethod
    async def update_users_code_id(
        cls, session: AsyncSession, user: User, refcode: ReferallCode
    ) -> User:
        user.code_id = refcode.id
        return user
