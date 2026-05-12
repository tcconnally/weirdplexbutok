"""Run static repo guards without requiring pytest."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_FILES = [
    ROOT / "tests" / "test_truthful_status.py",
]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    total = 0
    for path in TEST_FILES:
        module = load_module(path)
        for name in sorted(n for n in dir(module) if n.startswith("test_")):
            getattr(module, name)()
            total += 1
            print(f"PASS {name}")
    print(f"\n{total} static guard test(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
