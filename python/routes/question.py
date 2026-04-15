from fastapi import APIRouter
from utils.embed import embed
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
router = APIRouter()

@router.post("/")
def question(body: dict):
    repo_id = body["repo_id"]
    question = body["question"]
    if not repo_id or not question:
        return {"error": "Missing repo_id or question"}
    response = supabase.table("repos").select("status").eq("id", repo_id).execute()
    if response.data[0]["status"] != "success":
        return {"error": "Repo not processed yet or processing has failed"}

    question_embedding = embed([question])
    if not question_embedding["success"]:
        return {"error": "Failed to embed question"}
    
    reponse = supabase.rpc("match_embeddings", {
        "query_embedding": question_embedding["embedding"][0],
        "repo_id_input": repo_id,
        "match_count": 10
    }).execute()
    return {"response": reponse.data}