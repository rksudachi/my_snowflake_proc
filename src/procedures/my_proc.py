from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc
from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)


def business_logic(x: int, y: int) -> int:
    logger.info(f"business_logic: x={x}, y={y}")
    return x + y


@sproc(
    name="MY_PROC_ADD",
    is_permanent=False,
    statement_params={
        "QUERY_TAG": "my_proc_add",
    },
)
def my_proc(session: Session, x: int, y: int) -> int:
    """
    Snowflake 上にデプロイされる Python プロシージャ。
    """
    logger.info("Start my_proc")
    # 実際の処理はユニットテスト可能な関数に切り出す
    result = business_logic(x, y)
    logger.info(f"Result: {result}")
    return result


def create_session() -> Session:
    return (
        Session.builder.config("account", settings.snowflake_account)
        .config("user", settings.snowflake_user)
        .config("role", settings.snowflake_role)
        .config("warehouse", settings.warehouse)
        .config("database", settings.database)
        .config("schema", settings.schema)
        .create()
    )


def main():
    sess = create_session()
    res = my_proc(sess, 2, 3)
    print("local business_logic result:", res)


if __name__ == "__main__":
    main()
