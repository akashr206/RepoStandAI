import os
from pathlib import Path
IGNORE_DIRS = {
    "node_modules", ".git", ".next", "dist", "build"
}

IGNORE_EXTENSIONS = {
    ".lock", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".webp", ".ico", ".woff", ".woff2",
    ".ttf", ".eot", "package-lock.json"
}

def ignore_files(path: Path):
    if any(part in IGNORE_DIRS for part in path.parts):
        return True

    if path.suffix in IGNORE_EXTENSIONS:
        return True

    return False

def build_tree_json(path):
    tree = {}
    for item in os.listdir(path):
        if(ignore_files(Path(item))):
            continue
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree[item] = build_tree_json(full_path)
        else:
            tree[item] = None
    return tree
