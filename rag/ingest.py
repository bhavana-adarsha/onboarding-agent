"""Parse corpus docs, split into chunks, write chunks.json for inspection."""
import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import yaml
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

CORPUS = pathlib.Path(__file__).parent.parent / "data" / "corpus"
OUT = pathlib.Path(__file__).parent.parent / "data" / "chunks.json"

def parse_doc(path):
    """Split frontmatter from body. Returns (metadata dict, body str)."""
    raw = path.read_text()
    _, fm, body = raw.split("---", 2)
    return yaml.safe_load(fm), body.strip()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n## ", "\n# ", "\n\n", "\n", " "],  # prefer header boundaries
)

chunks = []
for path in sorted(CORPUS.glob("*.md")):
    meta, body = parse_doc(path)
    pieces = splitter.split_text(body)
    for i, piece in enumerate(pieces):
        chunks.append({
            "chunk_id": f"{meta['doc_id']}#{i}",
            "text": piece,
            "doc_id": meta["doc_id"],
            "source_type": meta["source_type"],
            "audience": meta["audience"],
            "last_updated": str(meta["last_updated"]),
        })

OUT.write_text(json.dumps(chunks, indent=2))

# Stats: this is what you compare when tuning
sizes = [len(c["text"]) for c in chunks]
docs = len(set(c["doc_id"] for c in chunks))
print(f"{len(chunks)} chunks from {docs} docs")
print(f"chars per chunk: min {min(sizes)}, avg {sum(sizes)//len(sizes)}, max {max(sizes)}")
per_doc = {}
for c in chunks:
    per_doc[c["doc_id"]] = per_doc.get(c["doc_id"], 0) + 1
multi = {k: v for k, v in per_doc.items() if v > 1}
print(f"docs split into multiple chunks: {len(multi)} -> {multi}")