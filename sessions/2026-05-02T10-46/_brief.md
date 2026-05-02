# 📋 작업 브리프

**원 명령:** 우리회사는 실은 회사 내의 하나의 팀이야... stakeholders를 정의하는 md파일을 만들고... @stakeholders라고 입력하면 해당 md파일을 업데이트하는 로직을 만들자...

## 요약
Stakeholder 관리를 위한 전용 Markdown 파일을 생성하고, '@stakeholders' 명령어를 통해 해당 파일을 자동으로 업데이트하는 자동화 로직을 구축합니다.

## 분배
- **💰 Business**: stakeholders.md 파일에 포함될 필수 데이터 스키마(예: 이름, 역할, 영향력, 이해관계 유형, 연락처 등)와 관리 기준을 정의하십시오.
- **💻 Developer**: 입력 텍스트에서 '@stakeholders' 패턴을 감지하고, 뒤에 오는 내용을 파싱하여 stakeholders.md 파일에 구조화된 데이터(YAML 또는 Markdown Table)로 추가/업데이트하는 Python 스크립트 또는 자동화 로직을 설계 및 구현하십시오.
- **📱 Secretary**: 새롭게 정의된 '@stakeholders' 명령어 사용법과 업데이트된 워크플로우를 회사 운영 가이드(Workflow Guide) 및 업무 매뉴얼에 기록하십시오.
