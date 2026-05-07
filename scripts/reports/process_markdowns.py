import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import os
from pathlib import Path
import shutil
import datetime
import re

# Use core modules
from core.config import VAULT_DIR, INBOX_DIR, FLEETING_DIR, LIT_DIR, PERM_DIR, ARCHIVE_DIR, SEARCH_DIRS, MODEL_NAME
from core.llm_client import generate_with_ollama
from core.web_scraper import enrich_content_with_urls
import pandas as pd
import pdfplumber

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
PERM_DIR = VAULT_DIR / "30_Permanent_Notes"
PROJECTS_DIR = VAULT_DIR / "40_Projects"
ATTACHMENTS_DIR = VAULT_DIR / "50_Resources" / "Attachments"
SEARCH_DIRS = [FLEETING_DIR, PERM_DIR, LIT_DIR, PROJECTS_DIR]

def get_category_prompt(text):
    return f"""
당신은 지식 분류 전문가입니다. 다음 텍스트의 내용을 보고 가장 적합한 카테고리를 하나만 선택하세요.
선택 가능 목록: [Work, Wealth]
만약 두 카테고리 모두 적합하지 않다면, 텍스트의 핵심 주제를 나타내는 영어 단어 하나(예: Health, Hobby, Study)를 새로 제안하세요.

응답은 오직 카테고리 단어 하나만 하세요.
예: Work

[텍스트]
{text[:1000]}
"""

def get_topic_prompt(existing_topics):
    return f"""
You are an AI assistant. Read the following text and determine its core topic in exactly 1 to 3 words. 

CRITICAL INSTRUCTIONS:
1. If the text is too short, lacks meaningful information, is just a simple greeting (e.g., 'hello', 'testing', '안녕'), or is otherwise garbage data, output EXACTLY the word "REJECT".
2. Semantic Matching: Here are the EXISTING topics in the knowledge base:
   [{existing_topics}]
   If the text is semantically related to or is a sub-topic of ANY of the existing topics above, you MUST output the EXACT name of that existing topic. (Do not create a new topic if an existing one fits reasonably well).
3. ONLY if it is a completely new topic, output the new topic words joined by underscores (e.g., AI_Security, Python_Coding).

Do NOT output any other text, quotes, or punctuation. Output ONLY the single topic string.
"""

def get_existing_topics():
    topics = set()
    for d in SEARCH_DIRS:
        if d.exists():
            for f in d.rglob("*.md"):
                topics.add(f.stem)
    return ", ".join(sorted(list(topics)))

def get_summary_prompt():
    existing_topics = get_existing_topics()
    style_guide = get_style_guide()
    return f"""
{style_guide}

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

def get_style_guide():
    style_guide_path = VAULT_DIR / "99_System_Prompts/Summary_Style_Guide.md"
    if style_guide_path.exists():
        with open(style_guide_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def get_merge_prompt():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    existing_topics = get_existing_topics()
    style_guide = get_style_guide()
    return f"""
{style_guide}

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

def get_stakeholder_prompt():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"""
You are an expert at analyzing stakeholder intentions and personas from meeting transcripts or reports. 
Read the provided document and check if any of the following stakeholders mentioned in 'stakeholders.md' have made statements or expressed specific intentions:
- 최종보 (Ent.SW프로덕트트라이브 담당)
- 주엄개 (유선사업담당 상무)
- 양은영 (인터넷/보안사업팀 팀장)
- 최연수 (신상품개발TF PM)
- 송후석 (Product Planner)
- 황현주 (Product Planner)
- 박지은 (Product Planner)

If any of these people (or their roles) are identified as speaking or being discussed, extract:
1. Their core intention or request.
2. Their primary concern or stance.
3. A short summary of their 'Persona Insight' from this text.

Format the output EXACTLY as follows for each person found, separated by "---":
---
PERSON: [Person Name from the list above]
INSIGHT: - [{today}]: [Core Intention/Insight summary in 1-2 sentences]
---
If NO stakeholder insights are found, output ONLY "NONE".
"""

