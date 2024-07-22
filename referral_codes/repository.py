from datetime import datetime, timedelta
from sqlalchemy import select, delete
from db.models import User, ReferallCode
from sqlalchemy.ext.asyncio import AsyncSession
from referral_codes.schemas import ReferralCodeBase, ReferralCodeUpdatePartial
from sqlalchemy.exc import IntegrityError


class RefCodeRepository:
    def generate_referral_code():
        import uuid
        import hashlib

        # Generate a random UUID
        random_uuid = uuid.uuid4()

        # Create a SHA-256 hash of the UUID
        sha256_hash = hashlib.sha256(random_uuid.bytes).hexdigest()

        # Take the first 8 characters of the hash as the referral code
        referral_code = sha256_hash[:8].upper()
        return referral_code

    @classmethod
    async def add_code(cls, session: AsyncSession, code: ReferralCodeBase) -> int:
        code_dict = code.model_dump()
        code = ReferallCode(**code_dict)
        session.add(code)
        await session.commit()
        return code.id

    @classmethod
    async def get_codes(
        cls,
        session: AsyncSession,
    ) -> list[ReferallCode]:
        query = select(ReferallCode)
        result = await session.execute(query)
        code_models = result.scalars().all()
        # code_schemas = [ReferralCode.model_validate(model) for model in code_models]
        return list(code_models)

    @classmethod
    async def get_code(cls, session: AsyncSession, code_id: int) -> ReferallCode:
        return await session.get(ReferallCode, code_id)

    @classmethod
    async def update_code(
        cls,
        session: AsyncSession,
        code: ReferallCode,
        code_update: ReferralCodeBase | ReferralCodeUpdatePartial,
        partial: bool = False,
    ) -> ReferallCode:
        for name, value in code_update.model_dump(exclude_unset=partial).items():
            setattr(code, name, value)
        await session.commit()
        return code

    @classmethod
    async def delete_code(cls, session: AsyncSession, code: ReferallCode) -> None:
        await session.delete(code)
        await session.commit()

    @classmethod
    async def create_user_refcode(
        cls, session: AsyncSession, user_id: int, validity_days: int
    ) -> ReferallCode:
        created_date = datetime.now()
        expiration_date = created_date + timedelta(days=validity_days)
        code = ReferallCode(
            code=cls.generate_referral_code(),
            created_date=created_date,
            expiration_date=expiration_date,
            user_id=user_id,
        )
        session.add(code)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError("Referral code for this user already exists.")
        return code

    @classmethod
    async def get_code_by_email(cls, session: AsyncSession, email: str) -> ReferallCode:
        query = (
            select(ReferallCode)
            .join(User, User.id == ReferallCode.user_id)
            .filter(User.email == email)
        )
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model
