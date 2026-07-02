"""Example tests. Offline, no network, no extra installs — pytest must stay green
on a fresh clone. Use tmp_path for any filesystem work (see the config fixture)."""

from __future__ import annotations

from pathlib import Path

from toolname.cli import main
from toolname.config import Config, load_config
from toolname.core import plan_actions

FIXTURE = Path(__file__).parent / "fixtures" / "config.example.yaml"


def test_load_config_reads_items():
    cfg = load_config(FIXTURE)
    assert cfg.items == ["alpha", "beta"]
    assert cfg.token_env == "TOOLNAME_TOKEN"


def test_token_resolves_from_env(monkeypatch):
    cfg = Config(token_env="TOOLNAME_TEST_TOKEN")
    assert cfg.token() is None
    monkeypatch.setenv("TOOLNAME_TEST_TOKEN", "s3cret")
    assert cfg.token() == "s3cret"


def test_plan_actions_is_pure():
    cfg = Config(items=["x", "y"])
    assert plan_actions(cfg) == ["process 'x'", "process 'y'"]


def test_run_defaults_to_dry_run(capsys):
    import json

    rc = main(["run", "-c", str(FIXTURE)])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["dry_run"] is True
    assert out["applied"] == []
    assert out["planned"] == ["process 'alpha'", "process 'beta'"]


def test_run_apply_marks_applied(capsys):
    import json

    rc = main(["run", "-c", str(FIXTURE), "--apply"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["dry_run"] is False
    assert out["applied"] == out["planned"]
