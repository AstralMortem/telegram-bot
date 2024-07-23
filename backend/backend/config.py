from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = Path(__file__).parent.parent.parent.joinpath(".env")


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    WEBAPP_URL: str = "https://google.com"
    BACKEND_URL: str = "http://127.0.0.1:8000"
    VITE_BACKEND_URL: str = BACKEND_URL
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    WEBHOOK_PATH: str = "/webhook"

    CORS_ORIGINS: str = (
        "https://893f-91-226-254-123.ngrok-free.app,https://f8a3-91-226-254-123.ngrok-free.app"
    )

    INITIAL_GOLD_SUPPLY: int = 1000000000
    INITIAL_GOLD_PRICE: int = 1
    BOUNDING_CURVE_KOEF: float = 0.5

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()

WEBHOOK_URL: str = settings.BACKEND_URL + settings.WEBHOOK_PATH
