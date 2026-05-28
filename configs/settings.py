from pathlib import Path

# ============================================================
# Base paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUTS_DIR = BASE_DIR / "inputs"
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"

# ============================================================
# Input files
# ============================================================

PROMPT_PATH = PROMPTS_DIR / "agent_prompt.txt"
ATTACK_JSON_PATH = INPUTS_DIR / "uc03_masquerade_fault.json"
PERFORMANCE_RESULTS_PATH = INPUTS_DIR / "performance_results.json"

# ============================================================
# Output files and directories
# ============================================================

LLM_RESPONSE_PATH = OUTPUTS_DIR / "llm_response.txt"
ITERATION_HISTORY_PATH = OUTPUTS_DIR / "iteration_history.json"
SUGGESTED_CONFIG_PATH = OUTPUTS_DIR / "suggested_attack_config.json"
METRICS_CSV_PATH = OUTPUTS_DIR / "metrics_history.csv"

LLM_RESPONSES_DIR = OUTPUTS_DIR / "llm_responses"
ATTACK_CONFIGS_DIR = OUTPUTS_DIR / "attack_configs"
EXPERIMENTS_DIR = OUTPUTS_DIR / "experiments"

# ============================================================
# LLM models used in the experiments
# ============================================================

MODEL_IDS = [
    "groq/compound-mini",
    "openai/gpt-oss-20b",
    "groq/compound",
    "qwen/qwen3-32b",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
]

# Default model used when running only:
# python main.py
MODEL_ID = "llama-3.1-8b-instant"

# ============================================================
# Agent configuration
# ============================================================

TEMPERATURE = 0.2
TOTAL_ITERATIONS = 30

# Context control to reduce token usage
HISTORY_WINDOW = 1
TOP_FEATURE_IMPORTANCES = 5
MAX_EDITABLE_FIELDS = 12

# Rate-limit control
SLEEP_BETWEEN_ITERATIONS_SECONDS = 8
SLEEP_BETWEEN_MODELS_SECONDS = 60

# ============================================================
# Synthetic generator runtime configuration
# ============================================================

GENERATOR_RUNTIME_DIR = BASE_DIR / "generator_runtime"

GENERATOR_JAR_PATH = GENERATOR_RUNTIME_DIR / "ereno-generator.jar"

GENERATOR_ATTACK_CONFIG_RELATIVE_PATH = "config/attacks/uc03_masquerade_fault.json"

GENERATOR_ACTION_CONFIG_RELATIVE_PATH = "config/actions/action_create_attack_dataset.json"

# This filename must match the output file defined inside:
# generator_runtime/config/actions/action_create_attack_dataset.json
GENERATOR_OUTPUT_DATASET_PATH = (
    GENERATOR_RUNTIME_DIR
    / "target"
    / "training"
    / "training_dataset_claude_v6.csv"
)

GENERATOR_RUN_COMMAND = [
    "java",
    "-jar",
    str(GENERATOR_JAR_PATH),
    GENERATOR_ACTION_CONFIG_RELATIVE_PATH,
]

# ============================================================
# Temporary backward-compatible aliases
# ============================================================
# These aliases avoid breaking files that still import ERENO_* names.
# After updating main.py and the runner, these can be removed.

ERENO_PROJECT_PATH = str(GENERATOR_RUNTIME_DIR)

ERENO_ATTACK_CONFIG_RELATIVE_PATH = GENERATOR_ATTACK_CONFIG_RELATIVE_PATH

ERENO_OUTPUT_DATASET_PATH = str(GENERATOR_OUTPUT_DATASET_PATH)

ERENO_RUN_COMMAND = GENERATOR_RUN_COMMAND