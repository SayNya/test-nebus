from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict



class DatabaseSettings(BaseModel):
    name: str = "catalog"
    host: str = "localhost"
    port: int = "5432"
    username: str = "postgres"
    password: str = "postgres"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class LoggingSettings(BaseModel):
    format: bool = False
    level: str = "DEBUG"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )

    debug: bool = True

    root_dir: Path
    src_dir: Path

    database: DatabaseSettings = DatabaseSettings()

    logging: LoggingSettings = LoggingSettings()



ROOT_PATH = Path(__file__).parent.parent.parent

settings = Settings(
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)
