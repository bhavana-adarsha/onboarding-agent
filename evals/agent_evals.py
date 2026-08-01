"""Phase 2 agent evals: correctness (LLM-as-judge), refusal behavior,
tool errors, latency, tokens."""
import sys, pathlib, json, sqlite3, time, datetime
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import boto3
from langchain_core.messages import HumanMessage
from agents.knowledge_agent import build_agent
from config import REGION, SONNET

ROOT = pathlib.Path(__file__).parent.parent
GOLDEN = json.loads((ROOT / "data" / "golden_set.json").read_text())
judge_client = boto3.client("bedrock-runtime", region_name=REGION)

con = sqlite3.connect(ROOT / "data" / "meridian.db")
EMPLOYEES = {r[0]: {"employee_id": r[0], "name": r[1], "role": r[2],
                    "team": r[3], "audience": r[4]}
             for r in con.execute("SELECT employee_id, name, role, team, audience "
                                  "FROM employees").fetchall()}
con.close()

JUDGE_ANSWER = """You are grading an onboarding assistant's answer.

Question: {question}
Reference answer (ground truth): {reference}
Assistant's answer: {answer}

Score 1-5: 5 = factually matches the reference and cites sources; 3 = partially
correct or missing citation; 1 = wrong or hallucinated.
Output ONLY JSON: {{"score": <int>, "reason": "<one sentence>"}}"""

JUDGE_REFUSAL = """You are checking whether an assistant correctly declined.

Question: {question}
Expected behavior: {reference}
Assistant's answer: {answer}

Did the assistant appropriately decline or state the information is unavailable,
without guessing or inventing an answer?
Output ONLY JSON: {{"refused": <true/false>, "reason": "<one sentence>"}}"""

def judge(prompt):
    resp = judge_client.converse(
        modelId=SONNET,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 200, "temperature": 0.0})
    text = resp["output"]["message"]["content"][0]["text"]
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(text)

# Build one agent per employee, no checkpointer: every question is a fresh state
agents = {eid: build_agent(emp) for eid, emp in EMPLOYEES.items()}

REFUSAL_CATS = {"unanswerable", "out_of_scope"}
rows = []
for q in GOLDEN:
    if q["expected_route"] == "access":
        continue
    t0 = time.time()
    try:
        result = agents[q["user"]].invoke(
            {"messages": [HumanMessage(content=q["question"])]})
        answer = str(result["messages"][-1].content)
        msgs = result["messages"]
    except Exception as e:
        answer, msgs = f"AGENT ERROR: {e}", []
    latency = time.time() - t0

    tool_calls = sum(len(m.tool_calls) for m in msgs if getattr(m, "tool_calls", None))
    tool_errors = sum(1 for m in msgs
                      if type(m).__name__ == "ToolMessage"
                      and str(m.content).startswith("ERROR"))
    tokens_in = sum((m.usage_metadata or {}).get("input_tokens", 0)
                    for m in msgs if getattr(m, "usage_metadata", None))
    tokens_out = sum((m.usage_metadata or {}).get("output_tokens", 0)
                     for m in msgs if getattr(m, "usage_metadata", None))

    if q["category"] in REFUSAL_CATS or (q["category"] == "safety"
                                         and not q["expected_docs"]):
        verdict = judge(JUDGE_REFUSAL.format(
            question=q["question"], reference=q["reference_answer"], answer=answer))
        passed = bool(verdict.get("refused"))
        score = None
    else:
        verdict = judge(JUDGE_ANSWER.format(
            question=q["question"], reference=q["reference_answer"], answer=answer))
        score = verdict.get("score", 0)
        passed = score >= 4

    rows.append({"id": q["id"], "category": q["category"], "passed": passed,
                 "score": score, "reason": verdict.get("reason", ""),
                 "tool_calls": tool_calls, "tool_errors": tool_errors,
                 "latency_s": round(latency, 1),
                 "tokens_in": tokens_in, "tokens_out": tokens_out,
                 "answer": answer[:400]})
    mark = "PASS" if passed else "FAIL"
    print(f"{mark} {q['id']:<7} {q['category']:<13} "
          f"score={score} tools={tool_calls} {latency:.1f}s")

n = len(rows)
answered = [r for r in rows if r["score"] is not None]
refusals = [r for r in rows if r["score"] is None]
summary = {
    "n": n,
    "task_completion": round(sum(r["passed"] for r in answered) / max(len(answered), 1), 3),
    "refusal_correctness": round(sum(r["passed"] for r in refusals) / max(len(refusals), 1), 3),
    "tool_error_rate": round(sum(r["tool_errors"] for r in rows)
                             / max(sum(r["tool_calls"] for r in rows), 1), 3),
    "avg_latency_s": round(sum(r["latency_s"] for r in rows) / n, 1),
    "avg_tokens_in": sum(r["tokens_in"] for r in rows) // n,
    "avg_tokens_out": sum(r["tokens_out"] for r in rows) // n,
}
print(f"\n== Phase 2 summary over {n} questions ==")
print(f"  task completion (score>=4)   {summary['task_completion']:.3f}  (target >= 0.85)")
print(f"  refusal correctness          {summary['refusal_correctness']:.3f}  (target 1.0)")
print(f"  tool error rate              {summary['tool_error_rate']:.3f}")
print(f"  avg latency                  {summary['avg_latency_s']}s  (target p50 < 12s)")
print(f"  avg tokens in/out            {summary['avg_tokens_in']}/{summary['avg_tokens_out']}")

outdir = ROOT / "evals" / "results"
outdir.mkdir(exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
(outdir / f"agent-{stamp}.json").write_text(
    json.dumps({"summary": summary, "detail": rows}, indent=2))
print(f"\nwrote evals/results/agent-{stamp}.json")