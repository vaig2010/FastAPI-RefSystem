from sqlalchemy.ext.asyncio import (async_sessionmaker, create_async_engine,
                                    async_scoped_session, AsyncSession)
from core.config import settings
from asyncio import current_task
#from fastapi_users.db import SQLAlchemyBaseUserTable
from .models import Base, User
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine =create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False
            )
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
            )
        return session
    
    async def session_dependency(self):
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess
            await session.remove()
            
        

db_helper = DatabaseHelper(settings.db_url, settings.db_echo)
    
async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        

async def drop_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
async def get_user_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
    