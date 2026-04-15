from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils.file_structure import build_tree_json
load_dotenv()

def gemini_chat(system_prompt: str, user_prompt: str):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
            contents=user_prompt,
        )
        return {"success": True, "response": response.text}
    except Exception as e:
        return {"error": e}

