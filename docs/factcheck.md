# Fact-check: "Revisión Sistemas Multiagente LLM.md"

Access date for all web sources: **2026-10-06**. Verified against primary sources: arXiv abs/HTML/PDF, conference pages, official docs and pricing pages.

---

## 1. Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657)

**VERDICT: PARTIALLY CORRECT.** The 14 modes and their percentages in the research file are correct. The LLM-judge statistics are **wrong** because the file merges two separate numbers.

- **Latest version:** v3, 26 Oct 2025. https://arxiv.org/abs/2503.13657
- **Venue:** NeurIPS 2025, **Datasets & Benchmarks Track**, Spotlight Poster. Confirmed at https://neurips.cc/virtual/2025/poster/121528
- **Authors:** Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran, Klein, Ramchandran, Zaharia, Gonzalez, Stoica (UC Berkeley).
- **MAST-Data:** **1,642** annotated traces from **7 MAS frameworks**: ChatDev, MetaGPT, HyperAgent, AppWorld, AG2 (MathChat), Magentic-One and OpenManus. Main models are the GPT-4 and Claude families. Qwen2.5-Coder and CodeLlama are also used (Table 1).
- **How the taxonomy was built:** grounded theory on **150 traces** with 6 expert annotators.
- **Human inter-annotator agreement:** Cohen's κ = **0.88**.
- **LLM annotator:** OpenAI **o1**.
  - Few-shot o1: accuracy **0.94**, Cohen's κ **0.77** (Table 2: recall 0.77, precision 0.833, F1 0.80).
  - Zero-shot o1: accuracy 0.89, κ 0.58.
  - Out-of-domain check (OpenManus and Magentic-One on MMLU and GAIA): human IAA κ = 0.79.
  - **Correction:** the research file says "LLM judge: 94% agreement and κ = 0.88". That is wrong. The 0.88 is human-human agreement; the LLM-human κ is 0.77.
- **Failure rates:** the paper says "41% to 86.7% failure rate on 7 SOTA open-source MAS" (Intro; Fig. 5, App. B). Per-framework values exist only in the Fig. 5 image. I could not verify the file's numbers (ChatDev 41.4, MetaGPT 56.4, Magentic-One 78.6, OpenManus 86.7). Also note:
  - The Fig. 5 caption says "**six** popular MAS … benchmarks differ, therefore **not directly comparable**".
  - Calling these "production environments" ("entornos de producción") is wrong. They are benchmark runs.
- **+15.6%:** confirmed. It comes from adding a high-level task-objective verification step to **ChatDev on ProgramDev** (App. H, Table 5). It is a single case study, not a general effect.
- **Released artifacts, reusable:**
  - Repo: https://github.com/multi-agent-systems-failure-taxonomy/MAST. It contains `llm_judge_pipeline.ipynb` (the LLM-annotator prompt and pipeline) and `taxonomy_definitions_examples/`. The GitHub API reports **no license** for the repo, so cite it rather than copy it.
  - pip package `agentdash` (v0.1.0, MIT): `from agentdash import annotator`. It needs an OpenAI key.
  - Dataset: https://huggingface.co/datasets/mcemri/MAST-Data (CC-BY-4.0).
  - Definitions are in App. A. Examples are in App. N.

### The 14 MAST failure modes (official IDs, names, % of failures in MAST-Data, official definitions from App. A)

**FC1. System Design Issues: 43.8%**

| ID | Name | % | Official definition |
|---|---|---|---|
| FM-1.1 | Disobey task specification | 11.8 | "Failure to adhere to the specified constraints or requirements of a given task, leading to suboptimal or incorrect outcomes." |
| FM-1.2 | Disobey role specification | 1.5 | "Failure to adhere to the defined responsibilities and constraints of an assigned role, potentially leading to an agent behaving like another." |
| FM-1.3 | Step repetition | 15.7 | "Unnecessary reiteration of previously completed steps in a process, potentially causing delays or errors in task completion." |
| FM-1.4 | Loss of conversation history | 2.80 | "Unexpected context truncation, disregarding recent interaction history and reverting to an antecedent conversational state." |
| FM-1.5 | Unaware of termination conditions | 12.4 | "Lack of recognition or understanding of the criteria that should trigger the termination of the agents' interaction." |

