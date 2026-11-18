from unittest.mock import patch

import pytest

from app.cli import run_fetch
from app.core.retriever import AccessDeniedError, AuthenticationRequiredError


@pytest.mark.parametrize("error", [AuthenticationRequiredError(), AccessDeniedError()])
def test_fetch_reports_auth_errors_without_url(error, capsys):
    url = "https://user:SECRET@example.com/Private?token=SECRET#SECRET"
    with patch("app.core.retriever.get_context", side_effect=error) as get_context:
        with pytest.raises(SystemExit) as exc:
            run_fetch(url)

    assert exc.value.code == 1
    get_context.assert_awaited_once_with(url)
    captured = capsys.readouterr()
    assert not captured.out
    assert error.code in captured.err
    assert "SECRET" not in captured.err
