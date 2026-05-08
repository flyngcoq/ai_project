import re

def clean_pdf_md(content):
    # 1. Fix common word breaks in Korean (e.g., "데이 터" -> "데이터")
    # This is tricky because some spaces are legitimate. 
    # We focus on common patterns found in the sample.
    patterns = [
        (r'데이 터', '데이터'),
        (r'악의 적인', '악의적인'),
        (r'애플리케이 션', '애플리케이션'),
        (r'파이프 라인', '파이프라인'),
        (r'화이 트리스트', '화이트리스트'),
        (r'명령 어', '명령어'),
        (r'취약 점', '취약점'),
        (r'알림 시스템', '알림 시스템'),
        (r'로깅', '로깅'),
        (r'모니터링', '모니터링'),
    ]
    
    for p, r in patterns:
        content = re.sub(p, r, content)

    # 2. Fix broken line breaks (lines ending with Korean character followed by newline and another Korean character)
    # This often happens when a sentence is split across pages.
    # We look for lines that end with a character but not a terminal punctuation (. ? !)
    # and join them with the next line if it starts with a lowercase or continuing character.
    
    lines = content.splitlines()
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            cleaned_lines.append("")
            i += 1
            continue
            
        # If line doesn't end with punctuation and next line exists and is not empty
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line and not any(line.endswith(p) for p in ['.', '!', '?', ':', '>', '#', '-', '*', '➊', '➋', '➌']):
                # Check if it looks like a split sentence (e.g., line ends with Korean char)
                if re.search(r'[가-힣]$', line) and re.match(r'^[가-힣]', next_line):
                    line = line + " " + next_line
                    i += 1 # skip next line
        
        cleaned_lines.append(line)
        i += 1
        
    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    file_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/인공지능_AI_보안_안내서-2.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    cleaned = clean_pdf_md(content)
    
    # Also fix tables manually for the specific sample section if possible
    # (Simplified regex for this task)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print("Cleanup complete.")