**FC2. Inter-Agent Misalignment: 32.15%**

| ID | Name | % | Official definition |
|---|---|---|---|
| FM-2.1 | Conversation reset | 2.20 | "Unexpected or unwarranted restarting of a dialogue, potentially losing context and progress made in the interaction." |
| FM-2.2 | Fail to ask for clarification | 6.80 | "Inability to request additional information when faced with unclear or incomplete data, potentially resulting in incorrect actions." |
| FM-2.3 | Task derailment | 7.40 | "Deviation from the intended objective or focus of a given task, potentially resulting in irrelevant or unproductive actions." |
| FM-2.4 | Information withholding | 0.85 | "Failure to share or communicate important data or insights that an agent possess and could impact decision-making." |
| FM-2.5 | Ignored other agent's input | 1.90 | "Disregarding or failing to adequately consider input or recommendations provided by other agents in the system." |
| FM-2.6 | Reasoning-action mismatch | 13.2 | "Discrepancy between the logical reasoning process and the actual actions taken by the agent." |

**FC3. Task Verification: 24.05%**

| ID | Name | % | Official definition |
|---|---|---|---|
| FM-3.1 | Premature termination | 6.20 | "Ending a dialogue, interaction or task before all necessary information has been exchanged or objectives have been met." |
| FM-3.2 | No or incomplete verification | 8.20 | "(Partial) omission of proper checking or confirmation of task outcomes or system outputs, potentially allowing errors." |
| FM-3.3 | Incorrect verification | 9.10 | "Failure to adequately validate or cross-check crucial information or decisions during the iterations." |

The research file's table lists the same 14 percentages, but without IDs and in its own order. Section 06 of the file says "F3.1 Terminación Prematura" and "F2.4 Retención de Información". Use the official form instead: FM-3.1 and FM-2.4.

---

## 2. Wu et al., AutoGen (arXiv 2308.08155)

**VERDICT: WRONG.** The claim "+8% MATH, +6% HumanEval" does not appear in the paper.

- **Venue:** COLM 2024. It also won Best Paper at the ICLR 2024 LLM Agents Workshop. The arXiv comment only gives the page count.
- **What the paper reports on MATH** (Sec. A1, Fig. 4a, App. D), all with GPT-4:
  - **120 randomly selected Level-5 problems** (20 from each of 6 categories, geometry excluded):
    - AutoGen **52.5%**
    - Others in the figure: 48.33%, 45.0%, 30.0%, 26.67%, 23.33% (ChatGPT+Code Interpreter, ChatGPT+Plugin (Wolfram), vanilla GPT-4, Multi-Agent Debate, LangChain ReAct)
    - The figure layout makes the exact label-to-value mapping uncertain. The text confirms only that AutoGen is highest.
  - **Whole MATH test set (5,000 problems):** AutoGen **69.48%** vs GPT-4 **55.18%** (stated in App. D text).
- **HumanEval:** not evaluated in the AutoGen paper.
- **Where "8%" comes from:** A4 OptiGuide. On 100 coding tasks, multi-agent vs single-agent safeguard raises **F1 for identifying unsafe code** by 8% with GPT-4 and 35% with GPT-3.5-turbo.
- **"65% → 85% with GPT-4":** not found in the paper. Unsourced.

PDF: https://arxiv.org/pdf/2308.08155 (Fig. 4, App. D, A4 paragraph)

---

## 3. Zhuge et al., GPTSwarm (arXiv 2402.16823, ICML 2024, PMLR 235)

**VERDICT: PARTIALLY CORRECT.** The numbers are really from GPTSwarm, not from AgentPrune or G-Designer, but the research file misframes them.

- **Benchmarks:** MMLU (adversarial setting: k truthful IO agents + k adversarial agents), Mini Crosswords (20 problems, edge optimization), HumanEval (node/prompt optimization) and GAIA.
- **Key numbers:**
  - Mini Crosswords: 0.465 → **0.575** after edge optimization; 0.668 with node optimization added (App. D.2).
  - HumanEval: 0.76 → **0.88** (online setting).
  - GAIA (Table 1): GPTSwarm avg **18.45** vs GPT-4-Turbo 9.70 (Level 1: 30.56).
