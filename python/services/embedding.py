from supabase import create_client
from dotenv import load_dotenv
from langchain_text_splitters import JSFrameworkTextSplitter
from pathlib import Path
from utils.embed import embed
import os
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

IGNORE_DIRS = {
    "node_modules", ".git", ".next", "dist", "build"
}

IGNORE_EXTENSIONS = {
    ".lock", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".webp", ".ico", ".woff", ".woff2",
    ".ttf", ".eot"
}

def ignore_files(path: Path):
    if any(part in IGNORE_DIRS for part in path.parts):
        return True

    if path.suffix in IGNORE_EXTENSIONS:
        return True

    return False
BASE_PATH = Path("repos")

def embed_file(repo_id: str):
    try:
        repo_path = BASE_PATH / repo_id
        rows = []
        for file in repo_path.rglob("*"):
            if not file.is_file():
                continue
            relative_path = file.relative_to(repo_path)
            if(ignore_files(relative_path)):
                continue
            if(file.stat().st_size > 5_000_000):
                continue
            print("Embedding : ", file)
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                # print(file.split(".")[-1])
                content = f.read()
                splitter = JSFrameworkTextSplitter(chunk_size=700, chunk_overlap=100)
                chunks = splitter.split_text(content)
                print("Len of chunk: ", len(chunks))
                res = embed(chunks)
                if(res["success"]):
                    embeddings = res["embedding"]
                    for i in range(len(embeddings)):
                        rows.append({
                            "repo_id": repo_id,
                            "file_path": str(relative_path).replace("\\", "/"),
                            "embedding": embeddings[i],
                            "content": chunks[i]
                        })

        if rows:
            supabase.table("embeddings").insert(rows).execute()

        return {"success" : True}
    except Exception as e:
        print(e)
        return {"error": e}

embed_file("ALKbSdsNA8")