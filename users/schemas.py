from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

class User(CreateUser):
    id: int