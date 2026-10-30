# Can subspace tuning limit emergent misalignment?

A static research blog by Arnav Chavan, Samyak Jain, and Kurt Keutzer.

**Live site:** https://arnav0400.github.io/subspace-tuning-emergent-misalignment/

The article studies fixed-basis subspace tuning on Qwen2.5-Coder-32B-Instruct
after one epoch on 6,000 insecure-code examples. It presents verified
insecure-code uptake, MMLU-Pro, conditional EM, coverage, and exact
denominators. A separately labeled Muon follow-up is included.

The response explorer contains 3,200 saved outputs: eight prompts, 100
samples per prompt, and four models. Its only controls are the question
selector, model buttons, and previous/next sample buttons. No model API
calls, analytics, external scripts, or runtime dependencies are used.

## Important interpretation

The headline EM metric averages each question's misaligned/eligible rate,
giving eligible questions equal weight. It is not the pooled answer rate.
For the selected AdamW runs, SST90 reduces this conditional rate from 8.58%
to 4.15%, while eligible-answer coverage rises from 19.52% to 83.06%.
SST90 has **116 flagged answers versus SFT's 55**, out of 4,800 generations
each. The article reports both observations.

Results use one training seed and post-hoc model selection on 100 ID
prompts. Similar observed insecure-code uptake does not establish
statistical equivalence. Insecure-code uptake is not functional coding
accuracy. The original study's question set was preregistered; this SST
model selection was not.

## Files

- `index.template.html` — editable article.
- `index.html` — generated, directly deployable article.
- `assets/style.css`, `assets/site.js` — layout and navigation.
- `assets/explorer.js` — simplified saved-response explorer.
- `data/results.json` — all main runs, exact counts, alternative EM
  aggregations, format/category results, provenance hashes, and Muon follow-up.
- `data/results.csv` — flat results for all nine main trained models and base.
- `data/explorer.json` — 3,200 saved responses, scores, and provenance.
- `data/qualitative.json` — seven selected comparisons, including a remaining
  SST failure, with exact prompts and completions.
- `data/muon.json` — separately labeled follow-up.
- `scripts/plot_results.py` — figures generated from the included results.

## Edit and preview

```sh
python3 scripts/build.py
python3 -m http.server 8000
```

Open `http://localhost:8000`. Fetching the saved responses requires HTTP;
opening `index.html` directly as a `file:` URL may block the explorer.

To regenerate the figures:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-figures.txt
.venv/bin/python scripts/plot_results.py
python3 scripts/build.py
```

GitHub Pages serves the repository root on `main`. `.nojekyll` keeps the
deployment static. No application build is needed for hosting.

## Verification and provenance

The published main metrics were checked against saved evaluation summaries.
The EM audit independently reaggregated 72,000 scored answers across 40
files for the ten included main models. The visualizer's trained-model
responses match the existing explorer; matching untouched-base responses
were verified against the original scored records by prompt and sample slot.
Selected qualitative records were checked against exact source lines and hashes.

The public data retain scientific run IDs and source hashes. Local paths,
private storage locations, and infrastructure identifiers are omitted.
No new training, answer generation, or judging was performed for this site.

The page was checked in Chromium at desktop, tablet, and mobile widths,
including the explorer's exact outputs, model switching, sample boundaries,
missing-data fallback, image loading, and internal links.

## Research and typography

- [Subspace tuning paper](https://arxiv.org/abs/2610.22293)
- [Pinned SST implementation](https://github.com/Arnav0400/SST/blob/07f42e580b2af07f43f66285150fa74deed17f40/sst_torch/optimizer.py)
- [Emergent Misalignment](https://arxiv.org/abs/2502.17424)

The writing and presentation follow the requested research-post references:
[Optimiser Choice Can Amplify or Suppress Emergent Misalignment](https://www.lesswrong.com/posts/Wq6CaAbiixoCEzbat/optimiser-choice-can-amplify-or-suppress-emergent-1)
and [How Can Post-Trained Models Continually Learn from Off-Policy Data?](https://ar-forum.github.io/grafting-web/).

Source Serif 4 is bundled under the SIL Open Font License; its copyright
notice and license are in `assets/fonts/OFL.txt`.
