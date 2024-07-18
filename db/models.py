from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    code_id: Mapped[int] = mapped_column(nullable=True)


# class User(Base):
#     __tablename__ = "users"
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str] = mapped_column(unique=True)
#     password: Mapped[str]
#     referral_codes: Mapped[list["ReferallCode"]] = relationship(back_populates="user")
    
    
    
class ReferallCode(Base):
    __tablename__ = "referral_codes"
    code: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #user: Mapped["User"] = relationship(back_populates="referral_codes", uselist=False)
    