- **Where "83.01% vs 83.66%, $5.32 vs $105.93" comes from:** GPTSwarm **Appendix D.1, Table 3**.
  - Setting: MMLU **adversarial** setting (3 truthful + 3 adversarial agents), gpt-4-1106-preview.

    | Method | Accuracy | Optimization cost | Inference cost |
    |---|---|---|---|
    | GPTSwarm | 0.8301 | $5.32 | $1.82 |
    | DyLAN (avg over 1–5 pruned agents) | 0.8366 | $105.93 | $14.99 |
    | Multiagent Debate | 0.5751 | $32.8 total | |

  - Problems with how the file uses it:
    - $5.32 vs $105.93 is the **optimization** cost, not "the cost of the full experiment".
    - DyLAN is **not a static topology**. It prunes agents dynamically.
    - It is an appendix result in an adversarial setup, not a headline Pareto result.
- **Confusable number in AgentPrune:** AgentPrune (2410.02506) also contains "83.66". That is GPTSwarm+AgentPrune on MMLU: 83.32 → 83.66. It is a coincidence, not the source.

PDF: https://arxiv.org/pdf/2402.16823 (Table 3, Table 11)

---

## 4. Li et al. 2025, Self-MoA (arXiv 2502.00674)

**VERDICT: CONFIRMED (numbers). Venue: could not verify.**

- **Title:** "Rethinking Mixture-of-Agents: Is Mixing Different Large Language Models Beneficial?"
- **Authors:** Wenzhe Li, Yong Lin, Mengzhou Xia, Chi Jin (Princeton).
- **Status:** arXiv v1, 2 Feb 2025. arXiv shows no venue.
- **Main claims:**
  - Self-MoA aggregates multiple outputs of the **single top-performing LLM**.
  - **+6.6%** over MoA on AlpacaEval 2.0.
  - **+3.8% average** across MMLU, CRUX and MATH.
  - Reaches a new SOTA on the AlpacaEval 2.0 leaderboard.
  - MoA quality is sensitive to proposer quality; mixing LLMs often lowers average quality.
  - Self-MoA-Seq is a sequential version.
- **Qualification:** the authors also identify scenarios where mixing helps. The file's "refutación matemática de la diversidad inter-modelos" overstates the result. It is empirical, not a mathematical refutation.

https://arxiv.org/abs/2502.00674

---

## 5. Correlated errors

### "Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels" (arXiv 2605.29800)

**VERDICT: EXISTS; numbers partially correct.**

- **Author and status:** Guneet Kohli (single author, affiliation **Apple**). arXiv v1, 28 May 2026, preprint and not peer-reviewed. The file's ref [140] "Apple Research" is the same paper, not a separate source.
- **Setup:** 9 frontier LLMs from 7 families, acting as **judges** on NLI datasets (MNLI, SNLI, AlphaNLI; 100 human annotations per item) plus RewardBench.
- **Key results:**
  - Kish n_eff ≈ **2.18** (MNLI), 2.35, 2.48. Across conditions it is about 2.0–2.5.
  - Roughly three quarters of the panel's nominal independence is lost.
  - Panel accuracy is 8–22 pp below the Condorcet-independent prediction.
  - The best single judge matches or beats the panel.
  - Dawid-Skene or weighted aggregation closes at most 11% of the gap.
- **About "2.3–3.1":** the phrase does appear ("effective independence asymptoting at roughly 2.3–3.1, varying by dataset"). However, the measured value for 9 judges is about 2.2, with an asymptote 1/φ̄ ≈ 2.6. Cite "≈2 effective votes".
- **Scope:** the result is about **judge panels on NLI labels**, not task-solving ensembles. Extrapolating it to agent swarms is your own hypothesis.

https://arxiv.org/abs/2605.29800

### Solid primary papers on correlated errors

- **Kim, Garg, Peng, Garg (2025), "Correlated Errors in Large Language Models," ICML 2025** (arXiv 2506.07962).
  - Covers more than 350 LLMs; "models agree 60% of the time when both models err" on one leaderboard dataset.
  - Larger, more accurate models have more correlated errors, even across providers and architectures.
