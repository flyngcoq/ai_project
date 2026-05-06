from core.config import VAULT_DIR

def retrieve_context(query: str) -> str:
    stopwords = {"이", "그", "저", "것", "수", "등", "및", "을", "를", "이", "가", "은", "는", "에", "대해", "알려줘", "뭐야", "어때", "어떻게", "해줘", "의", "도"}
    words = [w for w in query.split() if w not in stopwords and len(w) > 1]
    if not words:
        return ""
        
    scores = {}
    for filepath in VAULT_DIR.rglob("*.md"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                score = sum(content.count(w) for w in words)
                if score > 0:
                    scores[filepath] = (score, content)
        except Exception:
            continue
            
    if not scores:
        return ""
        
    top_files = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:2]
    
    context_str = "다음은 사용자의 작업 공간(Obsidian_Vault)에서 발췌한 관련 문서 내용입니다:\n\n"
    for filepath, (score, content) in top_files:
        trunc_content = content[:1500] + "..." if len(content) > 1500 else content
        context_str += f"--- 문서: {filepath.name} ---\n{trunc_content}\n\n"
        
    return context_str
