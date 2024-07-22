from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///ref_codes.db"
    db_echo: bool = False
    # db_echo: bool = True
    auth_jwt: AuthJWTSettings = AuthJWTSettings()


settings = Setting()
