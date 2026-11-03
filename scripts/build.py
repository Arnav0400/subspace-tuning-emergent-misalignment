#!/usr/bin/env python3
"""Build the article with its self-contained activation visualization."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
template = (ROOT / "index.template.html").read_text()
marker = "<!-- ACTIVATION_DEMO -->"
if template.count(marker) != 1:
    raise ValueError("The article must contain exactly one activation-demo marker.")
fragment = (ROOT / "assets" / "activation-demo.fragment.html").read_text()
(ROOT / "index.html").write_text(template.replace(marker, fragment))
print("Built index.html.")
