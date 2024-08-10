from typing import Optional
from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import exceptions, models, schemas

from models.db_helper import get_user_db
from models.models import User
from models.db_helper import db_helper
from referral_codes.repository import RefCodeRepository
from users.repository import UserRepository

SECRET = "SECRET"  # if needed. Change and move to config


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET  # if needed
    verification_token_secret = SECRET  # if needed

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def get(self, id: models.ID) -> models.UP:
        session = db_helper.get_scoped_session()
        user = await UserRepository.get_user_by_id(session=session, user_id=id)
        await session.remove()

        if user is None:
            raise exceptions.UserNotExists()

        return user

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
        if "code" in user_dict:
            referral_code = user_dict.pop("code")
            try:
                session = db_helper.get_scoped_session()
                referrer_id = await RefCodeRepository.get_user_id_by_refcode(
                    session=session, code=referral_code
                )
                user_dict["referrer_id"] = referrer_id
                await session.remove()
            except ValueError as e:
                await session.remove()
                raise HTTPException(status_code=400, detail=str(e))
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
