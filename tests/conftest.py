import os
from types import SimpleNamespace
import pytest
from snowflake.snowpark import Session
from src.config import settings


# ───────────────────────────────────────────────────────────────
# 1) CLIオプションの追加
# ───────────────────────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--snowflake-env",
        action="store",
        default="local",
        choices=["local", "prod"],
        help="Snowflake接続モード (local|prod)",
    )


# ───────────────────────────────────────────────────────────────
# 2) テスト起動前に一度だけ呼ばれる hook でセッションを生成
# ───────────────────────────────────────────────────────────────
# モジュール外に置いておくことで、「フィクスチャ関数の外側」で作成可能
_session = None


def pytest_configure(config):
    global _session
    mode = config.getoption("--snowflake-env")
    builder = Session.builder

    if mode == "local":
        # ローカルテスト用モード
        _session = builder.config("local_testing", True).create()
    else:
        # 本番接続モード
        _session = (
            builder.config("account", settings.snowflake_account)
            .config("user", settings.snowflake_user)
            .config("role", settings.snowflake_role)
            .config("warehouse", settings.warehouse)
            .config("database", settings.database)
            .config("schema", settings.schema)
            .create()
        )


# ───────────────────────────────────────────────────────────────
# 3) テスト内で使うセッションフィクスチャ
# ───────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def session():
    """
    pytest_configureで作成された _session を返すだけ。
    フィクスチャ本体の外側で一度だけ初期化済みなので高速です。
    """
    return _session


@pytest.fixture(autouse=True)
def patch_src_session(monkeypatch):
    import src

    # session = SimpleNamespace()
    monkeypatch.setattr(src, "session", _session)
    monkeypatch.setattr(
        "src.procedures.my_proc.session", _session, raising=False
    )
    return _session
