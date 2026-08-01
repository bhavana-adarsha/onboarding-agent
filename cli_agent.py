"""Agent CLI, final Phase 2: agent + 3 memory tiers + turn logging."""
import sys, sqlite3, pathlib, time
sys.path.append(str(pathlib.Path(__file__).parent))

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from agents.knowledge_agent import build_agent
from memory.profile import make_profile_tools
from memory.episodic import make_episodic_tools, log_turn

ROOT = pathlib.Path(__file__).parent
con = sqlite3.connect(ROOT / "data" / "meridian.db")
ROWS = con.execute(
    "SELECT employee_id, name, role, team, audience FROM employees").fetchall()
con.close()
EMPLOYEES = {r[0]: {"employee_id": r[0], "name": r[1], "role": r[2],
                    "team": r[3], "audience": r[4]} for r in ROWS}

for eid, e in EMPLOYEES.items():
    print(f"  {eid}: {e['name']} ({e['role']}, audience={e['audience']})")
uid = input("\nLogin as [emp-001]: ").strip() or "emp-001"
emp = EMPLOYEES[uid]

checkpointer = SqliteSaver(sqlite3.connect(ROOT / "data" / "checkpoints.db",
                                           check_same_thread=False))
graph = build_agent(
    emp, checkpointer=checkpointer,
    extra_tools=(make_profile_tools(emp["employee_id"])
                 + make_episodic_tools(emp["employee_id"])),
    extra_rules="""
8. When the user states a durable fact about themselves (a goal, a completed
   training, a preference, a topic finished), save it with remember_about_user.
9. Before recommending study materials or plans, call recall_user_profile and
   do not re-recommend what they already completed.
10. If the user references a past conversation, use recall_similar_questions.""")

thread = input(f"Thread id [{uid}-main]: ").strip() or f"{uid}-main"
cfg = {"configurable": {"thread_id": thread}}
print(f"Logged in as {emp['name']}, thread '{thread}'. 'quit' to exit.\n")

while True:
    q = input(f"{emp['name']}> ").strip()
    if q.lower() in ("quit", "exit", ""):
        break
    t0 = time.time()
    result = graph.invoke({"messages": [HumanMessage(content=q)]}, cfg)
    answer = result["messages"][-1].content
    log_turn(emp["employee_id"], q, str(answer))
    print(f"\n{answer}\n")
    print(f"  [{time.time() - t0:.1f}s]\n")