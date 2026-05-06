import sys
import json
import urllib.request

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:26b-a4b-it-q4_K_M"

def query_gemma(prompt):
    """Sends a prompt to the local Ollama instance and returns the response."""
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
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
            return result.get("response", "")
    except Exception as e:
        return f"Error: Failed to connect to local Ollama. {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gemma_bridge.py [your prompt]")
        sys.exit(1)
        
    user_prompt = " ".join(sys.argv[1:])
    response = query_gemma(user_prompt)
    print(response)
