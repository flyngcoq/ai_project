# Ollama 연동 및 활용 가이드

이 문서는 맥북 환경에서 로컬 LLM인 Ollama를 설치하고, Obsidian 및 파이썬 자동화 스크립트와 연동하는 방법을 정리한 가이드입니다.

## 1. Ollama 설치 및 기본 모델 다운로드

맥북(Apple Silicon 지원)에서 가장 빠르고 설정이 간편한 Ollama를 사용합니다.

1. **설치**:
   터미널을 열고 Homebrew를 이용해 설치합니다.
   ```bash
   brew install ollama
   ```
   또는 [Ollama 공식 홈페이지](https://ollama.com)에서 Mac 버전을 다운로드하여 설치할 수 있습니다.

2. **모델 다운로드 및 실행**:
   한국어 처리에 준수한 성능을 보이거나 빠르고 가벼운 모델을 다운로드합니다.
   ```bash
   # 기본적으로 빠르고 범용적인 Llama 3
   ollama run llama3
   
   # 한국어에 특화된 모델이 필요하다면 (예: qwen 등)
   ollama run qwen:7b
   ```

3. **백그라운드 실행 확인**:
   Ollama 앱을 켜두면, 기본적으로 `http://localhost:11434` 주소로 API 서버가 동작합니다.

## 2. Obsidian과 직접 연동 (플러그인)

Obsidian 내에서 문서를 작성하면서 바로 AI의 도움을 받기 위한 설정입니다.

1. **추천 플러그인 설치**:
   Obsidian의 `Community plugins` 탭에서 다음 플러그인 중 하나를 설치합니다.
   * **Text Generator**: 문서 생성 및 템플릿 기반 프롬프팅에 특화
   * **BMO Chatbot**: 채팅 UI 형태로 질문하고 답변을 문서에 바로 삽입할 때 유용
   * **Smart Connections**: 노트 간의 유사도를 분석하고 대화할 때 유용

2. **플러그인 설정 (Text Generator 예시)**:
   * Text Generator 설정으로 이동합니다.
   * **LLM Provider**를 `Ollama` 또는 `Custom API (OpenAI 호환)`로 선택합니다.
   * **Base URL**에 `http://localhost:11434/v1` (OpenAI 호환 API 사용 시) 또는 `http://localhost:11434` 를 입력합니다.
   * **Model** 이름에 다운로드한 모델명 (예: `llama3`)을 정확히 입력합니다.

## 3. 파이썬 자동화 스크립트 연동

수백 개의 방대한 마크다운 문서를 일괄로 정리할 때 파이썬 스크립트를 사용합니다. (`/scripts/process_markdowns.py` 참고)

1. Python의 내장 라이브러리 `urllib`이나 `requests` 패키지를 사용하여 로컬 API(`http://localhost:11434/api/generate`)로 HTTP POST 요청을 보냅니다.
2. 스크립트 내의 `SYSTEM_PROMPT`를 수정하여, 문서 요약, 태그 추출, 목차 생성 등 원하는 형태로 데이터 가공을 자동화할 수 있습니다.
