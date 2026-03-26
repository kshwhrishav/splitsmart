from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator


class Settings(BaseSettings):
    app_name: str = "SplitSmart API"

    database_url: str
    alembic_database_url: str | None = None

    auth0_domain: str = ""
    auth0_audience: str = ""
    auth0_issuer: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def set_alembic_url(self):
        if not self.alembic_database_url:
            self.alembic_database_url = self.database_url
        return self


settings = Settings()