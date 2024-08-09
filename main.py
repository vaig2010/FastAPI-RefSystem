from fastapi import FastAPI
from contextlib import asynccontextmanager
from referral_codes.router import router as refcodes_router
from users.router import router as users_router
from referrals.router import router as referrals_router
from auth.auth import auth_backend
from db.schemas import UserRead, UserCreate, UserUpdate, ReferralCodeBase
from auth.fastapi_users import fastapi_users
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from core.config import settings


# TODO: add tests
@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Referral Codes API",
)
app.include_router(refcodes_router)
app.include_router(users_router)
app.include_router(referrals_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)


@app.get("/")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
