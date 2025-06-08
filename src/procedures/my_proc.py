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
    session_parameters={
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


if __name__ == "__main__":
    # ローカル実行用スタブ（Session は接続不要でテスト用）
    class DummySession:
        pass

    print(settings)
    res = business_logic(2, 3)
    print("local business_logic result:", res)
