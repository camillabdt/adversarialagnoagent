# adversarialagnoagent

Agentic pipeline for parametric adversarial evaluation of Intrusion Detection Systems (IDSs) in IEC-61850 environments. LLM-based agents iteratively modify parameters of Masquerade attack scenarios to expose detection blind spots in a Random Forest IDS — without perturbing samples directly or interacting with real substations.

> This repository accompanies the paper *"An LLM-Based Agentic Pipeline for Generator-Level Adversarial Evaluation of Smart Grid IDSs"* (SBSeg 2026).

---

## How it works

1. A baseline Masquerade fault attack configuration (JSON) is used to generate a synthetic dataset via **the synthetic generator runtime**.
2. A **Random Forest** classifier is trained on this baseline dataset and kept fixed.
3. An **LLM-based agent** receives the current attack config, the latest IDS metrics, and the iteration history, then suggests parameter changes to create new attack variants.
4. Each variant is fed back to the synthetic generator runtime to generate a new dataset, which is evaluated against the fixed baseline IDS.
5. Metrics (F1-score, recall, false negatives, etc.) and artifacts are logged at every iteration.

---

## Requirements

- Python 3.10+
- Java (required by the synthetic generator runtime internally — check its own README)
- API key for **Groq** (see [Configuration](#configuration))

---

## Installation

### 1. Clone with submodules

the synthetic generator runtime is included as a git submodule. You **must** use `--recurse-submodules`:

```bash
git clone --recurse-submodules https://github.com/camillabdt/adversarialagnoagent.git
cd adversarialagnoagent
```

If you already cloned without the flag, run:

```bash
git submodule update --init --recursive
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your actual keys — see [Configuration](#configuration) for details.

### 5. Set up the synthetic generator runtime

The synthetic generator is executed through a local JAR runtime. Make sure the runtime files are available before starting the pipeline:

```bash
cd the synthetic generator runtime
# follow the synthetic generator runtime's own setup steps
cd ..
```

---

## Configuration

All pipeline constants (paths, model IDs, number of iterations, temperature, sleep intervals) live in `configs/settings.py`. You can override the most important ones via `.env` or CLI flags.

### Environment variables (`.env`)

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for Groq — used for all models in the automated pipeline |

Copy `.env.example` to `.env` and fill in your values. The file is loaded automatically via `python-dotenv`.

---

## Usage

### Run a single model

```bash
python main.py --model-id groq/compound-mini --iterations 30
```

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--model-id` | defined in `configs/settings.py` | LLM model identifier as returned by the provider API |
| `--iterations` | `30` | Number of adversarial iterations |

### Run all models (batch)

Runs every model listed in `MODEL_IDS` (defined in `configs/settings.py`) sequentially, saving each model's outputs to `outputs/experiments/<model_name>/`.

```bash
python run_all_models.py
```

Between each model run, outputs are cleared and the baseline attack config is restored automatically.

---

## Models used in the paper

The following model identifiers were used in the experiments (as returned by their respective provider APIs):

| Provider | Model ID |
|---|---|
| Groq | `groq/compound-mini` |
| Groq | `groq/compound` |
| Groq | `llama-3.1-8b-instant` |
| Groq | `llama-3.3-70b-versatile` |
| Groq | `qwen/qwen3-32b` |
| Groq | `openai/gpt-oss-20b` |
| Groq | `openai/gpt-oss-120b` |

> **Note:** The `openai/` prefix in some model IDs is just the identifier format used by the `agno` library — all models above are accessed via the Groq API with a single `GROQ_API_KEY`. Claude was evaluated separately via the claude.ai interface and is not part of the automated pipeline.

---

## Output structure

After a run, outputs are saved to `outputs/` (or `outputs/experiments/<model>/` when using `run_all_models.py`):

```
outputs/
├── metrics_history.csv          # per-iteration metrics (F1, recall, FN, TP, FP, ...)
├── iteration_history.json       # full history including LLM responses and configs
├── llm_response.txt             # latest LLM response
├── suggested_attack_config.json # latest attack configuration applied
├── attack_configs/              # per-iteration attack JSON files
├── llm_responses/               # per-iteration LLM response text files
└── dataset_iteration_N.csv      # generated datasets per iteration
```

When using `run_all_models.py`, each model's outputs are additionally copied to:

```
outputs/experiments/<model_name>/
├── status.txt
├── metrics_history.csv
├── iteration_history.json
├── attack_configs/
├── llm_responses/
└── datasets/
```

---

## Reproducing paper figures

After running the experiments, use the analysis scripts:

```bash
# Generate the F1-score evolution chart (Figure 2 in the paper)
python generate_f1.py

# Compare baseline vs adversarial variants
python evaluate_baseline_vs_adversarial.py
```

Output figures are saved to `paper_figures/`.

---

## Baseline attack configuration

The baseline scenario is defined in `inputs/uc03_masquerade_fault.json`. Key parameters (Table 2 of the paper):

| Parameter | Value | Role |
|---|---|---|
| `attackType` | `masquerade_fault` | Attack scenario type |
| `fault.prob` | `0.6` | Fault occurrence probability |
| `fault.durationMs` | `50–800 ms` | Fault duration interval |
| `cbStatus` | `1` | Circuit breaker status |
| `incrementStNumOnFault` | `true` | State number behavior during faults |
| `sqnumMode` | `fast` | Sequence number behavior |
| `ttlMsValues` | `[20, 40, 80]` | Time-to-live values in GOOSE messages |
| `analog.deltaAbs` | `0.2–0.8` | Analog signal variation interval |
| `trapArea.multiplier` | `1.2–2.5` | Trap-area multiplier interval |
| `trapArea.spikeProb` | `0.5` | Spike probability |

---

## Project structure

```
adversarialagnoagent/
├── generator_runtime/               # JAR-based synthetic IEC-61850 dataset generator runtime
├── agents/
│   └── strategist_agent.py  # LLM-based agent logic
├── configs/
│   └── settings.py          # all pipeline constants and paths
├── inputs/
│   └── uc03_masquerade_fault.json  # baseline attack configuration
├── outputs/                 # generated during runs (gitignored)
├── outputs llama/           # reference outputs from paper (Llama models)
├── outputs openai/          # reference outputs from paper (Claude models)
├── paper_figures/           # figures used in the paper
├── prompts/                 # base prompt for the LLM agent
├── tools/
│   ├── attack_config_validator.py
│   ├── generator_runner.py
│   ├── experiment_memory.py
│   ├── ids_evaluator.py
│   ├── json_loader.py
│   ├── json_patch_applier.py
│   ├── llm_response_parser.py
│   └── results_logger.py
├── main.py                  # single-model pipeline entrypoint
├── run_all_models.py        # batch entrypoint for all models
├── evaluate_baseline_vs_adversarial.py
├── generate_f1.py
├── requirements.txt
└── .env.example
```

---

## Important notes

- **No real infrastructure is used.** All experiments run exclusively on synthetic datasets generated by the local JAR-based synthetic generator runtime in a controlled local environment.
- **The Random Forest is trained once** on the baseline dataset and kept fixed throughout all adversarial iterations.
- API costs apply. Running 30 iterations per model across 7 models makes a significant number of LLM calls — monitor your usage.
- If a model repeatedly produces outputs that cannot be parsed into valid configuration changes, its iterations will be logged as `skipped` (this is expected behavior, documented in the paper).

---

## License

See `LICENSE` if present, or contact the authors.
