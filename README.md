# A model- and domain-agnostic orchestrator for LLM agent swarms

**Julián Andrés Mendoza Castro · Esteban Gaviria Zambrano**
Artificial Intelligence (G1), Universidad Icesi, Cali, Colombia · October 2026

A queen–worker orchestrator in Python that runs the same code on any model backend and in any domain described as data. We use it to answer one question: **when does a swarm of LLM agents pay off?** In other words, when does adding agents and communication improve quality enough to justify the extra computation?

## Current study (V4.x): small local models, GPU-only

A first experiment with a strong API model (DeepSeek, notebook V3.4, now in `notebook/archive/`) solved 100% of the tasks with a single agent, so it could only show that coordination costs more. The current study uses **small local models**, for which a single agent still makes mistakes, so a benefit of the swarm could be measured if it existed.

| Factor | Design |
|---|---|
| Models | Qwen 2.5 (3B strong / 1.5B weak) and Llama 3.2 (3B strong / 1B weak), all **100% on one 4 GB GPU** |
| Teams | weak swarm (weak queen and workers); mixed swarm (strong queen, weak workers) |
| Architectures | single agent; hierarchical; mesh (adds an all-to-all review round), with *n* = 2 and 4 workers |
| Baselines | strong single agent, weak single agent, and **equal-compute majority voting** over *k* weak samples |
| Domains | GSM8K-Platinum (50 problems), MATH-500 level 5 (20), Cartagena trip plan (rubric) |
| Cost | GPU-seconds, GPU energy (integrated board power, 20 Hz), tokens, calls, wall time |
| Protocol | hypotheses H1–H8 and a difficulty-calibration rule fixed before running; paired per-problem tests with Holm correction |

**Main result** (3,640 evaluation runs, 10 hours of computation, no infrastructure failures). Accuracy, with GPU-seconds per run in brackets:

| | Qwen GSM8K | Llama GSM8K | Qwen MATH | Llama MATH |
|---|---|---|---|---|
| Strong single agent | **0.83** (1.7) | **0.74** (1.9) | **0.33** (7.7) | 0.10 (6.7) |
| Weak single agent | 0.62 (1.1) | 0.46 (1.1) | 0.14 (4.5) | 0.07 (4.9) |
| Weak-model voting, vote@5 | 0.74 (5.6) | 0.54 (5.5) | 0.10 (22.5) | 0.05 (24.7) |
| Weak swarms | 0.58–0.59 | 0.35–0.42 | 0.10–0.25 | 0.00–0.15 |
| Mixed swarms | 0.71–0.76 | 0.51–0.54 | 0.05–0.25 | 0.00–0.15 |

- **Cost.** Swarms cost 1.8–20.7× the weak single agent's GPU-seconds, and energy follows GPU-seconds.
- **The strong single agent wins.** Where a stronger model exists, using it alone was both better and cheaper than any swarm built around it. These are the only contrasts significant after Holm (Llama GSM8K, Δ ≈ −0.21).
- **Voting is at least as good as a weak swarm.** With only the weak model, majority voting over *k* samples matched or beat a swarm making the same number of calls.
- **The coordinator is the lever that helped.** Replacing only the queen with the strong model raised GSM8K accuracy by 0.11–0.19 and cut Llama's invalid plans from 81–92% to 22–39% of runs.
- **Cartagena (open task).** The rubric was applied blind by an LLM rater (Claude Opus 5.5), not by humans: single agents scored 0.61, mesh swarms 0.48 and hierarchical swarms 0.39.

The full analysis, hypothesis verdicts and limitations are in section 13 of the V4.2 notebook and in the paper.

## Contents

