# AI-Driven Workflow: Setup Guide

이 문서는 개인화된 AI 지식 관리 및 자동화 파이프라인을 구축하기 위한 초기 설정 가이드입니다. 환경을 새로 구축하거나 다른 기기에서 세팅할 때 참고하세요.

## 1. 지식 베이스 구축 (Obsidian)

마크다운(Markdown) 기반의 지식 관리를 위해 Obsidian을 사용하며, 다중 기기(Mac, Windows, iOS, Android) 동기화를 위해 Github을 활용합니다.

### 폴더 구조
`/Users/flyngcoq/AI_Project/Obsidian_Vault/` 디렉토리 아래에 다음과 같은 구조를 생성했습니다.
* `00_Inbox`: 새로운 메모, 스크랩, 수집된 원시 데이터가 처음 저장되는 곳.
* `10_Fleeting_Notes`: 임시 메모.
* `20_Literature_Notes`: 읽은 책, 아티클, 영상 등의 요약 노트.
* `30_Permanent_Notes`: 정제되고 연결된 나만의 지식 노트 (Zettelkasten).
* `40_Projects`: 현재 진행 중인 프로젝트 관련 문서.
* `50_Resources`: 참고 자료, 이미지, PDF 등.
* `90_Templates`: 반복해서 사용하는 문서의 템플릿.
* `99_System_Prompts`: 로컬 LLM 및 에이전트에 주입할 시스템 프롬프트 모음.

### Github 동기화 세팅
1. Vault 폴더 내에서 `git init`을 실행합니다.
2. 로컬 상태 파일들이 동기화되지 않도록 `.gitignore` 파일을 작성합니다.
   * 제외 대상: `.DS_Store`, `.obsidian/workspace.json`, `.obsidian/workspace-mobile.json`, `.obsidian/graph.json` 등
3. `sync.sh` 스크립트를 사용하여 커밋과 푸시를 자동화합니다.
4. **모바일 기기 동기화**: 
   * iOS: `Working Copy` 앱을 통해 Clone 후 Obsidian 폴더로 마운트.
   * Android: `GitJournal` 또는 `Termux`를 활용하여 Clone.

## 2. 로컬 LLM 구축 (Ollama) - 진행 예정

맥북 환경에서 가장 속도가 빠르고 Python/API 연동이 용이한 **Ollama**를 메인 엔진으로 사용합니다.

* 설치: `brew install ollama` 또는 공식 홈페이지에서 다운로드.
* 추천 모델: Llama 3 (다국어/영어 중심) 또는 qwen (한국어 특화).
* 연동: 향후 작성될 Python 스크립트에서 Ollama API (http://localhost:11434) 를 호출하여 마크다운 문서를 처리합니다.

---
*(이 문서는 프로젝트가 진행됨에 따라 지속적으로 업데이트 됩니다.)*
