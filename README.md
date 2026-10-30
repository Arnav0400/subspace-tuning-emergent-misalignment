# Update Geometry Can Control Emergent Misalignment

Arnav Chavan, Samyak Jain, Kurt Keutzer.

[Read the blog](https://arnav0400.github.io/subspace-tuning-emergent-misalignment/).

The article follows the supplied draft's wording and section order, with the
merged AdamW/Muon figures. Changes are limited to factual corrections, figure captions,
and the optimizer comparisons. The draft's two
motivation passages are kept together under one heading; author planning notes
are not part of the published article.

The visualizer restores the side-by-side layout from the HTML/CSS export.
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
