import subprocess

def clone_repo(repo_url: str, repo_id: str):
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, f"repos/{repo_id}"], check=True)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        print(e)
        return {"error": e}