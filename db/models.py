from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

# class UserOrm(SQLAlchemyBaseUserTable[int], Base):
#     pass

class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    referral_codes: Mapped[list["ReferallCode"]] = relationship(back_populates="user")
    
class ReferallCode(Base):
    __tablename__ = "referral_codes"
    code: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="referral_codes", uselist=False)
    
