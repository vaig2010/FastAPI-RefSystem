from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///ref_codes.db"
    #db_echo: bool = False
    db_echo: bool = True
    
settings = Setting()