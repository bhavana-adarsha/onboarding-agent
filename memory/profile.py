"""Long-term user profile memory: durable facts about an employee."""
import sys, pathlib, sqlite3, datetime
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from langchain_core.tools import tool

DB = pathlib.Path(__file__).parent.parent / "data" / "meridian.db"

def _init():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS user_facts (
        employee_id TEXT, fact TEXT, created_at TEXT)""")
    con.commit(); con.close()
_init()

def make_profile_tools(employee_id: str):
    @tool
    def remember_about_user(fact: str) -> str:
        """Save one durable fact about this employee for future sessions.
        Use for lasting facts (goals, completed trainings, preferences,
        topics already covered), never for one-off conversation details."""
        con = sqlite3.connect(DB)
        con.execute("INSERT INTO user_facts VALUES (?,?,?)",
                    (employee_id, fact.strip(),
                     datetime.datetime.now().isoformat(timespec="seconds")))
        con.commit(); con.close()
        return f"Saved: {fact.strip()}"

    @tool
    def recall_user_profile() -> str:
        """Read everything remembered about this employee from past sessions.
        Call this before giving study plans or personalized recommendations."""
        con = sqlite3.connect(DB)
        rows = con.execute(
            "SELECT created_at, fact FROM user_facts WHERE employee_id = ? "
            "ORDER BY created_at", (employee_id,)).fetchall()
        con.close()
        if not rows:
            return "No saved facts about this employee yet."
        return "\n".join(f"[{ts}] {f}" for ts, f in rows)

    return [remember_about_user, recall_user_profile]