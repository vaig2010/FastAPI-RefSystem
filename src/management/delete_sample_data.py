from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from models.db_helper import db_helper
from sqlalchemy.sql import text

SessionLocal = sessionmaker(
    bind=db_helper.engine, class_=AsyncSession, expire_on_commit=False
)


async def delete_sample_data(session: AsyncSession):
    # Delete users
    await session.execute(text("DELETE FROM users"))
    await session.commit()

    # Delete referral codes
    await session.execute(text("DELETE FROM referral_codes"))
    await session.commit()


async def main():
    async with SessionLocal() as session:
        await delete_sample_data(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    print("Sample data removed from database!")
