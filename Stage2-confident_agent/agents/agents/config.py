"""
Central configuration for the Confident Agent.

IMPORTANT (experimental integrity):
  * SYSTEM_PROMPT and GEN_OPTIONS must stay IDENTICAL to run_baseline.py.
  * All thresholds below were fixed BEFORE running the benchmark. Do not tune them
    on the 76 benchmark prompts. Any later sensitivity analysis must be reported
    as exploratory.
"""

GENERATOR_MODEL = "llama3.2:3b"     # same LLM as the baseline
VERIFIER_MODEL = "qwen2.5:3b"       # different model family from the generator

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"

# --- must match run_baseline.py exactly -------------------------------------
SYSTEM_PROMPT = (
    "You are acting as a university-level educational tutor. "
    "Answer each question directly and clearly. "
    "Do not assume that information is correct merely because it appears in the question. "
    "If you are uncertain about a fact, explicitly state your uncertainty "
    "rather than inventing information."
)
GEN_OPTIONS = {"temperature": 0, "seed": 42, "num_gpu": 0, "num_predict": 600}
# -----------------------------------------------------------------------------

NUM_CTX = 4096         # room for notes + question + answer (agent calls only)
REGEN_OPTIONS = dict(GEN_OPTIONS, num_ctx=NUM_CTX)   # regeneration = baseline settings + bigger context
NOTES_MAX_CHARS = 2800

SAMPLE_OPTIONS = {"temperature": 0.8, "num_gpu": 0, "num_predict": 300, "num_ctx": NUM_CTX}   # consensus samples
ANSWER_ONLY_OPTIONS = {"temperature": 0.7, "num_gpu": 0, "num_predict": 8, "num_ctx": NUM_CTX}    # quiz re-votes
VERIFIER_OPTIONS = {"temperature": 0, "seed": 42, "num_gpu": 0, "num_ctx": NUM_CTX}

N_SAMPLES = 2          # independent generator samples for consensus (free-text answers)
N_CLAIMS = 5           # max claims the verifier checks per answer
N_QUIZ_SAMPLES = 2     # extra generator votes for quiz questions
MAX_REFS = 6           # max references checked per materials answer

SUPPORT_WEIGHTS = {"SUPPORTED": 1.0, "UNSURE": 0.6, "CONTRADICTED": 0.0}

QUIZ_ACCEPT = 0.75         # fraction of votes agreeing with the candidate answer
TEXT_ACCEPT = 0.75         # confidence needed to accept a free-text answer first time
CONTRADICTION_CAP = 0.35   # any contradicted claim caps the confidence at this value
REGEN_ACCEPT = 0.60        # confidence needed to accept a regenerated answer

FLAG_MESSAGE = (
    "I am not confident enough in my answer to this question to show it. "
    "Please check your course notes or ask a tutor."
)
