from sqlalchemy import select, delete
from db.models import ReferallCodeOrm
from sqlalchemy.ext.asyncio import AsyncSession
from referral_codes.schemas import ReferralCode, ReferralCodeBase
class RefCodeRepository:
    @classmethod
    async def add_code(cls, session: AsyncSession, data: ReferralCodeBase) -> int:
        code_dict = data.model_dump()
        code = ReferallCodeOrm(**code_dict)
        session.add(code)
        await session.commit()
        return code.id
    @classmethod
    async def get_codes(cls, session: AsyncSession,) -> list[ReferralCode]:
        query = select(ReferallCodeOrm)
        result = await session.execute(query)
        code_models = result.scalars().all()
        #code_schemas = [ReferralCode.model_validate(model) for model in code_models]
        return list(code_models)
    
    

            