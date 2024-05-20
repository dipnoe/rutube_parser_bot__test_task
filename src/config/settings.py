from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / '.env'


class DatabaseSettings(BaseSettings):
    host: str = Field("", env="DB_HOST", type=str)
    port: int = Field(5432, env="DB_PORT", type=int)
    user: str = Field("", env="DB_USER", type=str)
    password: str = Field("", env="DB_PASSWORD", type=str)
    name: str = Field("", env="DB_NAME", type=str)

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix='DB_',
        extra='ignore'
    )

    @property
    def uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RutubeSettings(BaseSettings):
    url: str = Field("", env="RUTUBE_URL", type=str)

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix='RUTUBE_',
        extra='ignore'
    )


class AppSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    rutube: RutubeSettings = RutubeSettings()


settings = AppSettings()
