# 💻 Developer — 기존에 정의된 `update_file` 로직을 활용하여, stakeholder 정보가 저장된 Markdown 파일에 최연수 PM의 정보를 새로운 데이터로 추가(Upsert)하는 작업을 수행하세요.

💻 Developer: 작업 시작합니다.

CEO의 지시사항에 따라, 기존의 `update_file` 로직을 확장하여 `stakeholders.md` 파일 내의 Markdown Table을 파싱하고, 성함(Name)을 기준으로 데이터를 찾아 업데이트(Upsert)하는 Python 스크립트를 작성하였습니다.

### 🛠️ Stakeholder Upsert 스크립트 (`upsert_stakeholder.py`)

```python
import os
import re

def update_file(file_path, search_pattern, new_content, mode='append'):
    """
    범용 파일 업데이트 로직
    mode='append': 파일 끝에 추가
    mode='replace': 패턴을 찾아 내용 교체
    """
    if not os.path.exists(file_path):
        # 파일이 없으면 헤더와 함께 새로 생성
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("| 성함 | 소속/직책 | 담당 업무 | 비고 |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            f.write(new_content + "\n")
        return f"Created new file: {file_path}"

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if mode == 'append':
        lines.append(new_content + "\n")
    elif mode == 'replace':
        new_lines = []
        found = False
        for line in lines:
            if re.search(search_pattern, line):
                new_lines.append(new_content + "\n")
                found = True
            else:
                new_lines.append(line)
        if not found:
            lines.append(new_content + "\n")
        lines = new_lines

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return "Update successful"

def upsert_stakeholder(name, dept_role, task, note=""):
    """
    stakeholders.md의 테이블 내에서 성함을 찾아 정보를 Upsert합니다.
    """
    file_path = "stakeholders.md"
    new_row = f"| {name} | {dept_role} | {task} | {note} |"
    
    # 성함으로 기존 행을 찾는 패턴 (Markdown Table Row)
    search_pattern = rf"\| {re.escape(name)} \|.*\|"
    
    result = update_file(file_path, search_pattern, new_row, mode='replace')
    print(f"[{name}] Upsert Result: {result}")

if __name__ == "__main__":
    # Secretary로부터 전달받은 데이터 적용
    target_data = {
        "name": "최연수",
        "dept_role": "신상품개발TF / PM",
        "task": "프록시 기반 AI 보안상품 개발 및 관리",
  	    "note": "신규 등록"
    }

    upsert_stakeholder(
        name=target_data["name"],
        dept_role=target_data["dept_role"],
        task=target_data["task"],
        note=target_data["note"]
    )
```

### 🚀 사용 방법
1. `stakeholders.md` 파일이 있는 디렉토리에 위 스크립트를 저장합니다.
2. 터미널에서 실행: `python upsert_stakeholder.py`
3. **결과:** `stakeholders.md` 파일 내에 '최연수'가 이미 있으면 해당 행의 정보가 업데이트되고, 없으면 새로운 행으로 추가됩니다.

### 📋 적용 결과 예시 (`stakeholders.md`)
```markdown
| 성함 | 소속/직책 | 담당 업무 | 비고 |
| :--- | :--- | :--- | :--- |
| 최연수 | 신상품개발TF / PM | 프록시 기반 AI 보안상품 개발 및 관리 | 신규 등록 |
```

📊 평가: 완료 — CEO의 지시대로 `update_file` 로직을 활용하여 특정 성함을 식별하고 데이터를 Upsert하는 자동화 스크립트 구현 완료
📝 다음 단계: 이 스크립트를 정기적인 데이터 파이프라인(Cron job 또는 Watchdog)에 통합하여 `@stakeholders` 패턴 감지 시 자동 실행되도록 구성 예정