- **Goel et al. (2025), "Great Models Think Alike and this Undermines AI Oversight," ICML 2025** (PMLR 267:19621–19678, spotlight; arXiv 2502.04313).
  - Introduces the CAPA similarity metric.
  - LLM judges favor models similar to themselves.
  - Mistakes become more similar as capability increases.

---

## 6. Judge bias

- **Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations," NeurIPS 2024 (main track, oral).** **CONFIRMED.** arXiv 2404.13076.
  - GPT-4 and Llama 2 can recognize their own outputs with non-trivial accuracy.
  - There is a **linear correlation between self-recognition and self-preference** (shown via fine-tuning).
  - **Wrong in the file:** "evaluación cruzada reduce este sesgo en más del 30%" is not in this paper. Unsourced.
  - **Inaccurate in the file:** "firmas sintácticas de perplejidad latente" is not the paper's mechanism.
- **Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023 Datasets & Benchmarks.** **CONFIRMED.** arXiv 2306.05685.
  - Identifies **position bias, verbosity bias and self-enhancement bias**, plus limited math reasoning.
  - GPT-4 judge reaches **>80% agreement** with humans, the same level as human-human agreement.
  - Releases 3K expert votes and 30K conversations.

---

## 7. Anthropic, "How we built our multi-agent research system" (13 Jun 2025)

**VERDICT: CONFIRMED, but the file misquotes the comparison baseline.**

https://www.anthropic.com/engineering/multi-agent-research-system

- Quotes from the post:
  - "agents typically use about 4× more tokens than chat interactions"
  - "multi-agent systems use about 15× more tokens than chats"
  - On BrowseComp, three factors explain 95% of performance variance; "token usage by itself explains 80% of the variance", with the number of tool calls and model choice as the other two.
  - Multi-agent (Opus 4 lead + Sonnet 4 subagents) beat single-agent Opus 4 by **90.2%** on Anthropic's internal research eval.
- **Errors in the file:**
  - It says multi-agent uses 15× more tokens "que una interacción de agente único". The post says 15× vs **chat**. Against a single agent it is only about 15/4 ≈ 3.75×.
  - It attributes the 15× to "mallas completas". Anthropic's system is **orchestrator-worker** (lead agent plus parallel subagents), not a mesh.

---

## 8. Topology scaling

- **Qian et al., MacNet, "Scaling LLM-based Multi-Agent Collaboration" (arXiv 2406.07155), ICLR 2025.** **CONFIRMED.**
  - Agents arranged as DAGs; **more than 1,000 agents**.
  - Irregular topologies beat regular ones.
  - "Collaborative scaling law" with **logistic** growth; collaborative emergence occurs earlier than neural emergence.
  - Code: OpenBMB/ChatDev, macnet branch.
- **Zhang et al., AgentPrune, "Cut the Crap…" (arXiv 2410.02506).** **CONFIRMED.**
  - Comparable results to SOTA topologies at **$5.6 vs $43.7**.
  - **28.1%–72.8%** token reduction when plugged into AutoGen or GPTSwarm.
  - +3.5%–10.8% under adversarial attacks.
  - Published at ICLR 2025 according to the community record. The arXiv page has no venue line.
- **Kim, Gu, …, McDuff, Liu, "Towards a Science of Scaling Agent Systems" (arXiv 2512.08296; v3, 8 Apr 2026; Google Research and others; preprint).** **EXISTS.**
  - **Setup:** 5 architectures: single-agent (SAS), Independent, Centralized, Decentralized, Hybrid. **260** configurations (v3; v1 said 180). 6 benchmarks: BrowseComp-Plus, Finance-Agent, PlanCraft, Workbench, SWE-bench Verified, Terminal-Bench. Model families from OpenAI, Google and Anthropic.
  - **Trace-level error amplification (Table 5):**

    | Architecture | Amplification |
    |---|---|
    | Single agent | 1.0 |
    | **Centralized** | **4.4×** |
    | Hybrid | 5.1× |
    | Decentralized | 7.8× |
    | **Independent** | **17.2×** |

  - **Performance range:** from **+80.8%** (decomposable financial reasoning, centralized) to **−70.0%** (sequential planning, independent).
  - **Capability ceiling:** when the single-agent baseline exceeds about **45%**, adding agents gives negative returns (β = −0.236, p = 0.004).
  - **Tool-coordination trade-off:** β = −0.096.
  - **Predictive model:** cross-validated R² = 0.373 (0.413 with a task-grounded capability metric). It picks the best architecture for **87%** of held-out configurations.
  - This is the strongest primary source for "centralized > mesh/independent", and it is directly relevant to the RQ.

