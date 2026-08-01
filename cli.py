"""Interactive CLI for the onboarding assistant. Phase 1: RAG only."""
import sys, sqlite3, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from rag.generate import answer

con = sqlite3.connect(pathlib.Path(__file__).parent / "data" / "meridian.db")
EMPLOYEES = {e[0]: (e[1], e[2], e[3]) for e in
             con.execute("SELECT employee_id, name, role, audience FROM employees")}
con.close()

print("Meridian onboarding assistant. Users:")
for eid, (name, role, aud) in EMPLOYEES.items():
    print(f"  {eid}: {name} ({role}, audience={aud})")
uid = input("\nLogin as [emp-001]: ").strip() or "emp-001"
name, role, aud = EMPLOYEES[uid]
print(f"Logged in as {name}. Ask questions, 'quit' to exit.\n")

total_in = total_out = 0
while True:
    q = input(f"{name}> ").strip()
    if q.lower() in ("quit", "exit", ""):
        break
    r = answer(q, user_audience=aud)
    total_in += r["tokens_in"]; total_out += r["tokens_out"]
    print(f"\n{r['answer']}\n")
    print(f"  [retrieved: {', '.join(r['retrieved'])}]")
    print(f"  [tokens: {r['tokens_in']} in / {r['tokens_out']} out]\n")

print(f"Session total: {total_in} in / {total_out} out")