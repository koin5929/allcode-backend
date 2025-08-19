from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "allcode-backend"
    ENV: str = "prod"

    # JWT
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MIN: int = 30
    REFRESH_TOKEN_EXPIRES_DAYS: int = 14

    # CORS
    ALLOWED_ORIGINS: str = "*"  # 콤마 구분 또는 "*"

    # DB
    DATABASE_URL: str  # e.g. postgresql+psycopg2://user:pass@host:5432/dbname

    # Proxy Provider (stub)
    PROXY_PROVIDER_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
