from sqlalchemy import select, delete
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import CreateUser
# idk why i need ReferralCode
class UserRepository:
    @classmethod
    async def add_user(cls, session: AsyncSession, user: CreateUser) -> int:
        user_dict = user.model_dump()
        user = User(**user_dict)
        session.add(user)
        await session.commit()
        return user.id
    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User]:
        query = select(User)
        result = await session.execute(query)
        user_models = result.scalars().all()
        return list(user_models)