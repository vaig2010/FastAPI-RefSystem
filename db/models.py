from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

# class UserOrm(SQLAlchemyBaseUserTable[int], Base):
#     pass
    
class ReferallCodeOrm(Base):
    __tablename__ = "referral_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    created_date: Mapped[datetime]
    expiration_date: Mapped[datetime]
    user_id: Mapped[int]