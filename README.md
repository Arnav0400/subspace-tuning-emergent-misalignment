# Update Geometry Can Control Emergent Misalignment

Arnav Chavan, Samyak Jain, Kurt Keutzer.

[Read the blog](https://arnav0400.github.io/subspace-tuning-emergent-misalignment/).

The article follows the supplied draft's wording and section order, with its
existing figures. Changes are limited to factual corrections, figure captions,
and a short note clarifying the conditional EM result. The draft's two
motivation passages are kept together under one heading; author planning notes
are not part of the published article.

The visualizer has a prompt selector, model buttons, and previous/next response
controls, with no checkboxes. It uses 3,200 saved responses from the existing
evaluation, with no live model calls.

## Edit and preview

Edit `index.template.html`, then run:

```sh
python3 scripts/build.py
python3 -m http.server 8000
```

Open `http://localhost:8000`. GitHub Pages serves the root of `main`.

The original figures are in `assets/figure-1.svg`, `figure-2.svg`,
`figure-3.svg`, and `qualitative-samples.svg`. PNG copies are included.
Verified metrics, response data, and provenance are in `data/`.

Source Serif 4 is bundled under the SIL Open Font License, included in
`assets/fonts/OFL.txt`.
