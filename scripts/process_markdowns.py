import os
import json
import urllib.request
from pathlib import Path
import shutil
import datetime

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:26b-a4b-it-q4_K_M" # User's running model
VAULT_DIR = Path("/Users/flyngcoq/AI_Project/Obsidian_Vault")
INBOX_DIR = VAULT_DIR / "00_Inbox"
FLEETING_DIR = VAULT_DIR / "10_Fleeting_Notes"
LIT_DIR = VAULT_DIR / "20_Literature_Notes"
PERM_DIR = VAULT_DIR / "30_Permanent_Notes"
ARCHIVE_DIR = VAULT_DIR / "Archive"

SEARCH_DIRS = [PERM_DIR, LIT_DIR, FLEETING_DIR]

TOPIC_PROMPT = """
You are an AI assistant. Read the following text and determine its core topic in exactly 1 to 3 words. 
Output ONLY the topic words joined by underscores (e.g., AI_Security, Python_Coding, Marketing_Strategy). 
Do NOT output any other text, quotes, or punctuation.
"""

def get_existing_topics():
    topics = set()
    for d in SEARCH_DIRS:
        if d.exists():
            for f in d.glob("*.md"):
                topics.add(f.stem)
    return ", ".join(sorted(list(topics)))

def get_summary_prompt():
    existing_topics = get_existing_topics()
    return f"""
You are an expert knowledge management assistant.
Your task is to read the provided markdown document, summarize its core points, and suggest 3-5 relevant tags.

CRITICAL INSTRUCTION FOR WIKILINKS (Graph View):
Here is a list of EXISTING topics in the Vault: [{existing_topics}]
Whenever you mention any of these exact topics (or highly related terms) in your summary, you MUST wrap them in double square brackets like [[TopicName]].
Additionally, if you identify any other NEW important concepts, keywords, or entities, wrap them in double square brackets to create new nodes in the knowledge graph.

Return the output in the following format:

# Summary
[Your summary here with [[Wikilinks]]]

# Tags
#tag1 #tag2 #tag3

# Original Content
[Keep the original content below]

## 병합 히스토리 (Merge History)
- 최초 문서 생성됨.
"""

def get_merge_prompt():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    existing_topics = get_existing_topics()
    return f"""
You are an expert knowledge management assistant.
You are given an EXISTING document and a NEW document on the same topic.
Your task is to merge the NEW document's information into the EXISTING document seamlessly.
- Update the summary to reflect both documents.
- Combine the tags.
- Append the new original content to the existing original content section.
- At the very end of the document, maintain a `## 병합 히스토리 (Merge History)` section. Keep all past history, and append a new bullet point for today ({current_time}): A 1-line summary of what specific information was added/merged from the NEW document.

CRITICAL INSTRUCTION FOR WIKILINKS (Graph View):
Here is a list of EXISTING topics in the Vault: [{existing_topics}]
Whenever you mention any of these exact topics (or highly related terms) in your summary, you MUST wrap them in double square brackets like [[TopicName]].
Additionally, if you identify any other NEW important concepts, keywords, or entities, wrap them in double square brackets to create new nodes in the knowledge graph.

CRITICAL INSTRUCTION FOR CONFLICTS:
If the NEW document directly contradicts or conflicts with the EXISTING document, you MUST include both viewpoints and you MUST start your ENTIRE output with this exact line:
> [!WARNING] 병합 중 내용 충돌이 감지되었습니다. 확인이 필요합니다.

Output the final merged markdown:
"""

def generate_with_ollama(prompt, context_text=""):
    data = {
        "model": MODEL_NAME,
        "prompt": f"{prompt}\n\nDocument:\n{context_text}",
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
        print(f"Error communicating with Ollama: {e}")
        return None

def process_inbox():
    if not INBOX_DIR.exists():
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for d in SEARCH_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    for file_path in INBOX_DIR.glob("*.md"):
        print(f"Processing: {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
            
        # 1. Extract Topic
        topic = generate_with_ollama(TOPIC_PROMPT, new_content)
        if not topic:
            print("Failed to extract topic. Skipping.")
            continue
            
        topic_filename = f"{topic.strip()}.md"
        # Sanitize filename
        topic_filename = "".join(c for c in topic_filename if c.isalnum() or c in ('_', '-', '.'))
        
        # 2. Check if topic exists in any folder (Permanent -> Literature -> Fleeting)
        target_path = None
        for d in SEARCH_DIRS:
            if (d / topic_filename).exists():
                target_path = d / topic_filename
                break
                
        if target_path:
            print(f"Topic '{topic_filename}' found in {target_path.parent.name}. Merging...")
            with open(target_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            combined_text = f"--- EXISTING DOCUMENT ---\n{existing_content}\n\n--- NEW DOCUMENT ---\n{new_content}"
            final_content = generate_with_ollama(get_merge_prompt(), combined_text)
        else:
            print(f"New topic '{topic_filename}' detected. Summarizing...")
            target_path = FLEETING_DIR / topic_filename
            final_content = generate_with_ollama(get_summary_prompt(), new_content)
            
        # 3. Save Output
        if final_content:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Saved processed file to: {target_path}")
            
            # Move the original file to Archive
            shutil.move(str(file_path), str(ARCHIVE_DIR / file_path.name))
            print(f"Moved original to Archive: {file_path.name}")
        else:
            print(f"Failed to process: {file_path.name}")

if __name__ == "__main__":
    print("Starting markdown processing pipeline...")
    process_inbox()
    print("Pipeline finished.")
    
    # Auto-Sync to Github
    sync_script = VAULT_DIR / "sync.sh"
    if sync_script.exists():
        print("Triggering Github Auto-Sync...")
        import subprocess
        try:
            subprocess.run(["bash", str(sync_script)], cwd=str(VAULT_DIR), check=True)
            print("✅ Github Auto-Sync completed.")
        except Exception as e:
            print(f"❌ Error during Github Sync: {e}")
