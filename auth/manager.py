from typing import Optional
from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import exceptions, models, schemas
from db.db_helper import get_user_db
from db.models import User
from db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from referral_codes.repository import RefCodeRepository

SECRET = "SECRET"  # TODO: Change and move to config


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        referral_code = user_dict.pop("referral_code")
        try:
            session = db_helper.get_scoped_session()
            referrer_id = await RefCodeRepository.get_user_id_by_refcode(
                session=session, code=referral_code
            )
            user_dict["referrer_id"] = referrer_id
            await session.aclose()
        except ValueError:
            raise HTTPException(status_code=404, detail="Referral code not found")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
