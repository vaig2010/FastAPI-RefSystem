from sqlalchemy import select, delete
from db.models import ReferallCodeOrm
from sqlalchemy.ext.asyncio import AsyncSession
from referral_codes.schemas import ReferralCode, ReferralCodeBase, ReferralCodeUpdatePartial
# idk why i need ReferralCode
class RefCodeRepository:
    @classmethod
    async def add_code(cls, session: AsyncSession, code: ReferralCodeBase) -> int:
        code_dict = code.model_dump()
        code = ReferallCodeOrm(**code_dict)
        session.add(code)
        await session.commit()
        return code.id
    @classmethod
    async def get_codes(cls, session: AsyncSession,) -> list[ReferallCodeOrm]:
        query = select(ReferallCodeOrm)
        result = await session.execute(query)
        code_models = result.scalars().all()
        #code_schemas = [ReferralCode.model_validate(model) for model in code_models]
        return list(code_models)
    
    @classmethod
    async def get_code(cls, session: AsyncSession, code_id: int) -> ReferallCodeOrm:
        return await session.get(ReferallCodeOrm, code_id)
    
    @classmethod
    async def update_code(cls, session: AsyncSession, 
                          code: ReferallCodeOrm,
                          code_update: ReferralCodeBase | ReferralCodeUpdatePartial,
                          partial: bool = False,
                          )-> ReferallCodeOrm:
        for name,value in code_update.model_dump(exclude_unset=partial).items():
            setattr(code, name, value)
        await session.commit()
        return code
    
    @classmethod
    async def delete_code(cls, session: AsyncSession, code: ReferallCodeOrm) -> None:
        await session.delete(code)
        await session.commit()
            