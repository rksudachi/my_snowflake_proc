import src.procedures.my_proc as my_mod
import pytest
from snowflake.snowpark import Session
from src.config import settings
import src
from importlib import reload


def test_business_logic_simple():
    assert my_mod.business_logic(2, 3) == 5


def test_my_proc_via_session(session):
    # Session を渡すだけで @sproc デコレータが有効化される
    result = my_mod.my_proc(session, 4, 6)
    assert result == 10


# def test_create_session(session, mocker):
#     dummy_builder = mocker.Mock()
#     # config().config().… のチェーン呼び出しに対応
#     dummy_builder.config.return_value = dummy_builder
#     # create() が返す値を「session フィクスチャ」にしておく
#     dummy_builder.create.return_value = session

#     # 2) Session.builder を置き換え
#     mocker.patch.object(Session, "builder", dummy_builder)

#     # 3) テスト対象呼び出し
#     sess = my_mod.create_session()

#     # 4) config() の呼び出し順序を検証
#     expected = [
#         mocker.call.config("account", settings.snowflake_account),
#         mocker.call.config("user", settings.snowflake_user),
#         mocker.call.config("role", settings.snowflake_role),
#         mocker.call.config("warehouse", settings.warehouse),
#         mocker.call.config("database", settings.database),
#         mocker.call.config("schema", settings.schema),
#     ]
#     assert dummy_builder.mock_calls[:6] == expected
#     dummy_builder.create.assert_called_once()

#     # 5) 戻り値が session フィクスチャそのものかを確認
#     assert sess is session


def test_main(session, mocker, capsys, monkeypatch):
    # mock_session = mocker.patch.object(
    #     my_mod, "create_session", return_value=session
    # )
    # monkeypatch.setattr(src, "session", session)
    # # mocker.patch.object(src, "session", return_value=session)

    # # コピーまで差し替え
    # monkeypatch.setattr(
    #     "src.procedures.my_proc.session", session, raising=False
    # )
    # # 念のためリロード
    # reload(my_mod)

    mock_business = mocker.patch.object(my_mod, "my_proc", return_value=1234)

    my_mod.main()
    captured = capsys.readouterr()
    # mock_session.assert_called_once_with()
    assert captured.out.strip() == "local business_logic result: 1234"
    mock_business.assert_called_once_with(session, 2, 3)
