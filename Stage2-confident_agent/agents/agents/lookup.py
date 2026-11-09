"""External validation: bibliographic and URL lookups (no LLM involved).

Sources: Open Library (books), Crossref (papers), arXiv API (arXiv IDs), plain HTTP (URLs).
Statuses: VERIFIED, MISMATCH (found but details differ), NOT_FOUND, DEAD (URL),
          UNCHECKED (service unreachable - cannot tell).
"""
import difflib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "ConfidentAgent-COMP301/1.0 (university student project)"


def http_get(url, timeout=15, max_bytes=300000):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(max_bytes).decode("utf-8", "replace")


HTTP = http_get  # tests replace this


# ---------------------------------------------------------------- helpers
def norm(s):
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split())


def sim(a, b):
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    short, long_ = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(short) >= 8 and short in long_:
        return 0.95
    return difflib.SequenceMatcher(None, na, nb).ratio()


def last_names(names):
    return [n.split()[-1].lower() for n in names if n and n.strip()]


def _res(status, source="", detail=""):
    return {"status": status, "source": source, "detail": detail}


# ---------------------------------------------------------------- books / papers
def check_book(title, author_text, year):
    authors_lc = (author_text or "").lower()
    queries = [title]
    main = title.split(":")[0].strip()
    if main and main != title and len(main) >= 6:
        queries.append(main)
    best = None
    reachable = False
    for q in queries:
        url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode(
            {"title": q, "limit": 5, "fields": "title,author_name,first_publish_year,publish_year"})
        try:
            _, text = HTTP(url)
            data = json.loads(text)
            reachable = True
        except Exception:
            continue
        for d in data.get("docs", []):
            s = sim(title, d.get("title", ""))
            if s < 0.8:
                continue
            names = d.get("author_name") or []
            author_ok = (not authors_lc.strip()) or (not names) or any(
                ln in authors_lc for ln in last_names(names))
            years = set(d.get("publish_year") or [])
            if d.get("first_publish_year"):
                years.add(d["first_publish_year"])
            year_ok = year is None or not years or year in years
            if author_ok and year_ok:
                return _res("VERIFIED", "openlibrary", d.get("title", ""))
            if best is None or s > best[0]:
                best = (s, author_ok, year_ok, d.get("title", ""))
    cr = check_paper(title, authors_lc, year)
    if cr["status"] == "VERIFIED":
        return cr
    if best:
        why = " and ".join(x for x, ok in (("author", best[1]), ("year", best[2])) if not ok)
        return _res("MISMATCH", "openlibrary", f"title found ('{best[3]}') but {why} do not match")
    if cr["status"] == "MISMATCH":
        return cr
    if not reachable and cr["status"] == "UNCHECKED":
        return _res("UNCHECKED", "", "bibliographic services unreachable")
    return _res("NOT_FOUND", "openlibrary+crossref", "no matching record")


def check_paper(title, authors_lc, year):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 3, "select": "title,author,issued"})
    try:
        _, text = HTTP(url)
        items = json.loads(text)["message"]["items"]
    except Exception:
        return _res("UNCHECKED", "crossref", "unreachable")
    best = None
    for it in items:
        t = (it.get("title") or [""])[0]
        if sim(title, t) < 0.85:
            continue
        fams = [a.get("family", "") for a in it.get("author", []) if a.get("family")]
        author_ok = (not authors_lc.strip()) or any(f.lower() in authors_lc for f in fams)
        try:
            y = it["issued"]["date-parts"][0][0]
        except Exception:
            y = None
        year_ok = year is None or y is None or abs(year - y) <= 1
        if author_ok and year_ok:
            return _res("VERIFIED", "crossref", t)
        best = best or (t, author_ok, year_ok)
    if best:
        why = " and ".join(x for x, ok in (("author", best[1]), ("year", best[2])) if not ok)
        return _res("MISMATCH", "crossref", f"title found but {why} do not match")
    return _res("NOT_FOUND", "crossref", "no matching record")


def check_arxiv(arxiv_id, title, author_text):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": arxiv_id})
    try:
        _, text = HTTP(url)
        root = ET.fromstring(text)
    except Exception:
        return _res("UNCHECKED", "arxiv", "unreachable")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = root.findall("a:entry", ns)
    if not entries:
        return _res("NOT_FOUND", "arxiv", f"no paper with id {arxiv_id}")
    e = entries[0]
    t = (e.findtext("a:title", default="", namespaces=ns) or "").strip()
    if not t or t.lower().startswith("error"):
        return _res("NOT_FOUND", "arxiv", f"no paper with id {arxiv_id}")
    names = [(a.findtext("a:name", default="", namespaces=ns) or "") for a in e.findall("a:author", ns)]
    title_ok = (not title) or sim(title, t) >= 0.6
    author_ok = (not (author_text or "").strip()) or any(
        ln in author_text.lower() for ln in last_names(names))
    if title_ok and author_ok:
        return _res("VERIFIED", "arxiv", t)
    return _res("MISMATCH", "arxiv", f"id exists ('{t}') but title/authors differ")


