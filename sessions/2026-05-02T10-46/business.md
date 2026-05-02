# 💰 Business — stakeholders.md 파일에 포함될 필수 데이터 스키마(예: 이름, 역할, 영향력, 이해관계 유형, 연락처 등)와 관리 기준을 정의하십시오.

💰 Business: Stakeholder Management Framework 및 데이터 스키마 정의합니다.

이 작업은 팀의 의사결정 영향력을 파악하고, 프로젝트 리스크를 관리하기 위한 핵심 자산(Asset) 구축 작업입니다. `@stakeholders` 명령어를 통한 자동화를 고려하여, 파싱(Parsing)이 용이한 구조로 설계했습니다.

---

### 1. `stakeholders.md` 데이터 스키마 (Schema)

자동화 로직이 데이터를 정확히 분류할 수 있도록 **Markdown Table** 형식을 표준으로 채택합니다.

| 필드명 (Key) | 설명 (Description) | 데이터 타입/예시 | 비고 |
| :--- | :--- | :--- | :--- |
| **Name** | 이해관계자 성명 | String (홍길동) | 식별자 |
| **Role** | 조직 내 역할 및 직책 | String (PM, 개발자, 팀장) | |
| **Influence** | 의사결정 영향력 | Enum (High, Medium, Low) | P0(핵심) 결정권자 판별 |
| **Interest** | 프로젝트 관심도 | Enum (High, Medium, Low) | 리스크 관리 우선순위 |
| **Type** | 이해관계자 유형 | Enum (Internal, External) | 팀 내부 vs 타 부서/고객 |
| **Contact** | 연락처/커뮤니케이션 채널 | String (Slack, Email) | |
| **Key_Need** | 핵심 요구사항/니즈 | String (예: 비용 절감, 일정 준수) | 관리 포인트 |
| **Last_Update** | 최종 데이터 수정일 | Date (YYYY-MM-DD) | 데이터 신뢰도 확인 |

---

### 2. 관리 기준 (Management Standards)

데이터의 휘발성을 방지하고 'Single Source of Truth'를 유지하기 위한 운영 규칙입니다.

1.  **업데이트 트리거 (Update Trigger):**
    *   새로운 이해관계자 합류 또는 조직 개편 발생 시 즉시 업데이트.
    *   `@stakeholders [데이터]` 명령어를 통해 실시간 반영.
2.  **데이터 정합성 (Data Integrity):**
    *   `Influence`와 `Interest`가 모두 **High**인 인원은 'Key Stakeholder'로 별도 관리 (Critical Path).
    *   `Last_Update`가 3개월 이상 경과한 항목은 정기 리뷰(Monthly Review) 대상.
3.  **권한 및 책임 (R&R):**
    *   **작성/수정:** Business 에이전트 및 지정된 프로젝트 관리자.
    *   **검토:** CEO (또는 팀 리더).

---

### 3. 자동화 로직 설계: `@stakeholders` 명령어 규격

명령어 입력 시 파싱 엔진이 `stakeholders.md`의 테이블에 새로운 행(Row)을 추가하거나 기존 행을 업데이트하는 로직입니다.

**[명령어 문법 (Syntax)]**
`@stakeholders [Name] | [Role] | [Influence] | [Interest] | [Type] | [Contact] | [Key_Need]`

**[작동 프로세스]**
1.  **Input Scan:** 사용자가 `@stakeholders`로 시작하는 문자열을 입력함.
2.  **Parsing:** `|` (Pipe) 구분자를 기준으로 각 필드값을 추출.
3.  **Search & Match:** `stakeholders.md` 내에 동일한 `Name`이 존재하는지 확인.
    *   **Exists (Update):** 해당 Name의 행을 찾아 나머지 필드값을 최신 데이터로 덮어씀 (Last_Update는 자동 갱신).
    *   **Not Exists (Insert):** 새로운 행을 테이블 맨 아래에 추가.
4.  **Validation:** 필수 필드(Name, Role, Influence) 누락 시 에러 메시지 출력 및 반영 거부.

**[적용 예시]**
> **User Input:** `@stakeholders 김철수 | CTO | High | High | Internal | Slack | 기술적 타당성 검토`
>
> **Result (`stakeholders.md` 반영):**
> | Name | Role | Influence | Interest | Type | Contact | Key_Need | Last_Update |
> | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
> | 김철수 | CTO | High | High | Internal | Slack | 기술적 타당성 검토 | 2026-05-22 |

---

📊 평가: 완료 — 데이터 스키마, 관리 기준, 자동화 로직 규격을 모두 정의함
📝 다음 단계: 개발 에이전트에게 `@stakeholders` 파싱 및 업데이트 스크립트 구현 요청
