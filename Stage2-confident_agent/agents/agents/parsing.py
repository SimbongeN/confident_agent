"""Helpers for reading answers out of model text and classifying requests."""
import re


def read_mcq_letter(text):
    t = text.strip()
    m = re.search(r"(?i:correct\s+answer|answer)\s*(?:is|:)?\s*[\*\(]*([A-D])\b", t)
    if m:
        return m.group(1)
    m = re.match(r"^[\W_]{0,6}([A-D])[\.\)]", t)
    if m:
        return m.group(1)
    m = re.search(r"\*\*\s*([A-D])[\.\)]", t)
    if m:
        return m.group(1)
    return None


def read_tf(text):
    head = text.strip()[:200]
    found = []
    for m in re.finditer(r"\b(not\s+)?(true|false)\b", head, flags=re.I):
        neg = bool(m.group(1))
        val = m.group(2).lower() == "true"
        found.append((not val) if neg else val)
    if not found or len(set(found)) > 1:
        return None
    return "True" if found[0] else "False"


def parse_choice(text, kind):
    """Parse a full explanatory answer."""
    return read_mcq_letter(text) if kind == "mcq" else read_tf(text)


def parse_answer_only(text, kind):
    """Parse a terse answer such as 'B' or 'True'."""
    t = text.strip()
    if kind == "mcq":
        m = re.match(r"^\W*([A-D])\b", t)
        return m.group(1) if m else read_mcq_letter(t)
    return read_tf(t)


def quiz_kind(prompt):
    """'mcq', 'tf' or None - decided from the prompt text only."""
    if re.search(r"(?m)^\s*[A-D][\.\)]\s+\S", prompt):
        return "mcq"
    if re.search(r"true\s+or\s+false", prompt, re.I):
        return "tf"
    return None


MATERIALS_RE = re.compile(
    r"\b(recommend|books?|papers?|arxiv|doi|urls?|links?|youtube|citation|author|"
    r"published|publication|who wrote|chapter of)\b", re.I)


def is_materials_request(prompt):
    return bool(MATERIALS_RE.search(prompt))


def looks_like_error(text):
    return (not text.strip()) or text.strip().startswith("[ERROR]")