---

## 9. "More Agents" and "AI Agents That Matter"

- **Li, Zhang, Yu, Fu, Ye, "More Agents Is All You Need" (arXiv 2402.05120), TMLR (2024).** **CONFIRMED.**
  - Sampling-and-voting ("Agent Forest"): performance scales with the number of agents.
  - Gains grow with task difficulty; the method is orthogonal to other techniques.
- **Kapoor, Stroebl, Siegel, Nadgir, Narayanan, "AI Agents That Matter" (arXiv 2407.01502; Princeton).** **CONFIRMED.**
  - Main recommendations:
    1. Agent evaluations must be **cost-controlled**.
    2. **Jointly optimize accuracy and cost**, and visualize results as an accuracy-vs-inference-cost **Pareto curve** (constrained to be convex).
    3. Use simple baselines: retry, warming, and escalation (Llama-3 8B → stronger models).
  - On HumanEval these baselines match SOTA agents. Reflexion and LDB cost more than 50% more than warming; LATS costs more than 50× more.
  - Also covers holdout sets against overfitting, and reproducibility.
  - Venue: the arXiv v1 shows none; I did not verify the later journal version.

---

## 10. Current API prices (USD per 1M tokens, standard tier, cache miss), accessed 2026-10-06

| Provider / model ID | Input | Cached input | Output | Status / notes | Source |
|---|---|---|---|---|---|
| DeepSeek **`deepseek-chat`** | — | — | — | **RETIRED.** It was routed to V4-Flash after 2026-04-24 and became "fully retired and inaccessible after Jul 24th, 2026, 15:59 UTC". Earlier history: V3 → V3.1 → V3.2 (Dec 2025). | https://api-docs.deepseek.com/updates , https://api-docs.deepseek.com/news/news260424 |
| DeepSeek **`deepseek-flash`** (DeepSeek-V4.1-Flash, released 2026-09-10) | **$0.30** peak / $0.15 off-peak | $0.006 / $0.003 | **$1.20** peak / $0.60 off-peak | Current cheap model; thinking and non-thinking modes; 1M context. Off-peak is 50%. Peak hours are 01–04 and 06–10 UTC, Mon–Fri. | https://api-docs.deepseek.com/quick_start/pricing |
| DeepSeek `deepseek-v4-pro` (V4-Pro-0813) | $1.32 peak / $0.66 off-peak | $0.044 / $0.022 | $3.96 / $1.98 | `deepseek-reasoner` is also retired | same |
| OpenAI `gpt-4o-mini` | **$0.15** | $0.075 | **$0.60** | Still listed. Batch is $0.075 / $0.30. | https://developers.openai.com/api/docs/pricing , /models/gpt-4o-mini |
| OpenAI `gpt-5-nano` | **$0.05** | $0.005 | **$0.40** | Cheapest listed model. The docs suggest newer models for new projects. | /models/gpt-5-nano |
| OpenAI `gpt-5-mini` | **$0.25** | $0.025 | **$2.00** | | /models/gpt-5-mini |
| OpenAI `gpt-4.1-nano` | $0.10 | $0.025 | $0.40 | | pricing page |
| OpenAI `gpt-6-luna` (current flagship-family small model) | $0.10 | $0.01 | $0.50 | Short context; cache write $0.125 | pricing page |
| OpenAI `gpt-5.6-luna` | $0.20 | $0.02 | $1.20 | | pricing page |
| Anthropic **`claude-haiku-4-5`** (snapshot `claude-haiku-4-5-20251001`) | **$1.00** | $0.10 hit (5-min write $1.25) | **$5.00** | Batch is $0.50 / $2.50. Haiku 3.5 is retired on the first-party API. | https://platform.claude.com/docs/en/about-claude/pricing |
| Groq `llama-3.1-8b-instant` | — | — | — | **Deprecated for free and developer tiers, shut down 08/16/2026.** Now "Enterprise / Contact Sales" only. Groq's suggested replacement is `openai/gpt-oss-20b`. | https://console.groq.com/docs/deprecations , /docs/models |
| Groq `llama-3.3-70b-versatile` | — | — | — | Same as above, shut down 08/16/2026. Replacements: `openai/gpt-oss-120b` or `qwen/qwen3.6-27b` (itself replaced by qwen3.8-27b) | same |
| Groq `openai/gpt-oss-20b` | **$0.075** | — | **$0.30** | Open-weights | /docs/models |
| Groq `openai/gpt-oss-120b` | **$0.15** | — | **$0.60** | Open-weights | /docs/models |
| Groq `qwen/qwen3.8-27b` | $0.80 | — | $4.00 | Preview model | /docs/models |

