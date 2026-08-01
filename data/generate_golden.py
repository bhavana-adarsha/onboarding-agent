"""Generate routine golden questions, one per corpus doc, grounded in doc text."""
import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import boto3
from config import REGION, HAIKU

client = boto3.client("bedrock-runtime", region_name=REGION)
CORPUS = pathlib.Path(__file__).parent / "corpus"
SKIP = {"wiki-012", "run-008", "pol-001", "pol-002"}  # traps are handcrafted

PROMPT = """Below is an internal company document.

{doc}

Write ONE question a new employee would realistically ask that this document
answers, and a 2-3 sentence reference answer using ONLY facts from the document.
Output ONLY JSON: {{"question": "...", "reference_answer": "..."}}"""

items = []
for i, path in enumerate(sorted(CORPUS.glob("*.md"))):
    doc_id = path.stem
    if doc_id in SKIP:
        continue
    resp = client.converse(
        modelId=HAIKU,
        messages=[{"role": "user", "content": [{"text": PROMPT.format(doc=path.read_text())}]}],
        inferenceConfig={"maxTokens": 500, "temperature": 0.7},
    )
    text = resp["output"]["message"]["content"][0]["text"]
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    qa = json.loads(text)
    items.append({
        "id": f"q-g{i:02d}",
        "question": qa["question"],
        "category": "answerable",
        "user": "emp-001",
        "expected_route": "knowledge",
        "expected_docs": [doc_id],
        "reference_answer": qa["reference_answer"],
    })
    print(f"{doc_id}: {qa['question']}")

handcrafted = json.loads((pathlib.Path(__file__).parent / "golden_handcrafted.json").read_text())
golden = handcrafted + items
(pathlib.Path(__file__).parent / "golden_set.json").write_text(json.dumps(golden, indent=2))
print(f"\nGolden set: {len(golden)} questions ({len(handcrafted)} handcrafted, {len(items)} generated)")