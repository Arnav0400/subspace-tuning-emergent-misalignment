#!/usr/bin/env python3
"""Copy the source-faithful article template to the GitHub Pages entry point."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "index.html").write_bytes((ROOT / "index.template.html").read_bytes())
print("Built index.html.")
