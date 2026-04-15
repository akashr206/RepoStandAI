import subprocess
from pathlib import Path
import shutil
import os
import stat

def force_remove(func, path, _):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        pass  


def clone_repo(repo_url: str, repo_id: str):
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, f"repos/{repo_id}"], check=True)
        git_path = Path(f"repos/{repo_id}") / ".git"
        if git_path.exists():
            shutil.rmtree(git_path, onerror=force_remove)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        print(e)
        return {"error": e}
