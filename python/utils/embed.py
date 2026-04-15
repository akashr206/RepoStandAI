from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

def embed(texts: list[str]):
    try:
        model = SentenceTransformer("all-mpnet-base-v2", token=os.getenv("HF_API_KEY"))
        embeddings = model.encode(texts)
        return {"success": True, "embedding": embeddings.tolist()}

    except Exception as e:
        return {"success": False, "error": str(e)}

# embed(["hi", "how are you", "This is embedding test"])