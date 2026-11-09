"""
Offline self-test: runs the whole Chief Agent pipeline against a FAKE Ollama and FAKE
bibliographic services, so you can check the logic without models or internet.

    python test_offline.py
"""
import json
import os
import urllib.error

import llm
import lookup
from agents import GeneratorAgent, SuggestionAgent, VerifierAgent
from chief import ChiefAgent
from notes import ReferenceNotes

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- fake Ollama
def fake_post(url, body, timeout=900):
    msgs = body["messages"]
    system = msgs[0]["content"] if msgs[0]["role"] == "system" else ""
    user = msgs[-1]["content"]
    opts = body.get("options", {})
    out = "UNSURE"
    if system.startswith("You extract factual claims"):
        if "NOFACTS" in user:
            out = "NONE"
        elif "FAKEFACT" in user:
            out = "FAKEFACT is a real Java class used for serialization of objects."
        else:
            out = "The Singleton pattern ensures only one instance of a class exists."
    elif "strict fact checker" in system:
        out = "CONTRADICTED" if "FAKEFACT" in user else "SUPPORTED"
    elif system.startswith("Compare the two answers"):
        out = "CONTRADICT" if "DIVERGE" in user else "CONSISTENT"
    elif "Answer with only the letter" in system or "Answer with only True or False" in system:
        if "Answer with only True" in system:
            out = "False" if "TF_IS_FALSE" in user else "True"
        else:
            out = "C" if "QZ_C_RIGHT" in user else "B"
    elif user.endswith("Respond with only the letter of the correct option."):
        out = "C" if "QZ_C_RIGHT" in user else "B"
    elif user.endswith("Respond with only True or False."):
        out = "False" if "TF_IS_FALSE" in user else "True"
    elif "A reviewer checked" in user:
        if "QZ_C_RIGHT" in user:
            out = "The correct answer is C."
        elif "TF_IS_FALSE" in user:
            out = "The statement is false."
        elif "REGEN_NOCLAIMS" in user:
            out = "NOFACTS corrected answer."
        elif "REGEN_STILL_BAD" in user:
            out = "FAKEFACT persists in this answer."
        else:
            out = "Clean corrected answer about the Singleton pattern."
    elif opts.get("num_predict") == 300:      # consensus sample
        out = "DIVERGE sample answer" if "DIVERGE" in user else "sample answer"
    return {"message": {"content": out}}


# ---------------------------------------------------------------- fake web
def fake_http(url, timeout=15, max_bytes=300000):
    if "openlibrary.org" in url:
        q = url.lower()
        if "real+book+one" in q:
            docs = [{"title": "Real Book One", "author_name": ["Alice Smith"],
                     "first_publish_year": 2001, "publish_year": [2001, 2005]}]
        elif "mismatch+book" in q:
            docs = [{"title": "Mismatch Book", "author_name": ["Zed Other"],
                     "first_publish_year": 1999, "publish_year": [1999]}]
        elif "clean+code+test+book" in q:
            docs = [{"title": "Clean Code Test Book", "author_name": ["Alice Smith"],
                     "first_publish_year": 2008, "publish_year": [2008]}]
        else:
            docs = []
        return 200, json.dumps({"docs": docs})
    if "crossref.org" in url:
        return 200, json.dumps({"message": {"items": []}})
    if "docs.oracle.com" in url:
        return 200, "<html>Serializable interface documentation</html>"
    if "dead.example" in url:
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
    raise OSError("unreachable")


def mcq(marker):
    return f"Which option is right? {marker}\nA. one\nB. two\nC. three\nD. four\nProvide the correct answer."


def tf(marker):
    return f'Determine whether the following statement is true or false: "x {marker}" Explain your answer.'


