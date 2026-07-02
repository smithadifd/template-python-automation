"""Load and validate config.yaml into typed dataclasses.

The committed template is `config.example.yaml`; the real, local file is
`config.yaml` (gitignored). Secrets NEVER live in either file — a config field
names the *environment variable* that holds the secret (e.g. `token_env`), and
the code reads `os.environ[...]` at runtime. This mirrors the feed-condenser
pattern and satisfies standards/security.md (no secrets in committed files).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Top-level typed config. Extend with the fields your tool needs.

    `token_env` is the *name* of the env var holding an API token, not the token
    itself — resolve it lazily with `Config.token()` at the point of use.
    """

    # Where the tool writes its output; a real tool would add its own knobs here.
    output_dir: str = "out"
    # Name of the env var that holds the API token (value never committed).
    token_env: str = "TOOLNAME_TOKEN"
    # Arbitrary list of work items, just to show list parsing in the example.
    items: list[str] = field(default_factory=list)

    def token(self) -> Optional[str]:
        """Resolve the secret from the environment. Returns None if unset."""
        return os.environ.get(self.token_env)


def load_config(path: "str | Path" = "config.yaml") -> Config:
    """Parse a YAML config file into a `Config`. `yaml` is imported lazily so
    that merely importing this module stays stdlib-only and network-free."""
    import yaml  # lazy: keeps `import toolname` dependency-light

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return Config(
        output_dir=raw.get("output_dir", "out"),
        token_env=raw.get("token_env", "TOOLNAME_TOKEN"),
        items=list(raw.get("items", [])),
    )
