"""Figures, tables and numbers for paper V2.0, from the tables written by the notebook (no hand-typed results).

Run from the repository root:  python paper/make_assets.py
Reads notebook/results_local/tables/*.csv (written by notebook V4.2, section 10) and notebook/results_local/hardware.json.
Writes paper/figs/*.pdf, paper/tabs/*.tex and paper/numbers.json, and prints the numbers quoted in the text.
Labels are in Spanish on purpose: they belong to the paper, which is written in Spanish.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "notebook" / "results_local"
TAB = RES / "tables"
FIGS = HERE / "figs"; FIGS.mkdir(exist_ok=True)
TABS = HERE / "tabs"; TABS.mkdir(exist_ok=True)

S = pd.read_csv(TAB / "summary.csv")
V = pd.read_csv(TAB / "votes.csv")
C = pd.read_csv(TAB / "contrasts.csv")
CO = pd.read_csv(TAB / "coordination.csv")
CD = pd.read_csv(TAB / "condorcet.csv")
KT = pd.read_csv(TAB / "kendall.csv")
MR = pd.read_csv(TAB / "mesh_review.csv")
CA = pd.read_csv(TAB / "cartagena.csv")
HW = json.loads((RES / "hardware.json").read_text())

FAMS = ["qwen", "llama"]
FNAME = {"qwen": "Qwen", "llama": "Llama"}
DOMS = ["gsm8k", "math", "travel"]
DNAME = {"gsm8k": "GSM8K", "math": "MATH niv.~5", "travel": "Cartagena"}
DPLAIN = {"gsm8k": "GSM8K", "math": "MATH nivel 5", "travel": "Cartagena"}
SWARMS = [f"{a}-{n}/{t}" for t in ("weak", "mixed") for a in ("hier", "mesh") for n in (2, 4)]
TEAM_ES = {"weak": "débil", "mixed": "mixto"}
ARCH_ES = {"hier": "jer", "mesh": "malla"}

def lab(cfg):
    if cfg == "single/strong":
        return "único fuerte"
    if cfg == "single/weak":
        return "único débil"
    shape, team = cfg.split("/")
    a, n = shape.split("-")
    return f"{ARCH_ES[a]}-{n} {TEAM_ES[team]}"

def get(fam, dom, cfg, col):
    r = S[(S.family == fam) & (S.domain == dom) & (S.config == cfg)]
    return float(r[col].iloc[0]) if len(r) else np.nan

def vote(fam, dom, k, col):
    r = V[(V.family == fam) & (V.domain == dom) & (V.k == k)]
    return float(r[col].iloc[0]) if len(r) else np.nan

def f2(x):
    return "--" if pd.isna(x) else f"{x:.2f}".replace("-", "$-$")

def f1(x):
    return "--" if pd.isna(x) else f"{x:.1f}"

# ------------------------------------------------------------------ numbers quoted in the text
N = {}
ver = S[S.domain != "travel"]
sw = ver[ver.arch != "single"]
N["runs_eval"] = int(S.runs.sum())
N["swarm_gpu_x_weak"] = [round(sw.gpu_s_x_weak.min(), 1), round(sw.gpu_s_x_weak.max(), 1)]
N["swarm_tokens_x_weak_max"] = round(sw.total_tokens_x_weak.max(), 1)
N["joule_per_gpu_s"] = [round((S.energy_j / S.gpu_s).min(), 1), round((S.energy_j / S.gpu_s).max(), 1)]
N["travel_gpu_x_weak"] = [round(S[(S.domain == "travel") & (S.arch != "single")].gpu_s_x_weak.min(), 1),
                          round(S[(S.domain == "travel") & (S.arch != "single")].gpu_s_x_weak.max(), 1)]
for fam in FAMS:
    for dom in ("gsm8k", "math"):
        g = S[(S.family == fam) & (S.domain == dom)]
        st = get(fam, dom, "single/strong", "gpu_s")
        mixed = g[g.team == "mixed"]
        N[f"{fam}_{dom}_mixed_gpu_x_strong"] = [round((mixed.gpu_s / st).min(), 1), round((mixed.gpu_s / st).max(), 1)]
        N[f"{fam}_{dom}_strong_gpu_x_weak"] = round(get(fam, dom, "single/strong", "gpu_s_x_weak"), 2)
N["largest_prompt"] = int(S.largest_prompt_tokens.max())
N["holm_significant"] = int((C.p_holm < 0.05).sum()); N["contrasts"] = len(C)
N["phi"] = [round(CD.mean_error_corr_phi.min(), 2), round(CD.mean_error_corr_phi.max(), 2)]
N["kendall"] = KT.round(3).to_dict(orient="records")
N["idle_w"] = round(HW["idle_power_w"], 2)
cart = CA.assign(kind=CA.arch.map({"single": "single", "hierarchical": "hier", "mesh": "mesh"}))
N["cartagena_by_arch"] = cart.groupby("kind").quality.mean().round(2).to_dict()
N["cartagena_trunc"] = cart.groupby("final_truncated").quality.mean().round(2).to_dict()
N["cartagena_trunc_n"] = int(cart.final_truncated.sum())
N["cartagena_criteria"] = cart[[f"c{i}" for i in range(1, 8)]].sum().astype(int).to_dict()
(HERE / "numbers.json").write_text(json.dumps(N, indent=1, ensure_ascii=False, default=str))
print(json.dumps(N, indent=1, ensure_ascii=False, default=str))

# ------------------------------------------------------------------ Table: main results (accuracy and GPU-seconds)
CELLS = [(f, d) for d in ("gsm8k", "math") for f in FAMS]
rows = [("single/strong", None), ("single/weak", None), (None, 3), (None, 5), (None, 9)] + [(c, None) for c in SWARMS]
lines = []
for cfg, k in rows:
    name = lab(cfg) if cfg else f"votación@{k} débil"
    cells = []
    for fam, dom in CELLS:
        if cfg:
            q, g = get(fam, dom, cfg, "quality"), get(fam, dom, cfg, "gpu_s")
        else:
            q, g = vote(fam, dom, k, "accuracy"), vote(fam, dom, k, "gpu_s")
        cells += [f2(q), f1(g)]
    for fam in FAMS:
        cells.append(f2(get(fam, "travel", cfg, "quality")) if cfg else "--")
    lines.append(name + " & " + " & ".join(cells) + r" \\")
    if cfg == "single/weak" or k == 9 or cfg == "mesh-4/weak":
        lines.append(r"\midrule")
(TABS / "main.tex").write_text("\n".join(lines) + "\n")

# best-in-column in bold is decided by the reader; we only mark nothing to keep the table neutral.

# ------------------------------------------------------------------ Table: contrasts summary (ranges of delta per cell, Holm count)
def rng(df):
    if df.empty:
        return "--"
    lo, hi = df.delta.min(), df.delta.max()
    s = f"{lo:+.2f}" if abs(hi - lo) < 0.005 else f"{lo:+.2f} a {hi:+.2f}"
    return s.replace("-", "$-$").replace("+", "$+$")

SPEC = [("H2", "swarm débil $-$ único débil", lambda c: c.str.contains("/weak − single/weak")),
        ("H3", "swarm débil $-$ votación", lambda c: c.str.contains("/weak − vote@")),
        ("H3", "swarm mixto $-$ votación", lambda c: c.str.contains("/mixed − vote@")),
        ("H4", "swarm mixto $-$ único fuerte", lambda c: c.str.contains("/mixed − single/strong")),
        ("H5", "swarm mixto $-$ débil", lambda c: c.str.contains(r"/mixed − (?:hier|mesh)-\d/weak"))]
lines = []
for h, name, sel in SPEC:
    sub = C[sel(C.contrast)]
    cells = [rng(sub[(sub.family == f) & (sub.domain == d)]) for f, d in CELLS]
    raw = int((sub.p_value < 0.05).sum()); holm = int((sub.p_holm < 0.05).sum())
    lines.append(f"{h} & {name} & " + " & ".join(cells) + f" & {raw}/{len(sub)} & {holm} \\\\")
(TABS / "contrasts.tex").write_text("\n".join(lines) + "\n")
print("\n", C[C.p_holm < 0.05].to_string())

# ------------------------------------------------------------------ Table: coordination failures on GSM8K (mean over the 4 shapes)
co = CO[CO.domain == "gsm8k"].copy()
co["team"] = co.config.str.split("/").str[1]
ss = S[(S.domain == "gsm8k") & (S.arch != "single")].copy()
ss["fail_final_trunc"] = ss.rate_final_truncated
mr = MR[MR.domain == "gsm8k"].copy(); mr["team"] = mr.config.str.split("/").str[1]
items = [("Plan inválido (JSON o roles)", "FM-1.1 (parcial)", lambda f, t: co[(co.family == f) & (co.team == t)].plan_failure),
         ("Reina descarta la respuesta correcta", "FM-2.5/3.3 (cand.)", lambda f, t: co[(co.family == f) & (co.team == t)].lost),
         ("Reina conserva la respuesta correcta", "--", lambda f, t: co[(co.family == f) & (co.team == t)].kept),
         ("Revisión de la malla mejora obreros", "--", lambda f, t: mr[(mr.family == f) & (mr.team == t)].improved),
         ("Revisión de la malla empeora obreros", "--", lambda f, t: mr[(mr.family == f) & (mr.team == t)].worsened)]
lines = []
for name, mast, fn in items:
    cells = []
    for f in FAMS:
        for t in ("weak", "mixed"):
            v = fn(f, t)
            cells.append(f"{v.min():.2f}--{v.max():.2f}" if len(v) else "--")
    lines.append(f"{name} & " + " & ".join(cells) + f" & {mast} \\\\")
(TABS / "coordination.tex").write_text("\n".join(lines) + "\n")

# ------------------------------------------------------------------ figures (IEEE column 3.5 in, text 7.16 in)
plt.rcParams.update({"font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                     "legend.fontsize": 6.3, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.25, "grid.linewidth": 0.5, "axes.linewidth": 0.6, "legend.frameon": False,
                     "pdf.fonttype": 42, "font.family": "DejaVu Sans"})
C_W, C_X, C_ST, C_WK, C_V = "#2a78d6", "#eb6834", "#1F2430", "#8A93A3", "#5E6675"
INK = "#333333"
MK = {"hier": "o", "mesh": "^"}

# Fig. 1: topologies and teams
fig, axes = plt.subplots(1, 3, figsize=(3.5, 1.65))
def node(ax, x, y, label, color, r=0.15):
    ax.add_patch(plt.Circle((x, y), r, color=color, zorder=3, lw=0))
    ax.text(x, y, label, ha="center", va="center", fontsize=5, color="white", zorder=4, fontweight="bold")
def edge(ax, a, b, color="#9aa3ae", lw=0.8):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=1)
W = [(-0.75, -0.55), (-0.25, -0.55), (0.25, -0.55), (0.75, -0.55)]
Q = (0, 0.45)
for ax, title, sub in zip(axes, ["Agente único", "Jerárquica", "Malla"],
                          ["1 llamada · 0 mensajes", "n+2 llamadas · 2n mensajes", "2n+2 llamadas · n(n+1) mensajes"]):
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.45, 0.85); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=7, pad=1, color=INK)
    ax.text(0, -1.42, sub, ha="center", va="bottom", fontsize=5, color="#555555")
node(axes[0], 0, 0, "A", C_WK, r=0.18)
for ax, mesh in ((axes[1], False), (axes[2], True)):
    for w in W:
        edge(ax, Q, w, color="#9aa3ae", lw=0.9)
    if mesh:
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = W[i], W[j]
                if j == i + 1:
                    edge(ax, a, b, color=C_X, lw=0.9)
                else:
                    xs = np.linspace(a[0], b[0], 30); h = 0.12 + 0.07 * (j - i)
                    ax.plot(xs, a[1] - h * np.sin(np.pi * (xs - a[0]) / (b[0] - a[0])), color=C_X, lw=0.8, zorder=1)
    node(ax, *Q, "R", C_ST)
    for k, w in enumerate(W, 1):
        node(ax, *w, str(k), C_W)
fig.tight_layout(pad=0.2, w_pad=0.3)
fig.savefig(FIGS / "topologias.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 2: accuracy vs GPU-seconds (the central comparison)
fig, axes = plt.subplots(1, 4, figsize=(7.16, 2.05))
for ax, (fam, dom) in zip(axes, [(f, d) for d in ("gsm8k", "math") for f in FAMS]):
    v = V[(V.family == fam) & (V.domain == dom)].sort_values("k")
    ax.plot(v.gpu_s, v.accuracy, color=C_V, lw=1.0, ls="--", marker=".", ms=3, zorder=2)
    for _, r in v.iterrows():
        if r.k in (1, 9):
            ax.annotate(f"k={int(r.k)}", (r.gpu_s, r.accuracy), textcoords="offset points", xytext=(0, 4), ha="center",
                        fontsize=5.3, color=C_V)
    for cfg, col in (("single/strong", C_ST), ("single/weak", C_WK)):
        ax.scatter(get(fam, dom, cfg, "gpu_s"), get(fam, dom, cfg, "quality"), s=26, marker="s", color=col, zorder=4)
    for cfg in SWARMS:
        shape, team = cfg.split("/"); a, n = shape.split("-")
        col = C_W if team == "weak" else C_X
        ax.scatter(get(fam, dom, cfg, "gpu_s"), get(fam, dom, cfg, "quality"), s=22, marker=MK[a], zorder=3, linewidths=0.9,
                   facecolors=col if n == "4" else "white", edgecolors=col)
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10, subs=(1, 2, 5)))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set(title=f"{FNAME[fam]} · {DPLAIN[dom]}", ylim=(0, 0.9), xlabel="GPU-segundos por corrida (log)")
axes[0].set_ylabel("Exactitud")
handles = [Line2D([], [], color=C_ST, marker="s", ls="", label="Único fuerte"),
           Line2D([], [], color=C_WK, marker="s", ls="", label="Único débil"),
           Line2D([], [], color=C_V, marker=".", ls="--", label="Votación@k (débil)"),
           Line2D([], [], color=C_W, marker="o", ls="", label="Swarm débil"),
           Line2D([], [], color=C_X, marker="o", ls="", label="Swarm mixto"),
           Line2D([], [], color=INK, marker="o", ls="", mfc="white", label="jerárquica"),
           Line2D([], [], color=INK, marker="^", ls="", mfc="white", label="malla"),
           Line2D([], [], color=INK, marker="o", ls="", mfc="white", mew=0.9, label="n=2 (hueco)"),
           Line2D([], [], color=INK, marker="o", ls="", label="n=4 (relleno)")]
fig.legend(handles=handles, loc="lower center", ncol=9, bbox_to_anchor=(0.5, -0.03), handletextpad=0.2, columnspacing=0.8)
fig.tight_layout(pad=0.3, rect=(0, 0.08, 1, 1))
fig.savefig(FIGS / "exactitud_vs_gpu.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 3: GPU-seconds relative to the weak single agent vs n
fig, axes = plt.subplots(2, 3, figsize=(7.16, 2.9), sharex=True)
for i, fam in enumerate(FAMS):
    for j, dom in enumerate(DOMS):
        ax = axes[i][j]; ends = []
        for team, col in (("weak", C_W), ("mixed", C_X)):
            for a, ls in (("hier", "-"), ("mesh", "--")):
                ys = [1.0] + [get(fam, dom, f"{a}-{n}/{team}", "gpu_s_x_weak") for n in (2, 4)]
                ax.plot([0, 2, 4], ys, color=col, ls=ls, marker=MK[a], ms=3.5, lw=1.1)
                ends.append([ys[-1], col])
        top = max(e[0] for e in ends); gap = 0.085 * top        # end labels, nudged apart so they never overlap
        ends.sort(key=lambda e: e[0]); pos = []
        for yv, col in ends:
            yp = max(yv, pos[-1] + gap) if pos else yv; pos.append(yp)
            ax.annotate(f"{yv:.1f}×", (4, yv), xytext=(4.2, yp), textcoords="data", va="center", fontsize=5.5, color=col)
        st = get(fam, dom, "single/strong", "gpu_s_x_weak")
        ax.axhline(st, color=C_ST, lw=0.9, ls=":")
        ax.set(xticks=[0, 2, 4], xlim=(-0.3, 5.0), ylim=(0, None), title=f"{FNAME[fam]} · {DPLAIN[dom]}")
        if i == 1:
            ax.set_xticklabels(["único", "n=2", "n=4"])
        if j == 0:
            ax.set_ylabel("GPU-s / único débil")
handles = [Line2D([], [], color=C_W, label="Swarm débil"), Line2D([], [], color=C_X, label="Swarm mixto"),
           Line2D([], [], color=INK, ls="-", marker="o", ms=3, label="jerárquica"),
           Line2D([], [], color=INK, ls="--", marker="^", ms=3, label="malla"),
           Line2D([], [], color=C_ST, ls=":", label="único fuerte")]
fig.legend(handles=handles, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(pad=0.3, h_pad=0.6, rect=(0, 0.05, 1, 1))
fig.savefig(FIGS / "costo_vs_n.pdf", bbox_inches="tight"); plt.close(fig)

# Fig. 4: coordination on GSM8K, queen outcome per swarm configuration + plan-failure rate
co = CO[CO.domain == "gsm8k"].copy()
order = [(f, c) for f in FAMS for c in SWARMS]
fig, ax = plt.subplots(figsize=(3.5, 2.5))
cats = [("kept", "conserva", "#1baf7a"), ("rescued", "rescata", C_W), ("lost", "descarta", C_X), ("none_correct", "ningún obrero acierta", "#c4c8cf")]
y = np.arange(len(order))[::-1]
left = np.zeros(len(order))
for key, name, col in cats:
    vals = np.array([float(co[(co.family == f) & (co.config == c)][key].iloc[0]) for f, c in order])
    ax.barh(y, vals, left=left, color=col, height=0.75, edgecolor="white", linewidth=0.5, label=name)
    left += vals
pf = np.array([float(co[(co.family == f) & (co.config == c)].plan_failure.iloc[0]) for f, c in order])
ax.scatter(pf, y, color="black", s=9, zorder=4, marker="D", label="plan inválido")
ax.set_yticks(y, [f"{FNAME[f]} {lab(c)}" for f, c in order], fontsize=5.6)
ax.set(xlim=(0, 1), xlabel="Fracción de corridas (GSM8K)")
ax.axhline(7.5, color="#888", lw=0.6)
ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.42, -0.42), fontsize=5.8)
ax.grid(axis="y", visible=False)
fig.tight_layout(pad=0.3)
fig.savefig(FIGS / "coordinacion.pdf", bbox_inches="tight"); plt.close(fig)
print("figures ->", FIGS, "· tables ->", TABS)
