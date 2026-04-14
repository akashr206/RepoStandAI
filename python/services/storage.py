import os
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path

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

def store_repo(repo_id: str):
    try:
        repo_path = BASE_PATH / repo_id

        for path in repo_path.rglob("*"):
            if not path.is_file():
                continue

            relative_path = path.relative_to(repo_path)
            relative_str = str(relative_path).replace("\\", "/")
            # print(relative_str)
            if ignore_files(relative_path):
                continue

            if path.stat().st_size > 5_000_000:
                continue

            try:
                with open(path, "rb") as f:
                    supabase.storage.from_("repos").upload(
                        f"{repo_id}/{relative_str}",
                        f,
                        {"content-type": "application/octet-stream"}
                    )
                pass
            except Exception as e:
                print(f"Skipping {relative_str}: {e}")

        return {"success": True}

    except Exception as e:
        print(e)
        return {"error": str(e)}
