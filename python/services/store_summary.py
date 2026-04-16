from supabase import create_client
from utils.gemini import gemini_chat
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_structure import build_tree_json
from dotenv import load_dotenv
from utils.embed import embed
import os

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def store_summary(repo_id: str):
    try:    
        file_tree = build_tree_json(f"repos/{repo_id}")

        if "package.json" in file_tree:
            with open(f"repos/{repo_id}/package.json", "r") as f:
                dependencies = f.read() 
        else:
            dependencies = "No dependencies found in the repository"

        response = gemini_chat("You are an expert repository summarizer. You are given a file structure of a repository and its dependencies contents, your task is to summarize the repository efficiently in 100-150 words. Be confident with your response.", f"File Structure:\n{file_tree}\nDependencies:\n{dependencies}")
        
        if response.get("error"):
            print("error gemini", response["error"])
            return {"error": response["error"]}

        print("Summary of the repo: ", response["response"])
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_text(response["response"])
        chunks = list(map(lambda x: "Summary of the repo: " + x, chunks))
        res = embed(chunks)
        rows = []
        if(res["success"]):
            embeddings = res["embedding"]
            for i in range(len(embeddings)):
                rows.append({
                    "repo_id": repo_id,
                    "file_path": "summary",
                    "embedding": embeddings[i],
                    "content": chunks[i]
                })
        if rows:
            supabase.table("embeddings").insert(rows).execute()
        supabase.table("repos").update({"summary": response["response"]}).eq("id", repo_id).execute()
        return {"success": True}
    except Exception as e:
        print("error storing summary", e)
        return {"error": e}