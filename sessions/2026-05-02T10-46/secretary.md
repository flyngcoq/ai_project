# 📱 Secretary — 새롭게 정의된 '@stakeholders' 명령어 사용법과 업데이트된 워크플로우를 회사 운영 가이드(Workflow Guide) 및 업무 매뉴얼에 기록하십시오.

📱 Secretary: 작업 시작합니다.

CEO의 지시사항에 따라, `@stakeholders` 명령어 사용법과 자동화 워크플로우를 반영한 **[Workflow Guide 업데이트 초안]**을 작성하였습니다. 이 내용을 기존 `Workflow_Guide.md`에 즉시 병합하여 사용하시기 바랍니다.

---

# 🚀 [Update] 이해관계자(Stakeholder) 관리 자동화 가이드

이 가이드는 팀 내 주요 이해관계자 정보를 `@stakeholders` 명령어를 통해 실시간으로 수집하고, `stakeholders.md` 파일에 자동 기록하는 프로세스를 설명합니다.

## 1. 🛠️ 자동화 워크플로우 (Automation Workflow)

사용자가 텍스트(대화록 또는 업무 로그)에 특정 패턴을 입력하면, 시스템이 이를 감지하여 데이터베이스를 업데이트합니다.

1.  **입력 (Input):** 사용자가 `@stakeholders Name: [이름], Role: [역할], ...` 형태의 명령어를 입력합니다.
2.  **감지 및 파싱 (Parsing):** `stakeholder_updater.py` 스크립트가 정규표현식을 사용하여 `Key: Value` 쌍을 추출합니다.
3.  **데이터 처리 (Upsert):** 
    *   기존에 동일한 `Name`이 존재할 경우: 해당 행의 데이터를 최신 정보로 **업데이트(Update)** 합니다.
    *   존재하지 않는 `Name`일 경우: 테이블의 새로운 행으로 **추가(Insert)** 합니다.
4.  **저장 (Storage):** 최종 결과물은 `stakeholders.md` 파일 내 Markdown Table 형식으로 저장됩니다.

## 2. ⌨️ 명령어 사용법 (Command Syntax)

명령어는 반드시 `@stakeholders`로 시작해야 하며, 각 항목은 `Key: Value` 형태를 유지하고 쉼표(`,`)로 구분합니다.

**[기본 문법]**
`@stakeholders Name: [이름], Role: [역할], Influence: [High|Medium|Low], Interest: [High|Medium|Low], Type: [Internal|External], Contact: [채널], Key_Need: [내용]`

**[입력 예시]**
> `@stakeholders Name: 김철수, Role: 개발팀장, Influence: High, Interest: High, Type: Internal, Contact: Slack, Key_new: 일정 준수`

## 3. 📊 데이터 스키마 (Data Schema)

`stakeholders.md`에 기록되는 표준 필드 정의입니다.

| 필드명 (Key) | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **Name** | String | 이해관계자 성명 (Primary Key) |
| **Role** | String | 조직 내 역할 및 직책 |
| **Influence** | Enum | 의사결정 영향력 (High, Medium, Low) |
| **Interest** | Enum | 프로젝트 관심도 (High, Medium, Low) |
| **Type** | Enum | 유형 (Internal: 내부, External: 외부) |
| **Contact** | String | 커뮤니케이션 채널 (Slack, Email 등) |
| **Key_Need** | String | 핵심 요구사항 및 관리 포인트 |
| **Last_Update** | Date | 데이터가 마지막으로 수정된 날짜 (자동 기록) |

## 4. 📋 운영 규칙 (Operating Rules)

1.  **즉시성:** 새로운 이해관계자가 프로젝트에 참여하거나 역할이 변경될 경우, 발견 즉시 `@stakeholders` 명령어를 실행합니다.
2.  **데이터 정합성:** `Influence`와 `Interest`가 모두 **High**인 인원은 'Key Stakeholder'로 분류하여 집중 관리합니다.
3.  **정기 검토:** `Last_Update` 날짜를 확인하여, 3개월 이상 경과된 데이터는 정기적인 정보 갱신(Monthly Review)을 수행합니다.

---

📊 평가: 완료 — 지시된 명령어 사용법과 워크플로우를 가이드 형식으로 구조화하여 작성 완료함.
📝 다음 단계: 위 내용을 `Workflow_Guide.md`에 반영하고, `stakeholders.md` 파일의 초기 헤더 생성 여부 확인.
