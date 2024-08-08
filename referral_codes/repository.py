from datetime import datetime, timedelta
from sqlalchemy import select, delete
from db.models import User, ReferralCode
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import ReferralCodeBase, ReferralCodeUpdatePartial
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload
from tasks.tasks import generate_referral_code

class RefCodeRepository:
    @classmethod
    async def add_code(cls, session: AsyncSession, code: ReferralCodeBase) -> int:
        code_dict = code.model_dump()
        code = ReferralCode(**code_dict)
        session.add(code)
        await session.commit()
        return code.id

    @classmethod
    async def get_codes(
        cls,
        session: AsyncSession,
    ) -> list[ReferralCode]:
        query = select(ReferralCode).options(selectinload(ReferralCode.user))
        result = await session.execute(query)
        code_models = result.scalars().all()
        # code_schemas = [ReferralCode.model_validate(model) for model in code_models]
        return list(code_models)

    @classmethod
    async def get_code(cls, session: AsyncSession, code_id: int) -> ReferralCode:
        return await session.get(
            ReferralCode, code_id, options=[joinedload(ReferralCode.user)]
        )

    @classmethod
    async def update_code(
        cls,
        session: AsyncSession,
        code: ReferralCode,
        code_update: ReferralCodeBase | ReferralCodeUpdatePartial,
        partial: bool = False,
    ) -> ReferralCode:
        for name, value in code_update.model_dump(exclude_unset=partial).items():
            setattr(code, name, value)
        await session.commit()
        return code

    @classmethod
    async def delete_code(cls, session: AsyncSession, code: ReferralCode) -> None:
        await session.delete(code)
        await session.commit()

    @classmethod
    async def create_user_refcode(
        cls, session: AsyncSession, user_id: int, validity_days: int
    ) -> ReferralCode:
        created_date = datetime.now()
        expiration_date = created_date + timedelta(days=validity_days)
        result_code = generate_referral_code.delay()
        code = ReferralCode(
            code=result_code.get(),
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
    async def get_code_by_email(cls, session: AsyncSession, email: str) -> ReferralCode:
        query = (
            select(ReferralCode)
            .join(User, User.id == ReferralCode.user_id)
            .filter(User.email == email)
        )
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model

    @classmethod
    async def get_user_id_by_refcode(cls, session: AsyncSession, code: str) -> int:
        query = select(ReferralCode).where(ReferralCode.code == code)
        result = await session.execute(query)
        ref_code: ReferralCode = result.scalars().first()
        if ref_code is None:
            raise ValueError("Referral code not found")
        elif ref_code.expiration_date < datetime.now():
            raise ValueError("Referral code expired")
        return ref_code.user_id
