from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = Path(__file__).parent.parent.parent.joinpath(".env")


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    WEBAPP_URL: str = "https://google.com"
    BACKEND_URL: str = "http://127.0.0.1:8000"
    VITE_BACKEND_URL: str = BACKEND_URL
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    WEBHOOK_PATH: str = '/webhook'

    CORS_ORIGINS: str = ""

    CURVE_KOEF_A: float = 0.000001
    CURVE_KOEF_B: float = 0
    CURVE_KOEF_C: float = 1

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()

WEBHOOK_URL: str = settings.BACKEND_URL + settings.WEBHOOK_PATH
print(WEBHOOK_URL)
