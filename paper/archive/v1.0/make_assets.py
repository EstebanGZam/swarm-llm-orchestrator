"""Numbers and figures for the paper, computed from the experiment logs (no hand-typed results).

Paper V1.0 (DeepSeek study). Run:  python paper/archive/v1.0/make_assets.py
Reads notebook/archive/v3_deepseek/results_deepseek and .../results_ollama (paper V1.0); writes paper/figs/*.pdf and paper/numbers.json
and prints the tables used in main.tex.
"""
import json, math, random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]   # paper/archive/v1.0 -> repository root
V3 = ROOT / "notebook" / "archive" / "v3_deepseek"
DS, OL = V3 / "results_deepseek", V3 / "results_ollama"
FIGS = HERE / "figs"; FIGS.mkdir(exist_ok=True)

def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")] if Path(p).exists() else []

# ---------------------------------------------------------------- data (current design only: max output 2048)
runs = pd.DataFrame(list({r["run_id"]: r for r in jl(DS / "runs.jsonl")}.values()))
keep = set(runs.attempt_id)
calls = pd.DataFrame([c for c in jl(DS / "calls.jsonl") if c["attempt_id"] in keep])
calls = calls.merge(runs[["run_id", "domain", "config", "arch", "n"]], on="run_id")
ledger = pd.DataFrame(jl(DS / "spend_ledger.jsonl"))

# rubric (blind LLM-assistant rater) for Cartagena
key = pd.read_csv(DS / "human_eval" / "_key_do_not_open.csv")
rat = pd.read_csv(DS / "human_eval" / "ratings_claude.csv")
CRIT = [f"c{i}" for i in range(1, 8)]
rat["rubric"] = rat[CRIT].mean(axis=1)
rub = key.merge(rat[["item_id", "rubric"] + CRIT], on="item_id")
runs = runs.merge(rub[["run_id", "rubric"]], on="run_id", how="left")
runs.loc[runs.domain == "travel", "quality"] = runs.loc[runs.domain == "travel", "rubric"]
judge = pd.DataFrame(jl(DS / "judge.jsonl")).drop_duplicates("run_id", keep="last")
runs = runs.merge(judge[["run_id", "judge_score"]], on="run_id", how="left")

CONFIGS = ["single", "hier-2", "hier-4", "mesh-2", "mesh-4"]
# Figure labels are in Spanish on purpose: these figures belong to the paper, which is written in Spanish.
LABEL = {"single": "único", "hier-2": "jer-2", "hier-4": "jer-4", "mesh-2": "malla-2", "mesh-4": "malla-4"}
DOMS = ["gsm8k", "math", "travel"]
DNAME = {"gsm8k": "GSM8K-Platinum", "math": "MATH-500 nivel 5", "travel": "Cartagena"}

def boot_ci(x, B=2000, seed=42):
    x = np.asarray(x, float)
    m = np.random.default_rng(seed).choice(x, size=(B, len(x)), replace=True).mean(axis=1)
    return np.percentile(m, [2.5, 97.5])

rows = []
for d in DOMS:
    for cfg in CONFIGS:
        g = runs[(runs.domain == d) & (runs.config == cfg)]
        lo, hi = boot_ci(g.quality)
        rows.append(dict(domain=d, config=cfg, runs=len(g), quality=g.quality.mean(), q_lo=lo, q_hi=hi,
                         calls=g.n_calls.mean(), messages=g.n_messages.mean(), tokens=g.total_tokens.mean(),
                         in_tokens=g.in_tokens.mean(), out_tokens=g.out_tokens.mean(),
                         usd_list=g.cost_usd_list.mean(), latency=g.latency_total_s.mean(), cp=g.latency_cp_s.mean(),
                         max_prompt=g.max_prompt_tokens.max(), judge=g.judge_score.mean() if d == "travel" else np.nan))
S = pd.DataFrame(rows)
for k in ("tokens", "usd_list", "latency"):
    S[k + "_x"] = S.apply(lambda r: r[k] / S[(S.domain == r.domain) & (S.config == "single")][k].iloc[0], axis=1)
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
print(S.round(4).to_string())

# per-stage tokens per run
stage = (calls.groupby(["domain", "config", "run_id", "stage"])[["in_tokens", "out_tokens"]].sum().sum(axis=1)
         .groupby(["domain", "config", "stage"]).mean().unstack(fill_value=0))
print("\nmean tokens per run by stage\n", stage.round(0))

# coordination on verifiable domains
coord = {}
for d in ("gsm8k", "math"):
    g = runs[(runs.domain == d) & (runs.arch != "single")]
    coord[d] = dict(swarm_runs=len(g), any_worker_wrong=int((g.frac_workers_correct < 1).sum()),
                    queen_kept=float((g.queen_outcome == "kept").mean()),
                    review_improved=int((g.get("review_effect") == "improved").sum()),
                    mesh_runs=int((g.arch == "mesh").sum()))
