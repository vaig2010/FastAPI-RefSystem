from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy,
)
from core.config import settings


cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth_jwt.private_key_path.read_text(),
        lifetime_seconds=3600,
        algorithm=settings.auth_jwt.algorithm,
        public_key=settings.auth_jwt.public_key_path.read_text(),
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
