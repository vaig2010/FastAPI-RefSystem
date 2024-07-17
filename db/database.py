from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable
engine =create_async_engine('sqlite+aiosqlite:///ref_codes.db')

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# class UserOrm(SQLAlchemyBaseUserTable[int], Base):
#     pass
    
class ReferallCodeOrm(Base):
    __tablename__ = "referral_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    created_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    user_id: Mapped[int]
    
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)