from datetime import datetime, timedelta, timezone
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

class TimeSettings(BaseModel):
    @classmethod
    def datetime_now(self):
        return datetime.now(timezone.utc)
    @classmethod
    def datetime_expiration(self):
        return self.datetime_now() + timedelta(days=30)
    time_now = datetime_now
    time_exp = datetime_expiration
    

class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///ref_codes.db"
    db_echo: bool = False
    # db_echo: bool = True
    debug: bool = True
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    time_func: TimeSettings = TimeSettings()
    redis_url: str = 'redis://localhost'

settings = Setting()
