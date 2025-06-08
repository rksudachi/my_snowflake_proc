import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    snowflake_account: str
    snowflake_user: str
    snowflake_role: str

    warehouse: str
    database: str
    schema: str

    class Config:
        env_prefix = "SNOWFLAKE_"
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config() -> Settings:
    # YAML 読み込み
    cfg_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    settings = Settings(**cfg)
    return settings


# .env 読み込み
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

settings = load_config()
