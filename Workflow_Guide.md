# AI 업무 자동화 및 산출물 활용 플로우 (Workflow Guide)

이 문서는 로컬 LLM(Ollama)과 자동화 스크립트를 통해 정리된 데이터가 어떻게 팀의 최종 보고서(Confluence/Jira)로 도달하는지, 그 전체적인 흐름과 구체적인 활용 방법을 설명합니다.

## 📊 업무 플로우 구성도 (Workflow Flowchart)

```mermaid
graph TD
    %% 1단계: 데이터 수집
    subgraph Data Input "1. 데이터 수집 (Raw Data)"
        A1[웹 스크랩/기사] -->|저장| B(Obsidian 00_Inbox)
        A2[회의록 초안] -->|작성| B
        A3[아이디어 메모] -->|모바일 동기화| B
    end

    %% 2단계: AI 자동화
    subgraph AI Processing "2. AI 자동화 처리 (Ollama + Python)"
        B -->|process_markdowns.py 실행| C{Ollama API}
        C -->|텍스트 요약 & 태깅| D1[10_Fleeting_Notes]
        C -->|구조화된 정보| D2[20_Literature_Notes]
    end

    %% 3단계: 일간/주간 취합
    subgraph Compilation "3. 리포트 생성 (Routine Automator)"
        D1 -->|스케줄러 취합| E[routine_automator.py 실행]
        D2 -->|스케줄러 취합| E
        E -->|일간/주간 템플릿 적용| F(40_Projects/Daily_Logs)
    end

    %% 4단계: 최종 산출물 활용
    subgraph Output Usage "4. 최종 산출물 활용 (Confluence / Jira)"
        F -->|Confluence_Report_Prompt 적용| G(Jira/Confluence용 마크다운 표)
        G -->|복사/붙여넣기| H[Confluence 위키 게시]
        G -->|복사/붙여넣기| I[Jira 티켓 코멘트 작성]
    end
    
    classDef highlight fill:#f9f,stroke:#333,stroke-width:2px;
    class C highlight;
```

---

## 💡 산출물 활용 가이드 (How to Use)

자동화된 환경에서 나온 결과물을 팀 보고용으로 활용하는 방법은 다음과 같습니다.

### Step 1. 데이터 수집 (의식의 흐름대로 작성)
* 일하는 도중 떠오르는 아이디어나 회의 내용, 중요한 웹 기사 등을 모두 `00_Inbox` 폴더 안에 마크다운(.md) 파일로 던져둡니다.
* 모바일 기기에서도 동일하게 생각날 때마다 Inbox에 적고 동기화(`sync.sh` 또는 Git) 시킵니다.

### Step 2. 파이프라인 가동 (자동 정제)
* 터미널에서 파이썬 스크립트(`python scripts/process_markdowns.py`)를 실행합니다.
* (현재 구동 중이신 `gemma4:26b-a4b-it-q4_K_M` 모델이 동작하여) Inbox의 두서없는 글들을 읽고 **핵심 3줄 요약, 태그 추가, 가독성 높은 구조**로 변환한 뒤 `10_Fleeting_Notes`로 이동시킵니다.

### Step 3. 일일/주간 리포트 자동 생성
* 스케줄러(`python scripts/routine_automator.py`)에 의해 자동으로 `40_Projects/Daily_Logs` 폴더에 오늘/이번 주의 통합 노트가 만들어집니다.
* 이곳에 정제된 메모들이 차곡차곡 쌓여 있게 됩니다.

### Step 4. Confluence / Jira 보고용 변환 (최종 복사)
* 데일리 로그나 정제된 메모를 보고서로 변환하고 싶을 때, Obsidian 내에서 작성해둔 **[Confluence_Report_Prompt.md](../99_System_Prompts/Confluence_Report_Prompt.md)** 를 활용합니다.
* Text Generator 플러그인 등에서 해당 프롬프트를 불러온 뒤 취합된 내용을 넣으면, AI가 즉시 **Jira/Confluence에 붙여넣기 완벽한 상태의 표(Table)와 이모지 리스트**로 출력해 줍니다.
* 출력된 마크다운 결과물을 그대로 Confluence의 마크다운 삽입 매크로(`{markdown}`) 또는 Jira 텍스트 입력창에 붙여넣기만 하면 팀 보고가 완료됩니다.
