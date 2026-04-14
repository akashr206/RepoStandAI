from services.git_cloner import clone_repo
from services.storage import store_repo
from services.embedding import embed_file
from supabase import create_client
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def process_repo(repo_url: str,repo_id: str):
    print("processing", repo_id)

    result = clone_repo(repo_url, repo_id)
    if result.get("error"):
        print("error cloning")
        supabase.table("repos").update({"status": "failed"}).eq("id", repo_id).execute()
        return

    print("cloned")

    result = store_repo(repo_id)
    if result.get("error"):
        print("error storing")
        supabase.table("repos").update({"status": "failed"}).eq("id", repo_id).execute()
        shutil.rmtree(f"repos/{repo_id}")
        return

    print("stored")

    result = embed_file(repo_id)
    if result.get("error"):
        print("error embedding")
        supabase.table("repos").update({"status": "failed"}).eq("id", repo_id).execute()
        shutil.rmtree(f"repos/{repo_id}")
        return

    print("embedded")
    supabase.table("repos").update({"status": "success"}).eq("id", repo_id).execute()
    shutil.rmtree(f"repos/{repo_id}")
    return