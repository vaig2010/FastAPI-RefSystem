from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from datetime import datetime, timedelta
from tasks.tasks import generate_referral_code
from core.config import settings
from models.models import User, ReferralCode
import models.schemas as schemas
from users.repository import UserRepository

class RefCodeRepository:
    @classmethod
    async def add_code(
        cls, session: AsyncSession, code: schemas.ReferralCodeBase
    ) -> int:
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
        query = select(ReferralCode)
        result = await session.execute(query)
        code_models = result.scalars().all()
        code_schemas = [
            schemas.ReferralCode.model_validate(model) for model in code_models
        ]
        return list(code_schemas)

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
        code_update: schemas.ReferralCodeBase | schemas.ReferralCodeUpdatePartial,
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
    async def get_refcode_by_user(cls, session: AsyncSession, user: User) -> ReferralCode:
        query = select(ReferralCode).where(user.refcode_id == ReferralCode.id)
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model


    @classmethod
    async def create_user_refcode(
        cls, session: AsyncSession, validity_days: int
    ) -> ReferralCode:
        created_date = datetime.now()
        expiration_date = created_date + timedelta(days=validity_days)
        if settings.debug:
            result_code = generate_referral_code()
        else:
            result_code = generate_referral_code.delay().get()
        code = ReferralCode(
            code=result_code, created_date=created_date, expiration_date=expiration_date
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
        query = select(ReferralCode).join(ReferralCode.user).where(User.email == email)
        result = await session.execute(query)
        code_model = result.scalars().first()
        return code_model

    @classmethod
    async def get_user_id_by_refcode(cls, session: AsyncSession, code: str) -> int:
        query = (
            select(User.id, ReferralCode.expiration_date)
            .join(User.referral_code)
            .where(ReferralCode.code == code)
        )
        result = await session.execute(query)
        user_id, exp_date = result.all()[0]
        if user_id is None:
            raise ValueError("No user found with this referral code")
        elif exp_date < datetime.now():
            raise ValueError("Referral code expired")
        else:
            return user_id
