"""Episodic memory: log every turn, embed questions, recall by similarity."""
import sys, pathlib, sqlite3, datetime
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import chromadb
from langchain_core.tools import tool
from rag.retrieve import embed

ROOT = pathlib.Path(__file__).parent.parent
DB = ROOT / "data" / "meridian.db"
_chroma = chromadb.PersistentClient(path=str(ROOT / "data" / "chroma"))
_episodes = _chroma.get_or_create_collection("episodes",
                                             metadata={"hnsw:space": "cosine"})

def _init():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS episodes (
        episode_id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT,
        employee_id TEXT, question TEXT, answer TEXT)""")
    con.commit(); con.close()
_init()

def log_turn(employee_id: str, question: str, answer: str):
    con = sqlite3.connect(DB)
    cur = con.execute("INSERT INTO episodes (ts, employee_id, question, answer) "
                      "VALUES (?,?,?,?)",
                      (datetime.datetime.now().isoformat(timespec="seconds"),
                       employee_id, question, answer))
    con.commit()
    _episodes.add(ids=[str(cur.lastrowid)], embeddings=[embed(question)],
                  documents=[question], metadatas=[{"employee_id": employee_id}])
    con.close()

def make_episodic_tools(employee_id: str):
    @tool
    def recall_similar_questions(query: str) -> str:
        """Search this employee's past questions from previous sessions.
        Use when they reference something discussed before ('like you said',
        'that thing I asked about') or repeat a topic."""
        if _episodes.count() == 0:
            return "No past questions logged yet."
        res = _episodes.query(query_embeddings=[embed(query)], n_results=3,
                              where={"employee_id": employee_id})
        if not res["ids"][0]:
            return "No similar past questions."
        con = sqlite3.connect(DB)
        out = []
        for eid in res["ids"][0]:
            row = con.execute("SELECT ts, question, answer FROM episodes "
                              "WHERE episode_id = ?", (eid,)).fetchone()
            out.append(f"[{row[0]}] Q: {row[1]}\nA: {row[2][:200]}")
        con.close()
        return "\n\n".join(out)
    return [recall_similar_questions]