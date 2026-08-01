"""Retrieval evals: recall@5, precision@5, MRR over the golden set."""
import sys, pathlib, json, sqlite3, datetime
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from rag.retrieve import hybrid_search
from config import CHUNK_SIZE, CHUNK_OVERLAP

ROOT = pathlib.Path(__file__).parent.parent
GOLDEN = json.loads((ROOT / "data" / "golden_set.json").read_text())
K = 5
STRUCTURED = {"glossary", "study_materials", "systems"}

# user -> audience, from the employees table
con = sqlite3.connect(ROOT / "data" / "meridian.db")
AUDIENCE = dict(con.execute("SELECT employee_id, audience FROM employees").fetchall())
con.close()

def corpus_docs(expected):
    return [d for d in expected if d not in STRUCTURED]

rows, skipped = [], []
for q in GOLDEN:
    expected = corpus_docs(q["expected_docs"])
    if not expected:
        skipped.append(q["id"])
        continue
    results = hybrid_search(q["question"], k=K, user_audience=AUDIENCE[q["user"]])
    got_docs = [r["doc_id"] for r in results]

    hits = [d for d in expected if d in got_docs]
    recall = len(hits) / len(expected)
    precision = sum(1 for d in got_docs if d in expected) / K
    rr = 0.0
    for rank, d in enumerate(got_docs, start=1):
        if d in expected:
            rr = 1.0 / rank
            break
    rows.append({"id": q["id"], "recall": recall, "precision": precision,
                 "rr": rr, "expected": expected, "got": got_docs})

n = len(rows)
summary = {
    "recall@5": round(sum(r["recall"] for r in rows) / n, 3),
    "precision@5": round(sum(r["precision"] for r in rows) / n, 3),
    "mrr": round(sum(r["rr"] for r in rows) / n, 3),
    "n_questions": n,
    "settings": {"chunk_size": CHUNK_SIZE, "chunk_overlap": CHUNK_OVERLAP, "k": K},
}

print(f"Evaluated {n} questions, skipped {len(skipped)} (structured/no-doc): {skipped}\n")
print(f"  Recall@5    {summary['recall@5']:.3f}   (target ≥ 0.90)")
print(f"  Precision@5 {summary['precision@5']:.3f}   (target ≥ 0.60)")
print(f"  MRR         {summary['mrr']:.3f}   (target ≥ 0.80)\n")

misses = [r for r in rows if r["recall"] < 1.0]
print(f"{len(misses)} questions with missed docs:")
for r in misses:
    missing = [d for d in r["expected"] if d not in r["got"]]
    print(f"  {r['id']}: missing {missing}, got {r['got']}")

outdir = ROOT / "evals" / "results"
outdir.mkdir(exist_ok=True)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
(outdir / f"retrieval-{stamp}.json").write_text(
    json.dumps({"summary": summary, "detail": rows}, indent=2))
print(f"\nwrote evals/results/retrieval-{stamp}.json")