from fastapi import APIRouter
from langchain_text_splitters import JSFrameworkTextSplitter
router = APIRouter()

@router.get("/test")
def test():
    splitter = JSFrameworkTextSplitter(chunk_size=1000, chunk_overlap=200)
    path = "repos/A9fr6Zqaa5/components/Contact.jsx"
    with open(path, "r") as f:
        content = f.read()
    chunks = splitter.split_text(content)
    for chunk in  chunks:
        print("-------- chunk --------")
        print(chunk)
    return {"message": "Test successful", "chunks": chunks}

test()