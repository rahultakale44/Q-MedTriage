"""End-to-end tests for context-aware /ask endpoint."""

import json
import textwrap

import requests

BASE = "http://localhost:8000/ask"
CTX = {
    "analysis_context": {
        "prediction": "PNEUMONIA",
        "confidence": 0.674,
        "probabilities": {"NORMAL": 0.326, "PNEUMONIA": 0.674},
        "analysis_type": "chest_xray_triage",
        "classifier": "classical",
        "model": "SVM",
        "priority": "HIGH",
    }
}

QUESTIONS = [
    ("What does 67.4% indicate?", [
        lambda d: any(x in d.get("answer", "").lower() for x in ["confidence", "model", "classification", "ai"]),
        lambda d: "67.4" in d.get("answer", "") or "67" in d.get("answer", ""),
    ]),
    ("Why did the model predict pneumonia?", [
        lambda d: any(x in d.get("answer", "").lower() for x in ["pneumonia", "predict", "model"]),
        lambda d: len(d.get("sources", [])) > 0,
    ]),
    ("What are symptoms of pneumonia?", [
        lambda d: len(d.get("sources", [])) > 0,
        lambda d: any(x in d.get("answer", "").lower() for x in ["symptom", "cough", "fever", "breath"]),
    ]),
    ("Explain this result in simple words.", [
        lambda d: any(x in d.get("answer", "").lower() for x in ["pneumonia", "confidence", "prediction", "model"]),
    ]),
]


def main():
    for i, (question, checks) in enumerate(QUESTIONS, 1):
        r = requests.post(BASE, params={"question": question}, json=CTX, timeout=90)
        d = r.json()
        print("=" * 70)
        print(f"TEST {i}: {question}")
        print(
            f"HTTP {r.status_code} | success={d.get('success')} | "
            f"sources={len(d.get('sources', []))} | "
            f"follow_ups={len(d.get('follow_up_questions', []))}"
        )
        answer = d.get("answer", "")
        print("ANSWER PREVIEW:")
        preview = answer[:700] + ("..." if len(answer) > 700 else "")
        print(textwrap.fill(preview, width=100))
        if d.get("follow_up_questions"):
            print("FOLLOW-UPS:", d["follow_up_questions"])
        for j, check in enumerate(checks, 1):
            ok = check(d)
            print(f"  check {j}: {'PASS' if ok else 'FAIL'}")
        print()


if __name__ == "__main__":
    main()
