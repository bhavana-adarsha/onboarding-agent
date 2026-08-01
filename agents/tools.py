"""Tools for the onboarding agent. Built per-user so access level is baked in."""
import sys, pathlib, sqlite3
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from langchain_core.tools import tool
from rag.retrieve import hybrid_search

DB = pathlib.Path(__file__).parent.parent / "data" / "meridian.db"

def make_tools(user_audience: str, employee_id: str):
    """Return the tool list for one logged-in user. Audience is fixed here,
    at construction time, so the model can never choose its own access level."""

    @tool
    def search_docs(query: str) -> str:
        """Search company wikis, runbooks, and HR policies. Use this for any
        question about how an application works, a workflow, a process, or a
        policy. Returns document excerpts tagged with doc_id and last_updated."""
        chunks = hybrid_search(query, k=5, user_audience=user_audience)
        if not chunks:
            return "No documents found for that query."
        return "\n\n".join(
            f"<document doc_id='{c['doc_id']}' last_updated='{c['last_updated']}'>\n"
            f"{c['text']}\n</document>" for c in chunks)

    @tool
    def lookup_glossary(term: str) -> str:
        """Look up one internal acronym or jargon term (like EOB or clean claim)
        in the company glossary. Pass just the term itself."""
        con = sqlite3.connect(DB)
        row = con.execute(
            "SELECT term, definition FROM glossary WHERE term = ? COLLATE NOCASE",
            (term.strip(),)).fetchone()
        if not row:
            row = con.execute(
                "SELECT term, definition FROM glossary WHERE term LIKE ? LIMIT 1",
                (f"%{term.strip()}%",)).fetchone()
        con.close()
        return f"{row[0]}: {row[1]}" if row else f"'{term}' is not in the glossary."

    @tool
    def list_study_materials(role: str = "all", topic: str = "") -> str:
        """List recommended study materials for a new hire. role is one of:
        all, data-analyst, claims-specialist, engineer. topic is optional, one of:
        claimsflow, carebridge, pulseboard, timetrax, data, security, hr-basics."""
        con = sqlite3.connect(DB)
        sql = ("SELECT title, url, topic, level, est_hours FROM study_materials "
               "WHERE role IN ('all', ?)")
        args = [role]
        if topic:
            sql += " AND topic = ?"
            args.append(topic)
        rows = con.execute(sql + " ORDER BY level, est_hours", args).fetchall()
        con.close()
        if not rows:
            return "No materials match."
        return "\n".join(f"- {t} [{tp}, {lv}, {h}h] {u}" for t, u, tp, lv, h in rows)

    return [search_docs, lookup_glossary, list_study_materials]

if __name__ == "__main__":
    tools = make_tools("all", "emp-001")
    print(tools[0].invoke({"query": "PTO vacation days"})[:300], "\n")
    print(tools[1].invoke({"term": "EOB"}), "\n")
    print(tools[2].invoke({"role": "data-analyst", "topic": "data"}))