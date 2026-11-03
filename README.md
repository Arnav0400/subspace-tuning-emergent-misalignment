# Update Geometry Can Control Emergent Misalignment

Arnav Chavan, Samyak Jain, Kurt Keutzer.

[Read the blog](https://arnav0400.github.io/subspace-tuning-emergent-misalignment/).

The article follows the supplied draft's section order, with the merged
AdamW/Muon figures. Motivation presents representation drift as a proposed
mechanism for emergent misalignment and includes an interactive activation probe.
The probe measures a local representation change; it does not establish that
this change causes EM. Author planning notes are not published.

The activation demo has one perturbation operation, a magnitude slider, and
single-band selection. Both plot axes and the smoothing bandwidth
stay fixed. It uses one real captured input from the pinned Qwen model, with
seeded perturbations of equal Frobenius norm across rank selections. Full
measurement details are in `data/activation-demo.json`.

`assets/activation-demo.fragment.html` is the editable, self-contained source
embedded into the article by `scripts/build.py`. Its bundled data and plotting
library make no model or network calls. `assets/activation-demo.html` is the
standalone export of the same fragment.

The response visualizer retains the side-by-side layout from the HTML/CSS export.
Colored outcome bars mark EM, other scored answers, and excluded answers.
An “EM in any model” checkbox filters sample slots while keeping every model
visible for comparison. A slider and previous/next buttons browse the responses.
It uses 4,000 saved responses from five models: base, AdamW SFT/SST90,
and Muon SFT/SST90. Template assignments are presented as numbered items or
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
