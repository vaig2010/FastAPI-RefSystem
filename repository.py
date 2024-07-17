from sqlalchemy import select
from sql_app.database import ReferallCodeOrm, async_session
from schemas import ReferralCode, ReferralCodeAdd
class RefCodeRepository:
    @classmethod
    async def add_code(cls, data: ReferralCodeAdd) -> int:
        async with async_session() as session:
            code_dict = data.model_dump()
            code = ReferallCodeOrm(**code_dict)
            session.add(code)
            await session.flush()
            await session.commit()
            return code.id
    @classmethod
    async def get_codes(cls) -> list[ReferralCode]:
        async with async_session() as session:
            query = select(ReferallCodeOrm)
            result = await session.execute(query)
            code_models = result.scalars().all()
            code_schemas = [ReferralCode.model_validate(model) for model in code_models]
            return code_schemas
            