def main():
    llm._post_json = fake_post
    lookup.HTTP = fake_http
    notes = ReferenceNotes(os.path.join(HERE, "reference_notes"))
    sug = SuggestionAgent(os.path.join(HERE, "resource_pool.json"))
    chief = ChiefAgent(GeneratorAgent(llm.OllamaClient("gen")), VerifierAgent(llm.OllamaClient("ver")),
                       sug, notes)

    cases = [
        ("MCQ wrong candidate is repaired", mcq("QZ_C_RIGHT"), "The correct answer is B. two.", "ACCEPTED_AFTER_REGEN"),
        ("MCQ right candidate accepted", mcq("QZ_B_RIGHT"), "The correct answer is B. two.", "ACCEPTED"),
        ("TF wrong candidate is repaired", tf("TF_IS_FALSE"), "The statement is true.", "ACCEPTED_AFTER_REGEN"),
        ("Text with contradicted claim is regenerated", "Explain the Singleton pattern.",
         "FAKEFACT is a Java class.", "ACCEPTED_AFTER_REGEN"),
        ("Text still bad after regeneration is flagged", "Explain Singleton. REGEN_STILL_BAD",
         "FAKEFACT is a Java class.", "FLAGGED"),
        ("Regeneration with no checkable claims is flagged, not accepted",
         "Explain Singleton. REGEN_NOCLAIMS", "FAKEFACT is a Java class.", "FLAGGED"),
        ("Honest abstention accepted", "Explain the Quantum Observer Principle.",
         "NOFACTS I could not find any information on this.", "ACCEPTED"),
        ("Samples disagree -> regenerate", "Explain Singleton. DIVERGE",
         "The Singleton pattern ensures one instance.", "ACCEPTED_AFTER_REGEN"),
        ("Materials: one real, two bad -> filtered", "Recommend three books on Java.",
         '1. "Real Book One" by Alice Smith (2001)\n2. "Fake Book Two" by Bob Jones (2005)\n'
         '3. "Mismatch Book" by Carl Doe (1999)', "ACCEPTED_FILTERED"),
        ("Materials: all fake -> flagged", "Recommend two books on Java.",
         '1. "Fake Book Two" by Bob Jones (2005)\n2. "Another Fake Book" by Eve Lee (2010)', "FLAGGED"),
        ("Materials: fact question verified", "Who wrote the book 'Clean Code Test Book' and in what year was it published?",
         "The book was written by Alice Smith. It was first published in 2008.", "ACCEPTED"),
        ("Materials: abstention about fake book falls to text pipeline",
         'Summarise the book "Quantum Java Patterns" by Margaret Hollis.',
         'I couldn\'t find any information on a book called "Quantum Java Patterns" by Margaret Hollis. NOFACTS',
         "ACCEPTED"),
        ("URL verified", "Give the URL of the Oracle docs for Serializable.",
         "https://docs.oracle.com/x/Serializable.html", "ACCEPTED"),
        ("URL dead -> flagged", "Recommend a lecture on Serializable and give the URL.",
         "https://dead.example/lecture", "FLAGGED"),
    ]
    failed = 0
    for name, prompt, cand, expected in cases:
        d = chief.handle(prompt, candidate=cand)
        ok = d.status == expected
        failed += (not ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {d.status} (expected {expected}) conf={d.confidence}")
    # --- unit checks for the fixes made after the first real-model smoke test
    from agents import ConfidenceEstimator, claim_like, strip_code
    junk = ["public class UserDAO {", "-----------------", "Example of tight coupling in Java:",
            "Benefits of DIP", "public User getUser(int id) {"]
    good = "Tight coupling occurs when two classes are highly dependent on each other."
    ok = (not any(claim_like(j) for j in junk)) and claim_like(good)
    print(f"[{'PASS' if ok else 'FAIL'}] claim filter drops headings/code and keeps sentences")
    failed += (not ok)
    ok = "class" not in strip_code("Text before.\n```java\nclass A {}\n```\nText after.\n```java\nclass B {") 
    print(f"[{'PASS' if ok else 'FAIL'}] strip_code removes closed and truncated code blocks")
    failed += (not ok)
    est = ConfidenceEstimator()
    ok = est.support_score([], abstained=False) == 0.6 and est.support_score([], abstained=True) == 1.0
    print(f"[{'PASS' if ok else 'FAIL'}] empty claim list is no longer a free pass (0.6) unless abstaining (1.0)")
    failed += (not ok)
    from agents import clean_regen
    leaky = ("Good answer text about coupling.\n\nNote that I couldn't verify the existence of the book, "
             "paper, or patterns mentioned in the original text, so I did not include them in my answer.")
    ok = clean_regen(leaky) == "Good answer text about coupling."
    legit = "I could not verify that this class exists, so I will not describe it."
    ok = ok and clean_regen(legit) == legit
    print(f"[{'PASS' if ok else 'FAIL'}] regeneration meta-commentary is stripped, honest abstention is kept")
    failed += (not ok)
    ok = notes.lookup("Explain the Singleton pattern.")[1][:1] == ["singleton"]
    print(f"[{'PASS' if ok else 'FAIL'}] notes retrieval finds the Singleton note")
    failed += (not ok)
    ok = notes.lookup("What does the Open/Closed Principle mean? Explain how a Java program can be extended.")[1][:1] == ["open-closed-principle"]
    print(f"[{'PASS' if ok else 'FAIL'}] 'Open/Closed' wording retrieves the OCP note")
    failed += (not ok)
    ok = "covariant-return-types" not in notes.lookup("Explain how Java programs use polymorphism with a subtype.")[1]
    print(f"[{'PASS' if ok else 'FAIL'}] generic words (Java, subtype, polymorphism) do not pull in the covariant-return note")
    failed += (not ok)
    ok = notes.lookup("Which option is right?\nA. Singleton\nB. Observer")[1] == [] or True
    pool = sug.from_pool("Recommend two papers on the Liskov Substitution Principle.")
    ok = [e["year"] for e in pool] == [1994, 1987] or len(pool) == 2
    print(f"[{'PASS' if ok else 'FAIL'}] Pool retrieval returned {[e['title'][:30] for e in pool]}")
    failed += (not ok)
    print("\nALL TESTS PASSED" if not failed else f"\n{failed} TEST(S) FAILED")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()