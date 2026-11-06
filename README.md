# Emergent Misalignment and the Geometry of Fine-Tuning

Arnav Chavan, Samyak Jain, Kurt Keutzer.

[Read the blog](https://arnav0400.github.io/subspace-tuning-emergent-misalignment/).

The article opens with a TL;DR and qualitative response comparison, followed by
the supplied draft's main text and merged AdamW/Muon figures.
Motivation presents representation drift as a proposed
mechanism for emergent misalignment and includes an interactive activation probe.
The probe measures a local representation change; it does not establish that
this change causes EM. Author planning notes are not published.

The activation demo has one perturbation operation, a magnitude slider, and
single-band selection. Both plot axes and the smoothing bandwidth stay fixed.
It uses one real captured input from the pinned Qwen model. Magnitude is the
fraction of the selected band's contribution removed: 0% leaves it unchanged,
and 100% removes it. The edit scales that band's original singular values.
Full measurement details are in `data/activation-demo.json`.

`assets/activation-demo.fragment.html` is the editable, self-contained source
embedded into the article by `scripts/build.py`. Its data and plotting library
share one script so the inline loader can execute it independently of other
script nodes. It makes no model or network calls. `assets/activation-demo.html` is the
standalone export of the same fragment.

The response visualizer groups five model cards into Base, AdamW, and Muon
comparisons. It shows only the six prompts with at least one saved EM flag;
the “EM in any model” filter is enabled by default. Turning it off exposes all
100 sample slots for each displayed prompt. A slider and previous/next buttons
browse the responses, with the filtered position and original sample number
shown separately. Colored outcome bars and counts always summarize all
100 responses for that prompt and model, regardless of the filter.
The downloadable data retains all 4,000 saved responses across all eight
prompts, including those without EM.
Template assignments are presented as numbered items or
labeled prose, with exact source responses available under “Original response.”
No live model calls are made.

## Edit and preview

Edit `index.template.html`, then run:

```sh
python3 scripts/build.py
python3 -m http.server 8000
```

Open `http://localhost:8000`. GitHub Pages serves the root of `main`.

The merged figures are in `assets/figure-1.svg`, `figure-2.svg`, and
`figure-3.svg`. PNG copies are included. The sample screenshot has been removed.
Verified metrics, response data, and provenance are in `data/`.

Source Serif 4 is bundled under the SIL Open Font License, included in
`assets/fonts/OFL.txt`.
