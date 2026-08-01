"""Embed chunks with Titan v2 and load them into ChromaDB."""
import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).parent.parent))

import boto3
import chromadb
from config import REGION, EMBEDDINGS

client = boto3.client("bedrock-runtime", region_name=REGION)
CHUNKS = json.loads((pathlib.Path(__file__).parent.parent / "data" / "chunks.json").read_text())
DB_DIR = str(pathlib.Path(__file__).parent.parent / "data" / "chroma")

def embed(text):
    """One Titan v2 call -> list of 1024 floats."""
    resp = client.invoke_model(
        modelId=EMBEDDINGS,
        body=json.dumps({"inputText": text, "dimensions": 1024, "normalize": True}),
    )
    return json.loads(resp["body"].read())["embedding"]

chroma = chromadb.PersistentClient(path=DB_DIR)
try:
    chroma.delete_collection("corpus")   # rebuild from scratch each run
except Exception:
    pass
col = chroma.create_collection("corpus", metadata={"hnsw:space": "cosine"})

for i, c in enumerate(CHUNKS):
    col.add(
        ids=[c["chunk_id"]],
        embeddings=[embed(c["text"])],
        documents=[c["text"]],
        metadatas=[{
            "doc_id": c["doc_id"],
            "source_type": c["source_type"],
            "audience": c["audience"],
            "last_updated": c["last_updated"],
        }],
    )
    if (i + 1) % 10 == 0:
        print(f"embedded {i + 1}/{len(CHUNKS)}")

print(f"done: {col.count()} chunks in ChromaDB at data/chroma/")

# Sanity query
q = "how many vacation days do I get"
res = col.query(query_embeddings=[embed(q)], n_results=3)
print(f"\nsanity query: '{q}'")
for cid, dist in zip(res["ids"][0], res["distances"][0]):
    print(f"  {cid}  distance={dist:.3f}")