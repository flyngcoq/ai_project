import json
import urllib.request
from core.config import OLLAMA_API_URL, MODEL_NAME

def generate_with_ollama(system_prompt: str, user_content: str = "", model: str = None, images: list = None) -> str:
    target_model = model if model else MODEL_NAME
    messages = [{"role": "system", "content": system_prompt}]
    user_msg = {"role": "user", "content": user_content}
    if images:
        user_msg["images"] = images
    messages.append(user_msg)
    
    data = {
        "model": target_model,
        "messages": messages,
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("message", {}).get("content", "")
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return None

def stream_with_ollama(system_prompt: str, user_content: str = "", model: str = None):
    target_model = model if model else MODEL_NAME
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    
    data = {
        "model": target_model,
        "messages": messages,
        "stream": True
    }
    
    req = urllib.request.Request(
        OLLAMA_API_URL, 
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if chunk.get("done"):
                        break
    except Exception as e:
        print(f"Error streaming with Ollama: {e}")
        yield f"❌ 스트리밍 오류: {str(e)}"