print("\ncoordination", coord)

# rubric per criterion and judge agreement
rj = runs[runs.domain == "travel"].merge(rub[["run_id"] + CRIT], on="run_id")
jcrit = pd.DataFrame(jl(DS / "judge.jsonl")).drop_duplicates("run_id", keep="last").set_index("run_id").judge_criteria
def kappa(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); po = np.mean(a == b)
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)
crit_rows = []
for c in CRIT:
    h = rj[c].astype(int).values; j = np.array([int(jcrit[r][c]) for r in rj.run_id])
    crit_rows.append(dict(criterion=c, rubric_rate=h.mean(), judge_rate=j.mean(), agree=(h == j).mean(), kappa=kappa(h, j)))
CR = pd.DataFrame(crit_rows); print("\n", CR.round(3).to_string())

# local pilot (Ollama): exploratory failure modes
ol = pd.DataFrame(list({r["run_id"]: r for r in jl(OL / "runs.jsonl")}.values()))
olc = pd.DataFrame(jl(OL / "calls.jsonl"))
loc = ol[ol.arch != "single"].groupby("model").agg(swarm_runs=("run_id", "count"), invalid_json=("plan_invalid_json", "sum"),
                                                   role_mismatch=("plan_role_mismatch", "sum"), final_trunc=("final_truncated", "sum"),
                                                   queen_lost=("queen_outcome", lambda x: int((x == "lost").sum())))
print("\nlocal pilot\n", loc, "\nlocal runs", len(ol), "calls", len(olc), "max prompt", olc.in_tokens.max(),
      "tok/s", olc.groupby("model").tok_per_s.mean().round(1).to_dict())

N = dict(
    runs=len(runs), calls=int(runs.n_calls.sum()), tokens=int(runs.total_tokens.sum()),
    billed_calls=len(ledger), spend_billed=float(ledger.cost_usd.sum()), spend_list=float(ledger.cost_usd_list.sum()),
    cache_hit=int(ledger.cache_hit_tokens.sum()), ledger_in=int(ledger.in_tokens.sum()),
    reasoning=int(ledger.reasoning_tokens.sum()), failures=int(runs.technical_failure.sum()),
    max_prompt=int(runs.max_prompt_tokens.max()), coord=coord,
    local_runs=len(ol), local_calls=len(olc), local_max_prompt=int(olc.in_tokens.max()),
)
(HERE / "numbers.json").write_text(json.dumps(N, indent=1, default=float))
print("\n", json.dumps(N, indent=1, default=float))

# ---------------------------------------------------------------- figures (IEEE column 3.5 in, text 7.16 in)
plt.rcParams.update({"font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                     "legend.fontsize": 6.5, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.25, "grid.linewidth": 0.5, "axes.linewidth": 0.6, "legend.frameon": False,
                     "pdf.fonttype": 42, "font.family": "DejaVu Sans"})
C_H, C_M, C_S = "#2a78d6", "#eb6834", "#7d8796"
INK = "#333333"

# Fig. 1: topologies
fig, axes = plt.subplots(1, 3, figsize=(3.5, 1.6))
def node(ax, x, y, label, color, r=0.15):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=3, lw=0))
    ax.text(x, y, label, ha="center", va="center", fontsize=5, color="white", zorder=4, fontweight="bold")
def edge(ax, a, b, color="#9aa3ae", lw=0.8, ls="-"):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=ls, zorder=1)
W = [(-0.75, -0.55), (-0.25, -0.55), (0.25, -0.55), (0.75, -0.55)]
Q = (0, 0.45)
for ax, title, sub in zip(axes, ["Agente único", "Jerárquica", "Malla"],
                          ["1 llamada · 0 mensajes", "n+2 llamadas · 2n mensajes", "2n+2 llamadas · n(n+1) mensajes"]):
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.45, 0.85); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=7, pad=1, color=INK)
    ax.text(0, -1.42, sub, ha="center", va="bottom", fontsize=5, color="#555555")
node(axes[0], 0, 0, "A", C_S, r=0.18)
for ax, mesh in ((axes[1], False), (axes[2], True)):
    for w in W:
        edge(ax, Q, w, color=C_H, lw=0.9)
    if mesh:
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = W[i], W[j]
                if j == i + 1:
                    edge(ax, a, b, color=C_M, lw=0.9)
                else:   # arcs below the workers for non-adjacent pairs
                    xs = np.linspace(a[0], b[0], 30); h = 0.12 + 0.07 * (j - i)
                    ax.plot(xs, a[1] - h * np.sin(np.pi * (xs - a[0]) / (b[0] - a[0])), color=C_M, lw=0.8, zorder=1)
    node(ax, *Q, "R", "#2b3440")
    for k, w in enumerate(W, 1):
        node(ax, *w, str(k), C_H)
