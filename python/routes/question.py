from fastapi import APIRouter
from supabase import create_client
import os
from dotenv import load_dotenv
from services.question_chain import process_question

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

    if not response.data or response.data[0]["status"] != "success":
        return {"error": "Repo not processed yet or processing has failed"}
    
    response = process_question(repo_id, question)
    return {"response": response}