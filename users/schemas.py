from pydantic import BaseModel, ConfigDict, EmailStr

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(CreateUser):
    id: int
    model_config = ConfigDict(from_attributes=True)