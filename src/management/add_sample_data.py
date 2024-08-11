from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from models.models import User, ReferralCode
from models.db_helper import db_helper
from fastapi_users.password import PasswordHelper

# Create an asynchronous engine

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=db_helper.engine, class_=AsyncSession, expire_on_commit=False
)

password_helper = PasswordHelper()


async def add_sample_data(session: AsyncSession):
    # Add sample referral codes
    referral_code1 = ReferralCode(code="REFCODE1")
    referral_code2 = ReferralCode(code="REFCODE2")
    session.add(referral_code1)
    session.add(referral_code2)
    await session.commit()

    user1 = User(
        email="user1@example.com",
        hashed_password=password_helper.hash("password1"),
        refcode_id=referral_code1.id,
        is_superuser=True,
    )
    user2 = User(
        email="user2@example.com",
        hashed_password=password_helper.hash("password2"),
        refcode_id=referral_code2.id,
    )
    session.add(user1)
    await session.commit()
    user3 = User(
        email="user3@example.com",
        hashed_password=password_helper.hash("password3"),
        referrer_id=user1.id,
    )
    session.add(user2)
    session.add(user3)
    await session.commit()


async def main():
    async with SessionLocal() as session:
        await add_sample_data(session)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    print("Sample data added to the database!")
