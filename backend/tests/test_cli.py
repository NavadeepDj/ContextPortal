import sys
from unittest.mock import patch

import pytest

from app import get_current_version
from app.cli import main, run_fetch
from app.core.retriever import AccessDeniedError, AuthenticationRequiredError


def test_version_flag_exits_without_a_subcommand(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["contextportal", "--version"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 0
    assert capsys.readouterr().out == f"contextportal {get_current_version()}\n"


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
