from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from contextlib import asynccontextmanager
from auth.manager import get_user_manager
from referral_codes.router import router as refcodes_router
from users.router import router as users_router

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate

from db.models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(lifespan=lifespan, title="Referral Codes API", )
app.include_router(refcodes_router)
app.include_router(users_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Using FastAPI instance
@app.get("/")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)