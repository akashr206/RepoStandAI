from services.git_cloner import clone_repo
from services.storage import store_repo
from services.embedding import embed_file
from supabase import create_client
from dotenv import load_dotenv
from services.store_summary import store_summary
import os
import shutil

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def force_remove(func, path, _):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        pass  


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
        shutil.rmtree(f"repos/{repo_id}", onerror=force_remove)
        return

    print("stored")

    result = embed_file(repo_id)
    if result.get("error"):
        print("error embedding")
        supabase.table("repos").update({"status": "failed"}).eq("id", repo_id).execute()
        shutil.rmtree(f"repos/{repo_id}", onerror=force_remove)
        return

    print("embedded")

    result = store_summary(repo_id)
    if result.get("error"):
        print("error storing summary")
        supabase.table("repos").update({"status": "failed"}).eq("id", repo_id).execute()
        shutil.rmtree(f"repos/{repo_id}", onerror=force_remove)
        return
    print("summary stored")

    supabase.table("repos").update({"status": "success"}).eq("id", repo_id).execute()
    shutil.rmtree(f"repos/{repo_id}", onerror=force_remove)
    return

# process_repo("https://github.com/akashr206/portfolio", "a8gLpOOzmp")