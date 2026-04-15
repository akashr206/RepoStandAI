from fastapi import APIRouter, BackgroundTasks
from nanoid import generate
from supabase import create_client
from dotenv import load_dotenv
from services.process import process_repo
import os

load_dotenv()

router = APIRouter()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@router.post("/ingest")
def ingest_repo(body: dict, background_tasks: BackgroundTasks):
    repo_url = body.get("repo_url")
    if not repo_url:
        return {"error": "Repository URL is required"}
    
    repo_id = generate(size=10)
    repo_name = repo_url.split("/").pop().replace(".git", "")
    response = (
        supabase
        .table("repos")
        .insert({
            "id": repo_id,
            "name": repo_name,
            "status": "processing"
        })
        .execute()
    )

    background_tasks.add_task(process_repo, repo_url, repo_id)
    return {"status": "processing", "repo_id": repo_id}