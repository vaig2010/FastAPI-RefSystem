from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

"""
Note that the ORM’s “delete” and “delete-orphan” behavior applies only to the use of the Session.delete()
method to mark individual ORM instances for deletion within the unit of work process.
It does not apply to “bulk” deletes, which would be emitted using the delete() construct
as illustrated at ORM UPDATE and DELETE with Custom WHERE Criteria.
See Important Notes and Caveats for ORM-Enabled Update and Delete for additional background.
"""


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    refcode_id: Mapped[int] = mapped_column(
        ForeignKey("referral_codes.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    referrer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    referral_code: Mapped["ReferralCode"] = relationship(
        "ReferralCode", back_populates="user", uselist=False, cascade="all, delete"
    )


class ReferralCode(Base):
    __tablename__ = "referral_codes"
    code: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    user: Mapped["User"] = relationship("User", back_populates="referral_code")
