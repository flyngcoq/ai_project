import re

def clean_pdf_md_v3(content):
    # 1. Fix common word breaks in Korean (Remove single spaces between Korean characters)
    # We only do this if it looks like a single word split by a space.
    # Pattern: [Korean][Space][Korean] -> [Korean][Korean]
    # But we don't want to merge "나는 학교에" -> "나는학교에".
    # So we focus on 3+ syllable blocks that are often split.
    
    def fix_korean_spaces(text):
        # Specific known broken words from the user's example and others
        broken_words = {
            '이 루어진': '이루어진',
            '데이터': '데이터', # Already handled but for consistency
            '악의 적': '악의적',
            '애플리케이 션': '애플리케이션',
            '파이프 라인': '파이프라인',
            '화이 트리스트': '화이트리스트',
            '이 루어지고': '이루어지고',
            '라 이브러리': '라이브러리',
            '프레임 워크': '프레임워크',
            '취약 점': '취약점',
            '학 습': '학습',
            '이 상치': '이상치',
            '의 도': '의도',
            '애플리케이 션': '애플리케이션'
        }
        for b, r in broken_words.items():
            text = text.replace(b, r)
        return text

    content = fix_korean_spaces(content)

    # 2. Fix split headings (Heading title split across lines)
    lines = content.splitlines()
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if current line is a heading
        heading_match = re.match(r'^(#{1,6})\s*(.*)', line)
        if heading_match:
            level = heading_match.group(1)
            title = heading_match.group(2)
            
            # Look BACK at the previous non-empty line
            if len(cleaned_lines) > 0:
                prev_idx = len(cleaned_lines) - 1
                while prev_idx >= 0 and not cleaned_lines[prev_idx].strip():
                    prev_idx -= 1
                
                if prev_idx >= 0:
                    prev_line = cleaned_lines[prev_idx].strip()
                    # If prev_line doesn't end with punctuation and isn't a heading/bullet
                    if prev_line and not any(prev_line.endswith(p) for p in ['.', '!', '?', ':', '>', '#', '-', '*']):
                        # Merge prev_line into current heading
                        new_title = prev_line + " " + title
                        cleaned_lines[prev_idx] = "" # Clear the previous line
                        line = f"{level} {new_title}"
        
        cleaned_lines.append(line)
        i += 1

    # Final pass to fix any remaining spacing issues and clean up empty lines
    result = "\n".join(cleaned_lines)
    # Remove excessive newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result

if __name__ == "__main__":
    file_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/인공지능_AI_보안_안내서-2.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    cleaned = clean_pdf_md_v3(content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print("V3 Cleanup complete.")
