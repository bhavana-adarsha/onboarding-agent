# Model IDs for the whole project. Change here, changes everywhere.
REGION = "us-east-1"
HAIKU = "us.anthropic.claude-haiku-4-5-20251001-v1:0"     # workers, doc generation
SONNET = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"   # supervisor, judge (later)
EMBEDDINGS = "amazon.titan-embed-text-v2:0"        # RAG (later)
# RAG settings (tuned in step 13 against retrieval evals)
CHUNK_SIZE = 2400      # characters, ~600 tokens
CHUNK_OVERLAP = 400    # characters, ~100 tokens