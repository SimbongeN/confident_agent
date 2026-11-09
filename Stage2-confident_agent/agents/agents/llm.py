"""Thin Ollama client with call/latency accounting."""
import json
import re
import time
import urllib.request

import config

_STATS = {"calls": 0, "seconds": 0.0}


def reset_stats():
    _STATS["calls"] = 0
    _STATS["seconds"] = 0.0


def get_stats():
    return dict(_STATS)


def _post_json(url, body, timeout=900):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


class OllamaClient:
    def __init__(self, model):
        self.model = model

    def chat(self, user, system=None, options=None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        body = {"model": self.model, "messages": messages, "stream": False,
                "options": dict(options or {})}
        start = time.time()
        last_err = None
        data = None
        for _ in range(2):
            try:
                data = _post_json(config.OLLAMA_URL, body)
                break
            except Exception as e:  # retry once
                last_err = e
                time.sleep(2)
        if data is None:
            raise RuntimeError(f"Ollama call failed: {last_err}")
        _STATS["calls"] += 1
        _STATS["seconds"] += time.time() - start
        return strip_think(data["message"]["content"])
