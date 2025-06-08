# src/__init__.py
from snowflake.snowpark import Session
from src.config import settings

# モジュール読み込み時に一度だけセッションを作成
# session = (
#     Session.builder.config("account", settings.snowflake_account)
#     .config("user", settings.snowflake_user)
#     .config("role", settings.snowflake_role)
#     .config("warehouse", settings.warehouse)
#     .config("database", settings.database)
#     .config("schema", settings.schema)
#     .create()
# )
session = Session.builder.config("local_testing", True).create()
