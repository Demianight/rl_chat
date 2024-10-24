from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    user: str
    password: str
    db: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@localhost:5432/{self.db}"


class TokenSettings(BaseModel):
    secret_key: str
    algorithm: str


class BotSettings(BaseModel):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    postgres: PostgresSettings
    token: TokenSettings
    bot: BotSettings

    debug: bool
    base_dir: Path = Path(__file__).resolve().parent.parent


settings = Settings()
