from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Quiz Master"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    """SERVER_MODE: ["dev", "build", "prod"]"""

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVER_MODE = "dev"


class Settings(CommonSettings, ServerSettings):
    pass


settings = Settings()