def update_stakeholders_file(insights):
    import re
    stakeholders_path = PERM_DIR / "stakeholders.md"
    if not stakeholders_path.exists():
        print("stakeholders.md not found in PERM_DIR. Skipping persona update.")
        return
    
    with open(stakeholders_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse insights: PERSON: [Name]\nINSIGHT: [Text]
    blocks = re.findall(r"---?\nPERSON: (.*?)\nINSIGHT: (.*?)\n---?", insights, re.DOTALL)
    if not blocks:
        print("No valid insight blocks parsed.")
        return

    updated_names = []
    for person, insight in blocks:
        person = person.strip()
        insight = insight.strip()
        # Find the person's section in stakeholders.md (matches ### Name)
        pattern = rf"(### {re.escape(person)}.*?\n)(.*?)(\n\n|###|$|---)"
        
        def replace_func(match):
            header = match.group(1)
            body = match.group(2)
            footer = match.group(3)
            if "(최근 업데이트 대기 중...)" in body:
                body = body.replace("(최근 업데이트 대기 중...)", "").strip()
            
            # Avoid duplicate insights if already present
            if insight[:50] in body: # Simple check for first 50 chars
                return match.group(0)
                
            new_body = f"{body}\n{insight}".strip()
            return f"{header}{new_body}\n{footer}"
        
        new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            updated_names.append(person)
    
    if updated_names:
        with open(stakeholders_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated stakeholder insights for: {updated_names}")

def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image(file_path):
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Analyzing image: {file_path.name}...")
    
    base64_image = encode_image(file_path)
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Get list of existing topics for smarter matching
    existing_topics = [f.stem for f in FLEETING_DIR.rglob("*.md")] + \
                      [f.stem for f in LIT_DIR.rglob("*.md")] + \
                      [f.stem for f in PERM_DIR.rglob("*.md")]
    
    # Smart Topic Matching
    match_prompt = f"""
당신은 지식 분류 전문가입니다. 제공된 이미지를 보고, 아래의 기존 주제 목록 중 가장 적합한 것을 골라주세요.
만약 적합한 주제가 없다면, 새로운 1~3단어의 간결한 주제명을 한국어로 제안하세요.

[기존 주제 목록]
{", ".join(existing_topics[:100])} 

응답 형식: 
TOPIC: [결정된 주제명]
"""
    match_res = generate_with_ollama(match_prompt, images=[base64_image])
    match_res = match_res if match_res else ""
    topic_match = re.search(r"TOPIC:\s*(.*)", match_res)
    topic = topic_match.group(1).strip() if topic_match else "Image_Note"
    topic = "".join(c for c in topic if c.isalnum() or c in ('_', '-'))

    # Check if a note with this topic already exists
    existing_content = ""
    target_path = None
    for d in SEARCH_DIRS:
        for f in d.rglob(f"{topic}.md"):
            target_path = f
            with open(target_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            break
        if target_path: break
    
    vision_prompt = f"""
당신은 시각 지능을 갖춘 **금융 및 지식 관리 전문가**입니다. 
제공된 이미지를 분석하여 다음 항목에 따라 **한국어**로 답변하세요:

1. **상세 요약**: 이미지에 무엇이 담겨 있는지 상세히 설명하세요.
2. **핵심 데이터 추출 (OCR)**: 
   - **주의**: '전일 대비 등락(전일비)'와 '사용자 실제 수익률'을 엄격히 구분하세요.
   - 화살표(▲, ▼)와 함께 표시된 백분율(%)은 오늘 하루 동안의 변동인 **전일비**입니다.
   - 사용자님의 실제 **평가 손익(금액)**과 **보유 수익률**을 정확히 찾아내어 정리하세요.
3. **핵심 인사이트 및 시사점 (Implications)**: 
   - 오늘 주가가 하락했더라도 사용자님이 수익 구간인지(저점 매수 여부)를 분석하세요.
   - 포트폴리오의 리스크와 기회 요인을 분석하세요.
4. **시계열 비교 (Comparison)**: 
   [기존 내용 시작]
   {existing_content if existing_content else "기존 기록이 없습니다."}
   [기존 내용 끝]
   
   이전 기록과 현재 상태를 비교하여 수익금의 변화나 포트폴리오의 개선 여부를 분석하세요.
5. **최종 주제명**: [{topic}] (이 주제명을 유지하거나 더 적합하게 수정하세요)

출력 형식:
TOPIC: [주제명]
DESCRIPTION: [요약 내용]
IMPLICATIONS: [인사이트]
COMPARISON: [비교 분석 결과]
TEXT: [추출된 텍스트]
"""
    
    response = generate_with_ollama(vision_prompt, images=[base64_image])
    
    if not response or "TOPIC:" not in response:
        print(f"Failed to analyze image {file_path.name}.")
        return
    
    topic_match = re.search(r"TOPIC:\s*(.*)", response)
    desc_match = re.search(r"DESCRIPTION:\s*(.*)", response, re.DOTALL)
    impl_match = re.search(r"IMPLICATIONS:\s*(.*)", response, re.DOTALL)
    comp_match = re.search(r"COMPARISON:\s*(.*)", response, re.DOTALL)
    text_match = re.search(r"TEXT:\s*(.*)", response, re.DOTALL)
    
    topic = topic_match.group(1).strip() if topic_match else topic
    topic = "".join(c for c in topic if c.isalnum() or c in ('_', '-'))
    
    if existing_content:
        # Merge Logic
        print(f"Merging image analysis into existing note: {topic}.md")
        new_entry = f"""
---
### 📅 {today} 업데이트
![[{file_path.name}]]

#### 👁️ 분석 요약
{desc_match.group(1).strip() if desc_match else ""}

#### 💡 인사이트 및 비교
{comp_match.group(1).strip() if comp_match else ""}
{impl_match.group(1).strip() if impl_match else ""}

#### 📝 데이터 (OCR)
```text
{text_match.group(1).strip() if text_match else ""}
```
"""
        final_content = existing_content.strip() + "\n\n" + new_entry.strip()
    else:
        # New Note Logic
        print(f"Creating new image note: {topic}.md")
        final_content = f"""# {topic}
📅 최초 생성: {today}

![[{file_path.name}]]

## 👁️ AI 분석 및 요약
{desc_match.group(1).strip() if desc_match else ""}

## 💡 핵심 인사이트 (Implications)
{impl_match.group(1).strip() if impl_match else ""}

## 📝 텍스트 추출 (OCR)
```text
{text_match.group(1).strip() if text_match else ""}
```

#Tags
#Image #OCR #Insight #Comparison #Automated
"""
        # Determine Category
        category_res = generate_with_ollama(get_category_prompt(response if response else topic))
        category = category_res.strip() if category_res else "Other"
        category = "".join(c for c in category if c.isalnum())
        
        target_dir = FLEETING_DIR / category
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / f"{topic}.md"
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Saved image analysis to: {target_path}")
    
    # Determine attachment category based on the note's final location
    note_category = target_path.parent.name
    cat_attachments_dir = VAULT_DIR / "50_Resources" / note_category / "Attachments"
    cat_attachments_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(cat_attachments_dir / file_path.name))

def process_document(file_path):
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Analyzing document: {file_path.name}...")
    
    ext = file_path.suffix.lower()
    content_summary = ""
    
    try:
        if ext == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages[:10]: # Limit to first 10 pages
                    text += page.extract_text() + "\n"
                content_summary = f"PDF Content (First 10 pages):\n{text}"
        elif ext in [".csv", ".xlsx", ".xls"]:
            if ext == ".csv":
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            summary = df.describe(include='all').to_string()
            head = df.head(10).to_string()
            content_summary = f"Spreadsheet Data Summary:\n{summary}\n\nFirst 10 Rows:\n{head}"
    except Exception as e:
        print(f"Error reading document {file_path.name}: {e}")
        return

    if not content_summary:
        return

    # Use LLM to get topic and summary
    prompt = f"""
당신은 지능형 문서 분석 비서입니다. 아래 문서의 내용을 분석하여 **한국어**로 요약해 주세요.
주제명을 1~3단어로 제안하고, 주요 내용을 3-5가지 포인트로 요약하세요.

[문서 내용]
{content_summary[:5000]}

출력 형식:
TOPIC: [주제명]
SUMMARY: [요약 내용]
"""
    response = generate_with_ollama(prompt)
    if not response or "TOPIC:" not in response:
        return
        
    topic_match = re.search(r"TOPIC:\s*(.*)", response)
    summary_match = re.search(r"SUMMARY:\s*(.*)", response, re.DOTALL)
    
    topic = topic_match.group(1).strip() if topic_match else "Document_Note"
    topic = "".join(c for c in topic if c.isalnum() or c in ('_', '-'))
    
    # Create Markdown Note
    note_content = f"""# {topic}
📅 분석 일시: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
파일 링크: [[{file_path.name}]]

## 📄 문서 분석 요약
{summary_match.group(1).strip() if summary_match else "요약을 생성하지 못했습니다."}

## 📊 데이터 추출 원본 (일부)
```text
{content_summary[:2000]}
```

#Tags
#Document #Analysis #Automated
"""
    # Determine Category
    category_res = generate_with_ollama(get_category_prompt(note_content))
    category = category_res.strip() if category_res else "Other"
    category = "".join(c for c in category if c.isalnum())
    
    target_dir = FLEETING_DIR / category
    target_dir.mkdir(parents=True, exist_ok=True)

    note_path = target_dir / f"{topic}.md"
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)
        
    print(f"Created document note in {category}: {note_path.name}")
    
    # Move original to Categorized Attachments
    cat_attachments_dir = VAULT_DIR / "50_Resources" / category / "Attachments"
    cat_attachments_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(cat_attachments_dir / file_path.name))

