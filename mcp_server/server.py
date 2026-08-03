"""MCP server exposing the Meridian onboarding tools over stdio.
Audience is resolved at startup from MERIDIAN_EMPLOYEE_ID: the model
never chooses the access level."""
import sys, os, pathlib, sqlite3
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from rag.retrieve import hybrid_search

DB = pathlib.Path(__file__).parent.parent / "data" / "meridian.db"
EMPLOYEE_ID = os.environ.get("MERIDIAN_EMPLOYEE_ID", "emp-001")

con = sqlite3.connect(DB)
row = con.execute("SELECT audience FROM employees WHERE employee_id = ?",
                  (EMPLOYEE_ID,)).fetchone()
con.close()
AUDIENCE = row[0] if row else "all"

mcp = FastMCP("meridian-onboarding")

@mcp.tool()
def search_docs(query: str) -> str:
    """Search company wikis, runbooks, and HR policies. Use for any question
    about how an application works, a workflow, a process, or a policy.
    Returns document excerpts tagged with doc_id and last_updated."""
    chunks = hybrid_search(query, k=5, user_audience=AUDIENCE)
    if not chunks:
        return "No documents found for that query."
    return "\n\n".join(
        f"<document doc_id='{c['doc_id']}' last_updated='{c['last_updated']}'>\n"
        f"{c['text']}\n</document>" for c in chunks)

@mcp.tool()
def lookup_glossary(term: str) -> str:
    """Look up one internal acronym or jargon term (like EOB) in the company
    glossary. Pass just the term itself."""
    con = sqlite3.connect(DB)
    row = con.execute("SELECT term, definition FROM glossary "
                      "WHERE term = ? COLLATE NOCASE", (term.strip(),)).fetchone()
    if not row:
        row = con.execute("SELECT term, definition FROM glossary "
                          "WHERE term LIKE ? LIMIT 1", (f"%{term.strip()}%",)).fetchone()
    con.close()
    return f"{row[0]}: {row[1]}" if row else f"'{term}' is not in the glossary."

@mcp.tool()
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

if __name__ == "__main__":
    mcp.run()   # stdio transport