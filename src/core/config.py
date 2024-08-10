from datetime import datetime, timedelta, timezone
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"

class TimeSettings(BaseModel):
    @classmethod
    def get_current_datetime(cls) -> datetime:
        return datetime.now(timezone.utc)
    def get_expiration_datetime(cls) -> datetime:
        return cls.get_current_datetime() + timedelta(days=30)
    
    
    datetime_now = get_current_datetime
    datetime_expiration = get_expiration_datetime
    

class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///ref_codes.db"
    db_echo: bool = False
    # db_echo: bool = True
    debug: bool = True
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    time_func: TimeSettings = TimeSettings()
    redis_url: str = 'redis://localhost'

settings = Setting()
