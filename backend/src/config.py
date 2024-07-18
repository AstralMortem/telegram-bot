from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv(
        "BOT_TOKEN", "7235388130:AAEdsAs2kEqhi75Y1Ql8W_kdBElSFPJ_oFo"
    )
    FRONT_URL: str = "https://d10c-91-226-254-123.ngrok-free.app/"


settings = Settings()
