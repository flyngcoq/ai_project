import os
import json
import urllib.request
import datetime
import shutil
from pathlib import Path

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:26b-a4b-it-q4_K_M"
VAULT_DIR = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault")
FLEETING_DIR = VAULT_DIR / "10_Fleeting_Notes"
LIT_DIR = VAULT_DIR / "20_Literature_Notes"
PERM_DIR = VAULT_DIR / "30_Permanent_Notes"
PROJECTS_DIR = VAULT_DIR / "40_Projects"

PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_with_ollama(prompt, context_text):
    data = {
        "model": MODEL_NAME,
        "prompt": f"{prompt}\n\n[DATA TO PROCESS]\n{context_text}",
        "stream": False
    }
    req = urllib.request.Request(OLLAMA_API_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("response", "")
    except Exception as e:
        print(f"Ollama API Error: {e}")
        return None

def publish_to_confluence(title, content_md):
    # Try to load .env variables manually
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("No .env file found. Skipping Confluence publish.")
        return False
    
    confl_url = None
    confl_email = None
    confl_token = None
    confl_space = None

    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, val = line.strip().split('=', 1)
                if key == 'CONFLUENCE_URL': confl_url = val
                elif key == 'CONFLUENCE_EMAIL': confl_email = val
                elif key == 'CONFLUENCE_TOKEN': confl_token = val
                elif key == 'CONFLUENCE_SPACE_KEY': confl_space = val

    if not all([confl_url, confl_email, confl_token, confl_space]):
        print("Missing required Confluence environment variables. Skipping publish.")
        return False
        
    print(f"Publishing to Confluence Space: {confl_space}...")
    
    # Very basic Markdown to HTML conversion for Confluence
    # In a real scenario, use markdown library. For now, simple replacements.
    html_content = content_md.replace('\n', '<br>')
    
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": confl_space},
        "body": {
            "storage": {
                "value": html_content,
                "representation": "storage"
            }
        }
    }
    
    import base64
    auth_str = f"{confl_email}:{confl_token}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    
    req = urllib.request.Request(
        f"{confl_url}/rest/api/content",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_b64}'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201]:
                print("✅ Successfully published to Confluence!")
                return True
    except Exception as e:
        print(f"Confluence API Error: {e}")
        return False
    
    return False

def main():
    print("Collecting data from the last 7 days...")
    
    now = datetime.datetime.now()
    seven_days_ago = now - datetime.timedelta(days=7)
    
    collected_texts = []
    fleeting_files_to_promote = []
    
    for folder in [FLEETING_DIR, LIT_DIR, PERM_DIR]:
        if not folder.exists(): continue
        for file_path in folder.glob("*.md"):
            mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime >= seven_days_ago:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    collected_texts.append(f"--- File: {file_path.name} ---\n{content}\n")
                
                # Mark fleeting notes for promotion
                if folder == FLEETING_DIR:
                    fleeting_files_to_promote.append(file_path)

    if not collected_texts:
        print("No notes updated in the last 7 days. Exiting.")
        return

    print(f"Found {len(collected_texts)} updated notes. Synthesizing Weekly Report...")
    
    combined_text = "\n".join(collected_texts)
    
    report_prompt = """
    You are an expert Project Manager and Analyst.
    Read the following notes collected over the past week and synthesize them into a highly professional "Weekly Team Report".
    
    CRITICAL INSTRUCTIONS:
    - Use Confluence-friendly Markdown.
    - Start with a high-level executive summary (TL;DR).
    - Group the updates logically by Topic or Project.
    - Use markdown tables to summarize key metrics, tasks, or action items if applicable.
    - Use appropriate emojis to make the report engaging.
    - Format headers clearly (e.g. ## 🚀 Key Highlights, ## 📈 Topic Updates, ## ⚠️ Risks & Issues).
    """
    
    report_md = generate_with_ollama(report_prompt, combined_text)
    
    if not report_md:
        print("Failed to generate report.")
        return
        
    date_str = now.strftime("%Y-%m-%d")
    report_title = f"Weekly_Report_{date_str}"
    report_path = PROJECTS_DIR / f"{report_title}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"✅ Saved local report to: {report_path}")
    
    # Auto-Publish to Confluence
    publish_to_confluence(f"Team Weekly Report - {date_str}", report_md)
    
    # Auto-Promotion (Fleeting -> Permanent)
    if fleeting_files_to_promote:
        print(f"Promoting {len(fleeting_files_to_promote)} notes from Fleeting to Permanent...")
        PERM_DIR.mkdir(parents=True, exist_ok=True)
        for f_path in fleeting_files_to_promote:
            target_path = PERM_DIR / f_path.name
            shutil.move(str(f_path), str(target_path))
            print(f"  -> Promoted: {f_path.name}")
            
    print("All tasks completed.")

if __name__ == "__main__":
    main()
