"""Config loader defaults, overrides, and environment lookup."""

from toolname.config import Config, load_config


def test_blank_yaml_uses_defaults(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("", encoding="utf-8")

    assert load_config(path) == Config()


def test_omitted_fields_use_defaults(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("unrelated: placeholder\n", encoding="utf-8")

    config = load_config(path)
    assert config.output_dir == "out"
    assert config.token_env == "TOOLNAME_TOKEN"
    assert config.items == []


def test_fields_can_be_overridden(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text(
        "output_dir: custom-out\ntoken_env: TOOLNAME_TEST_TOKEN\nitems:\n  - first\n  - second\n",
        encoding="utf-8",
    )

    config = load_config(path)
    assert config.output_dir == "custom-out"
    assert config.token_env == "TOOLNAME_TEST_TOKEN"
    assert config.items == ["first", "second"]


def test_token_reads_environment_when_called(monkeypatch):
    monkeypatch.delenv("TOOLNAME_TOKEN", raising=False)
    config = Config()
    monkeypatch.setenv("TOOLNAME_TOKEN", "first-placeholder")

    assert config.token() == "first-placeholder"


def test_token_reads_changed_environment(monkeypatch):
    monkeypatch.setenv("TOOLNAME_TOKEN", "first-placeholder")
    config = Config()
    assert config.token() == "first-placeholder"

    monkeypatch.setenv("TOOLNAME_TOKEN", "second-placeholder")
    assert config.token() == "second-placeholder"


def test_token_returns_none_after_environment_is_unset(monkeypatch):
    monkeypatch.setenv("TOOLNAME_TOKEN", "first-placeholder")
    config = Config()
    assert config.token() == "first-placeholder"

    monkeypatch.delenv("TOOLNAME_TOKEN")
    assert config.token() is None