```
notebook/
  2026.10.12_Swarm_Notebook_EN_V4.2.ipynb   current notebook: analysis of the stored results, conclusions, table export
  2026.10.12_Swarm_Notebook_EN_V4.1.ipynb   previous version (same analysis, no table export)
  2026.10.11_Swarm_Notebook_EN_V4.0.ipynb   the same code as executed for the experiment (calibration, pilot, 10 h grid)
  results_local/
    runs.jsonl           one row per run: answer, accuracy, tokens, GPU-seconds, energy, failure flags
    calls.jsonl          one row per LLM call (prompt and generation time, tokens, energy)
    swaps.jsonl          model load/unload events, kept apart from the per-run costs
    hardware.json        GPU, driver, idle power, Ollama settings
    summary.csv          main results table
    tables/              analysis tables written by V4.2 (read by paper/make_assets.py)
    figures/             notebook figures
    human_eval/          blind Cartagena answers, rubric, the LLM rater's sheet and notes, answer key
                         (the folder keeps its original name; the rating is not human, see amendment C)
  archive/v3_deepseek/   first study (DeepSeek API, ceiling effect), behind paper V1.0
    2026.10.07_Demo_Swarm_Notebook_EN_V3.4.ipynb
    results_deepseek/, results_ollama/, pilots/
scripts/
  ollama_experiment_server.sh   Ollama server with the settings that keep every model 100% on GPU
paper/
  main.tex, main.pdf     paper V2.0 on the current study (IEEE format, in Spanish)
  make_assets.py         figures (figs/), table bodies (tabs/) and numbers.json from results_local/tables
  archive/v1.0/          paper V1.0 on the first (DeepSeek) study, with its own make_assets.py
docs/factcheck.md        primary-source check behind the paper's references
```

## Requirements

- Python 3.11 or later, then `pip install -r requirements.txt`.
- [Ollama](https://ollama.com) with `qwen2.5:3b`, `qwen2.5:1.5b`, `llama3.2:3b` and `llama3.2:1b`.
- An NVIDIA GPU for the energy metric (read through NVML).

## Reproducing

Start Jupyter from the `notebook/` folder: data and results paths are relative to it.

- **Analysis only, with no GPU and no server.** Open the V4.2 notebook, set `ANALYSIS_ONLY = True` and run all cells. Every run is identified by a deterministic id, so the notebook finds all 3,640 runs in `results_local/` and only recomputes tables, tests and figures.
- **Pipeline test.** Set `BACKEND = "mock"`. The fake answers go to `results_mock/` (ignored by git), and every output is stamped MOCK DATA.
- **Re-running the experiment.**
  1. Start `scripts/ollama_experiment_server.sh`; it listens on port 11435.
  2. Run up to section 8.3: environment checks, difficulty calibration, and a timing pilot that estimates the full grid.
  3. Set `RUN_FULL = True`. Runs that are already stored are never repeated, and a crash or a stop resumes where it left off.
- **Data.** GSM8K-Platinum and MATH-500 are downloaded from Hugging Face into `notebook/data/`, which git ignores.

## Rebuilding the paper

```bash
python paper/make_assets.py     # figures, table bodies and numbers.json from notebook/results_local/tables
```

- **On Overleaf or a full TeX Live:** upload `main.tex`, `IEEEtran.cls` and `figs/`, and compile with pdfLaTeX twice.
- **If your TeX lacks the Times fonts (`ptm`):** run `paper/build_local.sh`. It needs `t1utils` and the `urw-base35` fonts.

## Citation

```bibtex
@misc{mendoza2026swarm,
  author       = {Mendoza Castro, Juli{\'a}n Andr{\'e}s and Gaviria Zambrano, Esteban},
  title        = {A model- and domain-agnostic orchestrator for {LLM} agent swarms},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/EstebanGZam/swarm-llm-orchestrator}
}
```

## Data and licences

- **Code:** MIT licence (see `LICENSE`).
- **GSM8K-Platinum:** Vendrow et al., 2025; MIT.
- **MATH-500:** Lightman et al., 2023, a subset of MATH (Hendrycks et al., 2021); MIT.
- **Datasets:** neither is redistributed here; the notebook downloads them.
- **Models:** Qwen 2.5 (Apache 2.0 / Qwen licence) and Llama 3.2 (Llama 3.2 Community License), served by Ollama.
- **Cartagena answers:** generated by these models and included as experiment results.