# ---------------------------------------------------------------- URLs
_STOP = {"recommend", "provide", "youtube", "oracle", "please", "explain", "summarise",
         "summarize", "which", "about", "official", "documentation", "lecture", "principle",
         "pattern", "interface", "interfaces", "design", "software", "programming",
         "language", "exact", "pages", "page", "videos", "video"}


def relevance_tokens(prompt):
    toks = re.findall(r"\b[A-Z][A-Za-z]{5,}\b", prompt)
    return [t.lower() for t in toks if t.lower() not in _STOP and t.lower() != "java"]


def check_url(url, prompt=""):
    try:
        status, text = HTTP(url)
    except urllib.error.HTTPError as e:
        return _res("DEAD", "http", f"HTTP {e.code}")
    except Exception:
        return _res("UNCHECKED", "http", "could not connect")
    if status >= 400:
        return _res("DEAD", "http", f"HTTP {status}")
    toks = relevance_tokens(prompt)
    body = (text + url).lower()
    if toks and not any(t in body for t in toks):
        return _res("MISMATCH", "http", "page loads but does not mention the requested topic")
    return _res("VERIFIED", "http", "page loads and matches topic")


# ---------------------------------------------------------------- extraction
CUES = re.compile(
    r"(couldn't find|could not find|unable to|not aware|not familiar|no information|"
    r"don't have|do not have|cannot verify|can't verify|fictional|doesn't exist|"
    r"does not exist|may not exist|made-up|not a real|no record)", re.I)
QUOTE = re.compile(r'["\u201c]([^"\u201d\n]{6,160})["\u201d]')
QUOTE_ANY = re.compile(r"""(?<!\w)['"\u201c\u2018]([^'"\u201d\u2019\n]{8,160}?)['"\u201d\u2019](?!\w)""")
YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
ARX = re.compile(r"arxiv[:\s/]*(?:abs/)?(\d{4}\.\d{4,5})", re.I)
URL = re.compile(r"https?://[^\s\)\]>\"']+")
FACT_Q = re.compile(r"\b(who (wrote|is the author|authored)|what year|in what year|which year)\b", re.I)


def extract_references(prompt, response):
    refs = []
    for line in response.splitlines():
        if not line.strip() or CUES.search(line):
            continue
        urls = [u.rstrip(".,;:") for u in URL.findall(line)]
        for u in urls:
            refs.append({"kind": "url", "url": u, "raw": line.strip()})
        qm = QUOTE.search(line)
        am = ARX.search(line)
        if am:
            refs.append({"kind": "arxiv", "id": am.group(1), "title": qm.group(1) if qm else "",
                         "authors": line, "raw": line.strip()})
            continue
        if qm and not urls:
            title = qm.group(1).strip().rstrip(",.")
            if len(title.split()) >= 2:
                rest = line[qm.end():]
                ym = YEAR.search(rest)
                refs.append({"kind": "book", "title": title, "authors": rest[:200],
                             "year": int(ym.group(1)) if ym else None, "raw": line.strip()})
    if not refs and FACT_Q.search(prompt) and not CUES.search(response):
        qm = QUOTE_ANY.search(prompt)
        if qm:
            ym = YEAR.search(response)
            refs.append({"kind": "book", "title": qm.group(1).strip(), "authors": response,
                         "year": int(ym.group(1)) if ym else None,
                         "raw": response.strip().splitlines()[0] if response.strip() else ""})
    seen, out = set(), []
    for r in refs:
        key = (r["kind"], r.get("title") or r.get("url") or r.get("id"))
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def check_reference(ref, prompt=""):
    if ref["kind"] == "url":
        return check_url(ref["url"], prompt)
    if ref["kind"] == "arxiv":
        return check_arxiv(ref["id"], ref.get("title", ""), ref.get("authors", ""))
    return check_book(ref["title"], ref.get("authors", ""), ref.get("year"))


def selftest():
    """True if Open Library is reachable (used for a start-up warning)."""
    try:
        HTTP("https://openlibrary.org/search.json?title=effective+java&limit=1&fields=title", timeout=10)
        return True
    except Exception:
        return False
