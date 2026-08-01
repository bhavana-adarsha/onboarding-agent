"""Build a SQLite FTS5 keyword index over all chunks."""
import sys, pathlib, json, sqlite3
sys.path.append(str(pathlib.Path(__file__).parent.parent))

CHUNKS = json.loads((pathlib.Path(__file__).parent.parent / "data" / "chunks.json").read_text())
DB = pathlib.Path(__file__).parent.parent / "data" / "fts.db"

con = sqlite3.connect(DB)
cur = con.cursor()
cur.executescript("""
DROP TABLE IF EXISTS chunks_fts;
CREATE VIRTUAL TABLE chunks_fts USING fts5(
  chunk_id UNINDEXED,
  doc_id UNINDEXED,
  audience UNINDEXED,
  last_updated UNINDEXED,
  text
);
""")
cur.executemany(
    "INSERT INTO chunks_fts VALUES (?,?,?,?,?)",
    [(c["chunk_id"], c["doc_id"], c["audience"], c["last_updated"], c["text"]) for c in CHUNKS],
)
con.commit()
print(f"indexed {cur.execute('SELECT COUNT(*) FROM chunks_fts').fetchone()[0]} chunks into {DB.name}")

def fts_escape(q):
    """Make any string safe for FTS5 MATCH: quote each token as a literal."""
    tokens = q.split()
    return " ".join('"' + t.replace('"', '""') + '"' for t in tokens)

# Sanity queries: exact-term lookups where keyword search shines
def fts_escape(q):
    """Make any string safe for FTS5 MATCH: quote each token as a literal."""
    tokens = q.split()
    return " ".join('"' + t.replace('"', '""') + '"' for t in tokens)

for q in ["TimeTrax", "EOB", "MHP-3847"]:
    escaped = fts_escape(q)
    print(f"\n'{q}'  ->  MATCH {escaped}")
    rows = cur.execute(
        "SELECT chunk_id, bm25(chunks_fts) FROM chunks_fts WHERE chunks_fts MATCH ? "
        "ORDER BY bm25(chunks_fts) LIMIT 3", (escaped,)
    ).fetchall()
    for cid, score in rows:
        print(f"  {cid}  bm25={score:.2f}")
con.close()