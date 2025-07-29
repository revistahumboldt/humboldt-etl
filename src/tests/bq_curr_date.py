import pytest
from datetime import date
import sys
from utils.bq_auth import AuthUtils


def test_extraction_aborts_for_today(monkeypatch):
    from utils.get_date import DateUtils  

    # Mock da autenticação e do cliente BigQuery
    class FakeClient:
        def query(self, query):
            class Result:
                def result(self_inner):
                    class Row:
                        def get(self_inner2, _):
                            return date.today()  # retorna hoje, forçando o erro
                    return [Row()]
            return Result()

    monkeypatch.setattr(AuthUtils, "bq_authenticate", lambda *_: FakeClient())

    # Testa se a função levanta SystemExit
    with pytest.raises(SystemExit) as e:
        DateUtils.get_bq_based_time_range("project", "dataset", "table")

    assert e.value.code == 1
