from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from models.models import User


class UserRepository:
    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int) -> User:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.referral_code))
        )
        result = await session.execute(query)
        try:
            user_model = result.scalars().first()
        except NoResultFound:
            raise NoResultFound(f"User with ID {user_id} not found")
        return user_model

    @classmethod
    async def update_users_refcode_id(
        cls, session: AsyncSession, user: User, refcode_id: int
    ) -> User:
        query = update(User).where(User.id == user.id).values(refcode_id=refcode_id)
        await session.execute(query)
        await session.commit()
        return user