fig.tight_layout(pad=0.2, w_pad=0.3)
fig.savefig(FIGS / "topologias.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 2: cost relative to the single agent vs n
fig, axes = plt.subplots(1, 3, figsize=(7.16, 1.6), sharey=True)
for ax, d in zip(axes, DOMS):
    s = S[S.domain == d]
    for arch, col, mk, lab in (("hier", C_H, "o", "Jerárquica"), ("mesh", C_M, "^", "Malla")):
        ss = s[s.config.str.startswith(arch)]
        xs = [int(c.split("-")[1]) for c in ss.config]
        ax.plot(xs, ss.usd_list_x, color=col, marker=mk, ms=4, lw=1.4, label=lab)
        for x, y in zip(xs, ss.usd_list_x):
            ax.annotate(f"{y:.1f}×", (x, y), textcoords="offset points", xytext=(-6, 3) if x == 2 else (6, -2),
                        ha="right" if x == 2 else "left", fontsize=6, color=INK)
    ax.axhline(1, color=C_S, lw=0.9, ls=":", label="Agente único = 1")
    ax.set(title=DNAME[d], xlabel="Obreros (n)", xticks=[2, 4], xlim=(1.25, 4.9), ylim=(0, 18))
axes[0].set_ylabel("Costo por corrida / agente único")
axes[0].legend(loc="upper left")
fig.tight_layout(pad=0.3)
fig.savefig(FIGS / "costo_vs_n.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 3: quality vs relative cost
fig, axes = plt.subplots(1, 3, figsize=(7.16, 1.6), sharey=True)
for ax, d in zip(axes, DOMS):
    s = S[S.domain == d]
    for _, r in s.iterrows():
        col, mk = (C_S, "s") if r.config == "single" else (C_H, "o") if r.config.startswith("hier") else (C_M, "^")
        ax.errorbar(r.usd_list_x, r.quality, yerr=[[r.quality - r.q_lo], [r.q_hi - r.quality]], fmt=mk, color=col,
                    ms=4.5, elinewidth=0.8, capsize=1.5, zorder=3)
        if d == "travel" and r.config in ("hier-2", "mesh-2"):
            off, ha = (6, -3), "left"                         # off the error bars
        elif d == "travel" and r.config == "mesh-4":
            off, ha = (0, 6), "center"
        else:
            off, ha = ((0, -11) if r.config.startswith("mesh") else (0, 6)), "center"
        ax.annotate(LABEL[r.config], (r.usd_list_x, r.quality), textcoords="offset points", xytext=off, ha=ha, fontsize=5.8, color=INK)
    ax.set(title=DNAME[d], xscale="log", ylim=(0, 1.08), xlim=(0.8, 25))
    ax.set_xticks([1, 2, 5, 10, 20]); ax.set_xticklabels(["1", "2", "5", "10", "20"])
    ax.set_xlabel("Costo / agente único (escala log)")
axes[0].set_ylabel("Calidad")
axes[0].legend(handles=[Line2D([], [], color=C_S, marker="s", ls="", label="Agente único"),
                        Line2D([], [], color=C_H, marker="o", ls="", label="Jerárquica"),
                        Line2D([], [], color=C_M, marker="^", ls="", label="Malla")], loc="lower left")
fig.tight_layout(pad=0.3)
fig.savefig(FIGS / "calidad_vs_costo.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 4: where the tokens go (mean tokens per run by stage)
STAGES = [("single", "Agente único", C_S), ("plan", "Plan (reina)", "#2b3440"), ("work", "Trabajo (obreros)", C_H),
          ("review", "Revisión (malla)", C_M), ("integrate", "Integración (reina)", "#1baf7a")]
fig, axes = plt.subplots(1, 3, figsize=(7.16, 1.6))
for ax, d in zip(axes, DOMS):
    st = stage.loc[d].reindex(CONFIGS)
    bottom = np.zeros(len(CONFIGS))
    for key_, lab, col in STAGES:
        v = st[key_].fillna(0).values if key_ in st else np.zeros(len(CONFIGS))
        ax.bar(range(len(CONFIGS)), v / 1000, bottom=bottom / 1000, color=col, width=0.72, edgecolor="white", linewidth=0.6, label=lab)
        bottom += v
    for x, t in enumerate(bottom):
        ax.text(x, t / 1000, f"{t / 1000:.1f}", ha="center", va="bottom", fontsize=5.8, color=INK)
    ax.set_xticks(range(len(CONFIGS)), [LABEL[c] for c in CONFIGS])
    ax.set(title=DNAME[d], ylim=(0, bottom.max() / 1000 * 1.15))
axes[0].set_ylabel("Miles de tokens por corrida")
handles = [Patch(color=c, label=l) for _, l, c in STAGES]
fig.legend(handles=handles, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.06))
fig.tight_layout(pad=0.3, rect=(0, 0.08, 1, 1))
fig.savefig(FIGS / "tokens_por_etapa.pdf", bbox_inches="tight"); plt.close(fig)
print("figures written to", FIGS)