**Free tiers**

- **Groq:** a Free Plan exists.
  - `openai/gpt-oss-120b`, `gpt-oss-20b` and `qwen/qwen3.8-27b` each get **30 RPM, 1K requests/day, 8K TPM, 200K tokens/day**.
  - Llama chat models are **no longer** on the free plan.
  - Source: https://console.groq.com/docs/rate-limits
- **OpenRouter:** `:free` model variants get **20 RPM**.
  - Daily limit is **50 requests/day** if you have bought less than $10 of credits ever, **1,000/day** at $10 or more.
  - This is usable for a small open-model arm, but 50/day is tight.
  - Source: https://openrouter.ai/docs/api-reference/limits
  - I did not check the specific :free model list. Check it at run time.

**Errors in the research file's budget table**

- "DeepSeek-V3 $0.55 / $2.19" is wrong. Those were DeepSeek-R1 launch prices (Jan 2025); V3 was $0.27 / $1.10. Both model names are now retired.
- "GPT-4o-mini cache $0.30" is wrong. Cached input is $0.075; $0.30 is the batch output price.
- "Llama-3-8B $0 local" is fine only if you actually run it locally.

---

## 11. Microsoft Agent Framework and AAIF

- **Microsoft Agent Framework (MAF): CONFIRMED.**
  - **Version 1.0 (GA, production-ready, stable APIs, long-term support)** for .NET and Python was announced on **3 Apr 2026**. Release candidate was 19 Feb 2026; first announced Oct 2025. License: MIT.
    - https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/
  - The `microsoft/autogen` README says: "AutoGen is now in maintenance mode. It will not receive new features or enhancements and is community managed going forward… Microsoft Agent Framework (MAF) is the enterprise‑ready successor to AutoGen."
    - https://github.com/microsoft/autogen
  - Migration guide: https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
  - **Correction:** "AutoGen (Legacy / AG2)" in the file conflates two projects. AG2 (ag2ai) is a separate community fork, not Microsoft's AutoGen.
  - Do not cite "agentframework.net" or blogs. Cite devblogs.microsoft.com and learn.microsoft.com.
- **AAIF: CONFIRMED (as of now).**
  - The Linux Foundation announced the Agentic AI Foundation on **9 Dec 2025**. Anchor projects were Anthropic's **MCP**, Block's **goose** and OpenAI's **AGENTS.md**.
    - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  - **A2A** was first donated to the LF as a separate project (Jun 2025). It **joined AAIF as a hosted project on 17 Aug 2026**.
    - https://aaif.io/blog/a2a-joins-aaif
  - The AAIF projects page now lists MCP, goose, AGENTS.md, agentgateway, A2A and Agent Router: https://aaif.io/projects/
  - Wording fix: AAIF is a directed fund/foundation under the Linux Foundation, not "una división operativa certificada".

---

## 12. Datasets

- **GSM8K**
  - HF id: `openai/gsm8k`, config `main` (also `socratic`).
  - Size: **test = 1,319**, train = 7,473.
  - Fields: `question`, `answer`. The answer ends with **`#### <number>`** (e.g. "…#### 18") and contains `<<calc>>` annotations.
  - License: **MIT**.
- **MATH-500**
  - HF id: `HuggingFaceH4/MATH-500`, split `test`, **500** problems.
  - Fields: `problem`, `solution`, `answer`, `subject`, `level` (1–5), `unique_id`.
  - It is OpenAI's PRM800K "Let's Verify Step by Step" subset of MATH.
  - The HF card declares **no license**. Upstream, hendrycks/math and openai/prm800k are both **MIT**.
  - Answers are LaTeX, so use a math-equivalence checker (e.g. `math-verify`), not string match.

