from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()

client = InferenceClient(token=os.getenv("HF_API_KEY"))

def embed(texts: list[str]):
    try:
        embeddings = []

        for text in texts:
            res = client.feature_extraction(
                text,
                model="BAAI/bge-base-en"
            )

            while isinstance(res[0], list):
                res = res[0]

            embeddings.append(res)
        return {"success": True, "embedding": embeddings}

    except Exception as e:
        return {"success": False, "error": str(e)}