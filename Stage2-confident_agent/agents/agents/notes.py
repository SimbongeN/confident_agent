"""Topic-keyed reference notes (direct lookup, no vector database).

Each notes file in reference_notes/ looks like:

    # Topic title
    keywords: singleton, getinstance, single instance
    - fact 1 ...
    - fact 2 ...

Files whose names start with '_' are ignored (templates).
"""
import os
import re

import config


class ReferenceNotes:
    def __init__(self, folder):
        self.topics = {}
        if not os.path.isdir(folder):
            return
        for fn in sorted(os.listdir(folder)):
            if not fn.lower().endswith(".md") or fn.startswith("_"):
                continue
            with open(os.path.join(folder, fn), encoding="utf-8") as f:
                lines = f.read().splitlines()
            keywords, body, title = [], [], ""
            for ln in lines:
                if ln.startswith("# ") and not title:
                    title = re.sub(r"\s*\(.*?\)", "", ln[2:]).strip().lower()
                    body.append(ln)
                elif ln.lower().startswith("keywords:"):
                    keywords = [k.strip().lower() for k in ln.split(":", 1)[1].split(",") if k.strip()]
                else:
                    body.append(ln)
            self.topics[fn[:-3]] = {"keywords": keywords, "title": title,
                                    "text": "\n".join(body).strip()}

    # single-word keywords that appear in many unrelated prompts count for less
    GENERIC = {"int", "new", "state", "update", "event", "this", "context", "class", "object",
               "method", "instance", "static", "private", "public", "language", "sharing", "copy",
               "subject", "notify", "reuse", "grammar", "expression", "request", "kit", "token",
               "action", "cursor", "handler", "successor", "policy", "reference", "default",
               "super", "import", "package", "jar", "api", "hook", "visit", "accept", "leaf",
               "dependents", "composition", "inheritance", "interface", "abstract", "type",
               "java 8", "design pattern categories"}
    MIN_SCORE = 1.0

    @staticmethod
    def _hits(keyword, low):
        """Occurrences as a whole word/phrase, tolerating a plural ending."""
        return len(re.findall(r"(?<!\w)" + re.escape(keyword) + r"(?:s|es)?(?!\w)", low))

    @staticmethod
    def _singular(title):
        if title.endswith(("ses", "xes")):
            return title[:-2]
        return title[:-1] if title.endswith("s") else title

    def score(self, name, text):
        t = self.topics[name]
        low = text.lower()
        total = 0.0
        for k in t["keywords"]:
            generic = k in self.GENERIC
            h = min(self._hits(k, low), 1 if generic else 3)
            if h:
                weight = 0.4 if generic else (2.0 if " " in k else 1.0)
                total += h * weight
        title = self._singular(t.get("title", ""))
        if title and title not in self.GENERIC and self._hits(title, low):
            total += 3.0
        return total

    def lookup(self, text, max_topics=2, max_chars=config.NOTES_MAX_CHARS):
        """Return (notes_text, [topic names]) for the best-matching topics."""
        scored = sorted(((self.score(n, text), n) for n in self.topics), reverse=True)
        chosen = [n for s, n in scored[:max_topics] if s >= self.MIN_SCORE]
        notes = "\n\n".join(self.topics[n]["text"] for n in chosen)
        return notes[:max_chars], chosen