---

## Claims in the research file that must NOT be used

1. **"Mesh increases communication costs exponentially."** Wrong. A full mesh of n agents has n(n−1) directed messages per round, which is **O(n²)**: quadratic, not exponential. Token cost grows roughly as O(n²·r), plus history re-sending. The file itself later writes "polinómico", which contradicts "exponencial".
2. **"AutoGen +8% MATH, +6% HumanEval over baseline."** Not in the paper. Use instead: MATH full test **69.48% vs GPT-4 55.18%**; 120 Level-5 problems **52.5%** (best of the compared systems).
3. **"65% → 85% programming success with GPT-4."** Unsourced.
4. **"MAST LLM judge: 94% agreement and κ = 0.88."** Wrong. It is o1 few-shot, accuracy 0.94, κ = **0.77**. The 0.88 is human IAA.
5. **"Failure rates 41–86.7% in production environments."** These are benchmark runs, and the per-system rates are "not directly comparable". The per-framework values (41.4 / 56.4 / 78.6 / 86.7) could not be verified from text.
6. **"GPTSwarm 83.01% ≈ DyLAN 83.66% at $5.32 vs $105.93 per full experiment; DyLAN = static complex topology."** The numbers are real, from GPTSwarm App. D.1 Table 3. But they are an **adversarial-MMLU appendix experiment**, the dollar figures are **optimization costs**, and DyLAN is **dynamic**. If used at all, use it only with that context.
7. **"Anthropic: multi-agent uses 15× more tokens than a single agent" / "full meshes multiply usage up to 15×."** The post says 15× vs **chat**, about 3.75× vs a single agent, and the system is **orchestrator-worker**, not mesh.
8. **"Effective votes 2.3–3.1 in LLM ensembles."** The measured value for a 9-**judge** NLI panel is n_eff ≈ 2.2 (asymptote about 2.6). It comes from a single-author, non-peer-reviewed preprint about judge panels, not agent ensembles. Refs [136], [140] and [144] are one paper, and [144] is a secondary review site.
9. **"Self-MoA is a mathematical refutation of inter-model diversity."** Overstated. The result is empirical, and the authors identify cases where mixing helps.
10. **"Cross-evaluation reduces self-preference bias by >30%"** and **"judges detect latent-perplexity syntactic signatures."** Unsourced. They are not in Panickssery et al.
11. **Pricing table:** DeepSeek-V3/R1 at $0.55/$2.19, and GPT-4o-mini cached at $0.30, are wrong or outdated. `deepseek-chat` / `deepseek-reasoner` are **retired** (since 2026-07-24). Groq Llama 3.1-8B / 3.3-70B are **shut down** for free and dev tiers (2026-08-16). Re-plan the model grid. A cheap, current set would be: `deepseek-flash`, `gpt-5-nano` or `gpt-4o-mini`, `claude-haiku-4-5`, and Groq `openai/gpt-oss-20b` / `gpt-oss-120b` (open weights, free tier).
12. **"AutoGen (Legacy / AG2) obsolete."** AutoGen is in maintenance mode, but AG2 is a separate, active community fork. Do not merge them.
13. **"MAF GA since April 2026, successor of AutoGen and SK."** Correct, but cite Microsoft devblogs and the autogen README, not agentframework.net or blogs.
14. **"MCP and A2A governed by AAIF."** True only since **17 Aug 2026** for A2A. MCP has been there since Dec 2025. Cite the aaif.io / LF primary pages.
15. **Ref [112]** "Zhang, S., 'Faulty Implementation and Misread Developer Intent…', arXiv:2605.29442" is mis-cited. The real paper is Tang, Chen, Xu et al., "How Coding Agents Fail Their Users: … 20,574 Real-World Sessions".
16. **Blog references marked [VERIFICADO]** (NiteAgent, Meiklejohn, AY Automate, BenchLM, LLM Gateway, DeployBase, The Moonlight, agentframework.net, LangChain marketing pages) are secondary. Replace each with the primary source listed above.
17. **"Ruflo"** is described as literature. It is grey literature with no peer-reviewed evaluation, so do not use it as evidence.
