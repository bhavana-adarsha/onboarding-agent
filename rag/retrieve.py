"""Retrieval module. Vector search now, hybrid added in step 11."""
import sys, pathlib, json, sqlite3
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import boto3
import chromadb
from config import REGION, EMBEDDINGS

_client = boto3.client("bedrock-runtime", region_name=REGION)
_chroma = chromadb.PersistentClient(
    path=str(pathlib.Path(__file__).parent.parent / "data" / "chroma"))
_col = _chroma.get_collection("corpus")

def embed(text):
    resp = _client.invoke_model(
        modelId=EMBEDDINGS,
        body=json.dumps({"inputText": text, "dimensions": 1024, "normalize": True}),
    )
    return json.loads(resp["body"].read())["embedding"]

def fts_escape(q, mode="OR"):
    """FTS5-safe query. OR = recall-oriented (retrieval), AND = strict lookup."""
    tokens = ['"' + t.replace('"', '""') + '"' for t in q.split()]
    return (" OR " if mode == "OR" else " ").join(tokens)

def allowed_audiences(user_audience):
    """Map a user's audience level to the chunk audiences they may see."""
    return ["all"] if user_audience == "all" else ["all", "managers"]

def vector_search(query, k=5, user_audience="all"):
    """Return top-k chunks by cosine similarity, access-filtered in the DB."""
    res = _col.query(
        query_embeddings=[embed(query)],
        n_results=k,
        where={"audience": {"$in": allowed_audiences(user_audience)}},
    )
    return [
        {"chunk_id": cid, "text": doc, "distance": dist, **meta}
        for cid, doc, dist, meta in zip(
            res["ids"][0], res["documents"][0], res["distances"][0], res["metadatas"][0])
    ]

_fts = sqlite3.connect(
    str(pathlib.Path(__file__).parent.parent / "data" / "fts.db"),
    check_same_thread=False)

def keyword_search(query, k=5, user_audience="all"):
    """Top-k chunks by BM25, access-filtered in SQL."""
    placeholders = ",".join("?" for _ in allowed_audiences(user_audience))
    rows = _fts.execute(
        f"SELECT chunk_id, doc_id, audience, last_updated, text, bm25(chunks_fts) "
        f"FROM chunks_fts WHERE chunks_fts MATCH ? AND audience IN ({placeholders}) "
        f"ORDER BY bm25(chunks_fts) LIMIT ?",
        (fts_escape(query), *allowed_audiences(user_audience), k),
    ).fetchall()
    return [
        {"chunk_id": r[0], "doc_id": r[1], "audience": r[2],
         "last_updated": r[3], "text": r[4], "bm25": r[5]}
        for r in rows
    ]

def hybrid_search(query, k=5, user_audience="all", fetch_k=8, rrf_c=60):
    """Fuse vector and keyword results with reciprocal rank fusion."""
    vec = vector_search(query, k=fetch_k, user_audience=user_audience)
    kw = keyword_search(query, k=fetch_k, user_audience=user_audience)

    scores, seen = {}, {}
    for results in (vec, kw):
        for rank, r in enumerate(results):
            cid = r["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rank + rrf_c)
            seen[cid] = r

    ranked = sorted(scores, key=scores.get, reverse=True)[:k]
    out = []
    for cid in ranked:
        r = seen[cid]
        out.append({"chunk_id": cid, "doc_id": r["doc_id"], "audience": r["audience"],
                    "last_updated": r["last_updated"], "text": r["text"],
                    "rrf": scores[cid],
                    "in_vector": any(x["chunk_id"] == cid for x in vec),
                    "in_keyword": any(x["chunk_id"] == cid for x in kw)})
    return out

if __name__ == "__main__":
    tests = [
        ("how many vacation days do I get", "all"),
        ("what is ticket MHP-3847 about", "all"),
        ("TimeTrax timesheet deadline", "all"),
        ("how do I run a 90-day performance review", "all"),
    ]
    for q, aud in tests:
        print(f"\n=== '{q}'  (audience={aud})")
        for r in hybrid_search(q, k=5, user_audience=aud):
            src = ("V" if r["in_vector"] else "-") + ("K" if r["in_keyword"] else "-")
            print(f"  [{src}] {r['chunk_id']:<12} rrf={r['rrf']:.4f}")
    tests = [
        ("how many vacation days do I get", "all"),
        ("what is ticket MHP-3847 about", "all"),
        ("TimeTrax timesheet deadline", "all"),
        ("how do I run a 90-day performance review", "all"),
    ]
    for q, aud in tests:
        print(f"\n=== '{q}'  (audience={aud})")
        for r in hybrid_search(q, k=5, user_audience=aud):
            src = ("V" if r["in_vector"] else "-") + ("K" if r["in_keyword"] else "-")
            print(f"  [{src}] {r['chunk_id']:<12} rrf={r['rrf']:.4f}")
    tests = [
        ("how many vacation days do I get", "all"),
        ("how do I run a 90-day performance review", "all"),
        ("how do I run a 90-day performance review", "managers"),
        ("what does the reporting dashboard do", "all"),
    ]
    for q, aud in tests:
        print(f"\n=== '{q}'  (audience={aud})")
        for r in vector_search(q, k=5, user_audience=aud):
            print(f"  {r['chunk_id']:<12} dist={r['distance']:.3f}  audience={r['audience']}")