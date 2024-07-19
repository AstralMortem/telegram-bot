from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = Path(__file__).parent.parent.parent.joinpath(".env")


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    FRONT_URL: str = "https://google.com"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    CURVE_KOEF_A: float = 0.000001
    CURVE_KOEF_B: float = 0
    CURVE_KOEF_C: float = 1

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
