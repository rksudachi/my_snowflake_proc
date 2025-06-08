import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env から CONFIG_FILE_PATH も読み込む
load_dotenv()


class Settings(BaseSettings):
    snowflake_account: str
    snowflake_user: str
    snowflake_role: str

    warehouse: str
    database: str
    schema: str

    # （他に definitions_file などがあればここに追加）

    class Config:
        env_prefix = "SNOWFLAKE_"
        env_file = ".env"


def load_config() -> Settings:
    # 1) まず環境変数から設定ファイルパスを取得
    cfg_env = os.getenv("CONFIG_FILE_PATH")
    if cfg_env:
        cfg_path = Path(cfg_env)
    else:
        # 環境変数がセットされていなければ従来のデフォルト位置を使う
        cfg_path = Path(__file__).parents[1] / "config" / "config.yaml"

    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    # 2) YAML 読み込み
    with cfg_path.open(encoding="utf-8") as f:
        full_cfg = yaml.safe_load(f)

    # 3) 環境（dev|stg|prd）ごとのセクションを取り出し
    env = os.getenv("SNOWFLAKE_ENV", "dev")
    env_cfg = full_cfg.get(env)
    if env_cfg is None:
        raise ValueError(f"Unknown SNOWFLAKE_ENV: {env}")

    # 4) Pydantic でバリデーション
    return Settings(**env_cfg)


# 一度だけロード
settings = load_config()
