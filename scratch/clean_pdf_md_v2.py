import re

def clean_pdf_md(content):
    # 1. Basic cleaning
    content = content.replace("데이 터", "데이터")
    content = content.replace("악의 적인", "악의적인")
    content = content.replace("애플리케이 션", "애플리케이션")
    content = content.replace("파이프 라인", "파이프라인")
    content = content.replace("화이 트리스트", "화이트리스트")
    content = content.replace("이 루어지고", "이루어지고")
    content = content.replace("라 이브러리", "라이브러리")
    content = content.replace("프레임 워크", "프레임워크")
    content = content.replace("취약 점", "취약점")
    
    # 2. Fix broken line breaks
    lines = content.splitlines()
    cleaned_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            cleaned_lines.append("")
            i += 1
            continue
        
        # Merge lines if it's a split sentence
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line and not any(line.endswith(p) for p in ['.', '!', '?', ':', '>', '#', '-', '*', '➊', '➋', '➌']):
                if re.search(r'[가-힣]$', line) and re.match(r'^[가-힣]', next_line):
                    line = line + " " + next_line
                    i += 1
        cleaned_lines.append(line)
        i += 1
    
    content = "\n".join(cleaned_lines)
    
    # 3. Premium polish for the RAG section (Targeted replacement)
    rag_target = r"#### 3.4.6 LLM 출력결과를 정기적으로 모니터링하고 검토하고 있는가\?.*?무결성을 확보"
    rag_replacement = """#### 3.4.6 LLM 출력결과를 정기적으로 모니터링하고 검토하고 있는가?

- LLM 출력에 대해서는 정기적으로 **자기 일관성(Self Consistency on prompt)** 투표 기술을 사용하여 일관되지 않은 텍스트를 필터링함. 단일 프롬프트에 대한 여러 모델 응답을 비교하면 출력의 품질과 일관성을 더 잘 판단할 수 있음.

**[예시] LLM 출력결과 모니터링 시 확인사항**
- **출력 데이터 수집 및 로그 기록**
    1. **출력 데이터 로깅**: 모든 요청과 응답 데이터를 로그로 기록 (요청, 응답, 사용자 ID, 타임스탬프 등 메타데이터 포함)
    2. **로그 저장소 관리**: 로그 데이터를 암호화하여 저장. 전문 로그 관리 도구(Splunk, ELK Stack 등) 활용 권장
- **이상 탐지 및 자동화**
    1. **이상 출력 탐지**: AI 기반 이상 탐지 도구를 활용하여 비정상적인 패턴 탐지
    2. **규칙 기반 필터링**: 특정 키워드나 패턴에 대한 규칙 기반 점검 수행
    3. **실시간 알림**: 비정상 출력이 감지될 경우 즉시 담당자에게 알림을 전송하는 시스템 구축

#### 3.4.8 LLM의 벡터 및 임베딩 취약점에 대한 방어 방안을 수립하고 있는가?

- **RAG(Retrieval Augmented Generation)** 및 임베딩 기반 시스템은 정보 검색의 정확성을 높이기 위해 필수적이나, 공격자가 유해 콘텐츠 삽입이나 민감 정보 노출을 위해 악용할 수 있음.
- **RAG의 정의**: 사전 학습된 언어 모델과 외부 지식 소스를 결합하여 LLM 애플리케이션의 성능과 응답의 맥락 관련성을 향상시키는 모델 적응 기술.

**“벡터 및 임베딩 취약점”에 대한 예방책**

| 방어 기법 | 세부 내용 |
| :--- | :--- |
| **권한 및 접근 제어** | 세분화된 접근 제어 및 권한 관리가 가능한 벡터 및 임베딩 저장소를 구현 |
| **데이터 검증 및 출처 인증** | 강력한 데이터 검증 파이프라인을 구현하여 신뢰할 수 있고, 검증된 소스의 데이터만 허용 |
| **데이터 결합 및 분류 검토** | 서로 다른 소스의 데이터를 결합할 때, 결합된 데이터셋을 철저히 검토. 지식 데이터베이스 내 데이터를 태그하고 분류하여 접근 수준을 제어하고 데이터 불일치 오류를 방지 |
| **모니터링 및 로깅** | 의심스러운 동작을 신속히 탐지하고 대응하기 위해, 검색 활동에 대한 세부적인 불변 로그(immutable log)를 유지하여 기록의 무결성을 확보 |"""
    
    # Use re.DOTALL to match across lines
    content = re.sub(rag_target, rag_replacement, content, flags=re.DOTALL)
    
    return content

if __name__ == "__main__":
    file_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/인공지능_AI_보안_안내서-2.md"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Reset file to a cleaner state (optional, but good for testing)
    cleaned = clean_pdf_md(content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print("Full file cleanup and premium RAG section polish complete.")
