from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Quiz Master"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    """SERVER_MODE: ["dev", "build", "prod"]"""

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVER_MODE: str = "dev"


class DatabaseSettings(BaseSettings):
    """Add the .env file with these keys."""

    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/postgres"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Auth0Settings(BaseSettings):
    """Add the .env file with these keys."""

    DOMAIN: str = "domain"
    API_AUDIENCE: str = "api_audience"
    ISSUER: str = "issuer"
    ALGORITHMS: str = "RS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(CommonSettings, ServerSettings, DatabaseSettings, Auth0Settings):
    pass


settings = Settings()


def get_database_url():
    return settings.DATABASE_URL.replace("postgres://", "postgresql://")