def process_inbox():
    if not INBOX_DIR.exists():
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for d in SEARCH_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    # Process Markdown files
    for file_path in INBOX_DIR.glob("*.md"):
        print(f"Processing: {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
            
        # 0. Enrich with Web Info if URLs present
        new_content = enrich_content_with_urls(original_content)
        
        # 1. Extract Topic
        existing = get_existing_topics()
        prompt = get_topic_prompt(existing)
        topic = generate_with_ollama(prompt, new_content)
        if not topic:
            print("Failed to extract topic. Skipping.")
            continue
            
        if topic.strip().upper() == "REJECT":
            print(f"Content lacks meaning. Rejecting {file_path.name}.")
            shutil.move(str(file_path), str(ARCHIVE_DIR / f"REJECTED_{file_path.name}"))
            continue
            
        topic_filename = f"{topic.strip()}.md"
        # Sanitize filename
        topic_filename = "".join(c for c in topic_filename if c.isalnum() or c in ('_', '-', '.'))
        
        # 2. Check if topic exists in any folder
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
            # Determine Category
            category_res = generate_with_ollama(get_category_prompt(new_content))
            category = category_res.strip() if category_res else "Other"
            category = "".join(c for c in category if c.isalnum())
            
            target_dir = FLEETING_DIR / category
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_path = target_dir / topic_filename
            final_content = generate_with_ollama(get_summary_prompt(), new_content)
            
        # 3. Save Output
        if final_content:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Saved processed file to: {target_path}")
            
            # Move the original file to Archive
            shutil.move(str(file_path), str(ARCHIVE_DIR / file_path.name))
            print(f"Moved original to Archive: {file_path.name}")
            
            # 4. Extract Stakeholder Insights (Persona Update)
            print("Checking for stakeholder insights...")
            insights = generate_with_ollama(get_stakeholder_prompt(), new_content)
            if insights and insights.strip() != "NONE":
                update_stakeholders_file(insights)

        else:
            print(f"Failed to process: {file_path.name}")

    # Process Image files
    for file_path in INBOX_DIR.iterdir():
        if file_path.suffix.lower() in IMAGE_EXTENSIONS:
            process_image(file_path)
        elif file_path.suffix.lower() in {'.pdf', '.csv', '.xlsx', '.xls'}:
            process_document(file_path)

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
