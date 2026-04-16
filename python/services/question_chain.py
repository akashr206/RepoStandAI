
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from utils.embed import embed
from supabase import create_client
import os 
import dotenv

dotenv.load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_context(repo_id: str, question: str):
    question_embedding = embed([question])
    if not question_embedding["success"]:
        return ""
     
    response = supabase.rpc("match_embeddings", {
        "query_embedding": question_embedding["embedding"][0],
        "repo_id_input": repo_id,
        "match_count": 8
    }).execute()
    return response.data

def format_context(context):
    formatted_context = ""
    for item in context:
        formatted_context += f"File: {item['file_path']}\n"
        formatted_context += f"Content: {item['content']}\n\n"
    return formatted_context

def process_question(repo_id: str, question: str):
    context = get_context(repo_id, question)
    formatted_context = format_context(context)
    print("Formatted Context: ", formatted_context)
    prompt = ChatPromptTemplate.from_messages([("system", """
    You are an expert AI assistant for codebase analysis.

    Instructions:
    1. Answer concisely and directly.
    2. Start with a clear conclusion (YES / NO / PARTIAL).
    3. Then provide short supporting points from the context.
    4. You are allowed to make reasonable inferences from code patterns.
    5. If information is incomplete:
    - Still give a best-effort answer
    - Clearly mention uncertainty briefly
    6. Avoid long explanations unless necessary.
    7. Focus on technical clarity, not verbosity.

    For evaluation questions (e.g., correctness, scalability):
    - Give a judgment
    - Support it with evidence from the code
    - Mention limitations briefly
    """), ("user", "Context:\n{context}\n\nQuestion:\n{question}")])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "context": formatted_context,
        "question": question
    })



