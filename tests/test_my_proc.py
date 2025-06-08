import pytest
from src.procedures.my_proc import business_logic, my_proc


class DummySession:
    pass


def test_business_logic_logging(caplog):
    caplog.set_level("INFO")
    result = business_logic(1, 2)
    assert result == 3
    assert "business_logic: x=1, y=2" in caplog.text


def test_my_proc_invokes_business_logic(mocker):
    # business_logic をモックして呼び出し回数だけ検証
    mock_bl = mocker.patch(
        "src.procedures.my_proc.business_logic", return_value=42
    )
    res = my_proc(DummySession(), 5, 7)
    mock_bl.assert_called_once_with(5, 7)
    assert res == 42
