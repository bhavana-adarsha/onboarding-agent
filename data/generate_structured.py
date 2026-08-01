"""Generate structured SQLite data: study catalog, glossary, systems, employees."""
import sys, pathlib, json, sqlite3
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import boto3
from config import REGION, HAIKU

client = boto3.client("bedrock-runtime", region_name=REGION)
DB = pathlib.Path(__file__).parent / "meridian.db"
COMPANY = (pathlib.Path(__file__).parent / "company.md").read_text()

def ask_json(prompt):
    """Call Claude and parse a JSON array from the reply."""
    resp = client.converse(
        modelId=HAIKU,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 4000, "temperature": 0.5},
    )
    text = resp["output"]["message"]["content"][0]["text"]
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(text)

MATERIALS_PROMPT = f"""Company context:
{COMPANY}

Generate 25 study materials for new hires as a JSON array. Each object:
"title", "url" (fake internal confluence-style link), "topic" (one of:
claimsflow, carebridge, pulseboard, timetrax, data, security, hr-basics),
"role" (one of: all, data-analyst, claims-specialist, engineer),
"level" (intro or advanced), "est_hours" (number, 0.5 to 4).
Cover every topic at least twice. Output ONLY the JSON array, no other text."""

GLOSSARY_PROMPT = f"""Company context:
{COMPANY}

Generate 40 internal glossary entries as a JSON array. Each object: "term"
(acronym or internal jargon, e.g. "EOB", "clean claim"), "definition"
(one sentence). Healthcare claims and internal tooling terms. Output ONLY
the JSON array, no other text."""

materials = ask_json(MATERIALS_PROMPT)
glossary = ask_json(GLOSSARY_PROMPT)
print(f"Generated {len(materials)} materials, {len(glossary)} glossary terms")

# Hardcoded: precision matters here, these drive A2A and access-control tests later
systems = [
    ("ClaimsFlow", "Claims Ops", "Jira ticket to ACCESS project, manager approves", "manager"),
    ("CareBridge", "Care Coordination", "Jira ticket to ACCESS project, manager approves", "manager"),
    ("PulseBoard", "Data & Analytics", "Slack request in #data-access, data lead approves", "data-lead"),
    ("TimeTrax", "HR", "Automatic on day one via Workday", "none"),
    ("GitHub", "Platform Engineering", "Jira ticket, engineering lead approves", "eng-lead"),
    ("Workday", "HR", "Automatic on day one", "none"),
    ("Production DB read-replica", "Platform Engineering", "Jira ticket plus security training cert", "eng-lead"),
]
employees = [
    ("emp-001", "Priya Nair", "Data Analyst", "Data & Analytics", "2026-07-27", "all"),
    ("emp-002", "Marcus Webb", "Claims Ops Manager", "Claims Ops", "2023-02-13", "managers"),
    ("emp-003", "Dana Kim", "Platform Engineer", "Platform Engineering", "2026-07-20", "all"),
]

con = sqlite3.connect(DB)
cur = con.cursor()
cur.executescript("""
DROP TABLE IF EXISTS study_materials;
DROP TABLE IF EXISTS glossary;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS employees;
CREATE TABLE study_materials (id INTEGER PRIMARY KEY, title TEXT, url TEXT,
  topic TEXT, role TEXT, level TEXT, est_hours REAL);
CREATE TABLE glossary (term TEXT PRIMARY KEY, definition TEXT);
CREATE TABLE systems (name TEXT PRIMARY KEY, owner_team TEXT,
  access_process TEXT, approver_role TEXT);
CREATE TABLE employees (employee_id TEXT PRIMARY KEY, name TEXT, role TEXT,
  team TEXT, start_date TEXT, audience TEXT);
""")
cur.executemany("INSERT INTO study_materials (title,url,topic,role,level,est_hours) VALUES (?,?,?,?,?,?)",
    [(m["title"], m["url"], m["topic"], m["role"], m["level"], m["est_hours"]) for m in materials])
cur.executemany("INSERT OR IGNORE INTO glossary VALUES (?,?)",
    [(g["term"], g["definition"]) for g in glossary])
cur.executemany("INSERT INTO systems VALUES (?,?,?,?)", systems)
cur.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?)", employees)
con.commit()
con.close()
print(f"Wrote {DB.name}")