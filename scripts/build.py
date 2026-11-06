#!/usr/bin/env python3
"""Build the article, activation visualization, and filtered prompt choices."""
from hashlib import sha256
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
template = (ROOT / "index.template.html").read_text()
fragment = (ROOT / "assets" / "activation-demo.fragment.html").read_text()
data = json.loads((ROOT / "data" / "explorer.json").read_text())
prompts = [
    prompt for prompt in data["prompts"]
    if any(prompt["counts"][model["id"]]["flagged"] > 0 for model in data["models"])
]
default_prompt = data.get("defaults", {}).get("prompt")
if not any(prompt["id"] == default_prompt for prompt in prompts):
    default_prompt = prompts[0]["id"] if prompts else None
options = []
for prompt in prompts:
    selected = " selected" if prompt["id"] == default_prompt else ""
    options.append(
        f'<option value="{escape(prompt["id"], quote=True)}"{selected}>'
        f'{escape(prompt["question"])}</option>'
    )
replacements = {
    "<!-- ACTIVATION_DEMO -->": fragment,
    "<!-- EXPLORER_PROMPTS -->": "".join(options) or "<option>No prompts with EM</option>",
}
for marker, content in replacements.items():
    if template.count(marker) != 1:
        raise ValueError(f"The article must contain exactly one {marker} marker.")
    template = template.replace(marker, content)
for asset in (
    "assets/style.css", "assets/explorer.js", "assets/explorer.css",
    "assets/figure-1.svg", "assets/figure-2.svg", "assets/figure-3.svg",
    "assets/figure-1.png",
):
    version = sha256((ROOT / asset).read_bytes()).hexdigest()[:12]
    template = template.replace(f'{asset}"', f'{asset}?v={version}"')
(ROOT / "index.html").write_text(template)
print("Built index.html.")
