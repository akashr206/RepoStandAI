from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
from routes import repo

load_dotenv()

app = FastAPI()
app.include_router(repo.router, prefix="/api/repo")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)