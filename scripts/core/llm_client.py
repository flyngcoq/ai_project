import json
import urllib.request
import urllib.error
from core.config import OLLAMA_API_URL, LOCAL_OLLAMA_URL, MODEL_NAME, SAFE_AI_GATEWAY_TOKEN

def _make_request(url, data, use_token=True):
    """Internal helper to make a request to Ollama with optional token."""
    headers = {'Content-Type': 'application/json'}
    if use_token and SAFE_AI_GATEWAY_TOKEN:
        headers['Authorization'] = f"Bearer {SAFE_AI_GATEWAY_TOKEN}"
    
    return urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )

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
    
    # Try Gateway first
    try:
        req = _make_request(OLLAMA_API_URL, data)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("message", {}).get("content", "")
    except Exception as e:
        # Fallback to Local if Gateway is different from Local and failed
        if OLLAMA_API_URL != LOCAL_OLLAMA_URL:
            try:
                # Silent fallback to local
                local_req = _make_request(LOCAL_OLLAMA_URL, data, use_token=False)
                with urllib.request.urlopen(local_req, timeout=20) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get("message", {}).get("content", "")
            except Exception:
                pass 
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
    
    # Try Gateway first
    try:
        req = _make_request(OLLAMA_API_URL, data)
        # Increased timeout for local models that might need loading time
        with urllib.request.urlopen(req, timeout=15) as response:
            for line in response:
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if chunk.get("done"):
                        break
    except Exception as e:
        # Fallback to Local
        if OLLAMA_API_URL != LOCAL_OLLAMA_URL:
            try:
                local_req = _make_request(LOCAL_OLLAMA_URL, data, use_token=False)
                with urllib.request.urlopen(local_req, timeout=30) as response:
                    for line in response:
                        if line:
                            chunk = json.loads(line.decode('utf-8'))
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                yield content
                            if chunk.get("done"):
                                break
            except Exception as local_e:
                yield f"❌ 로컬 연결 오류: {str(local_e)}"
        else:
            # If OLLAMA_API_URL IS LOCAL_OLLAMA_URL, and it failed
            yield f"❌ 모델 연결 불가 (Ollama 확인 필요): {str(e)}"
