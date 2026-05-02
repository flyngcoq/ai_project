# 💻 Developer — 입력 텍스트에서 '@stakeholders' 패턴을 감지하고, 뒤에 오는 내용을 파싱하여 stakeholders.md 파일에 구조화된 데이터(YAML 또는 Markdown Table)로 추가/업데이트하는 Python 스크립트 또는 자동화 로직을 설계 및 구현하십시오.

💻 Developer: 작업 시작합니다.

CEO의 지시사항에 따라 `@stakeholders` 패턴을 감지하여 `stakeholders.md`를 자동으로 업데이트하는 Python 스크립트를 구현했습니다. 이 스크립트는 정규표현식을 사용하여 `Key: Value` 패턴을 추출하며, 기존 데이터가 있으면 업데이트(Upsert), 없으면 신규 추가합니다.

### 1. `stakeholder_updater.py` 구현

```python
import re
import os
from datetime import datetime

class StakeholderUpdater:
    def __init__(self, file_path="stakeholders.md"):
        self.file_path = file_path
        self.headers = ["Name", "Role", "Influence", "Interest", "Type", "Contact", "Key_Need", "Last_Update"]
        self.header_line = "| " + " | ".join(self.headers) + " |"
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """파일이 없으면 헤더와 구분선을 포함하여 생성합니다."""
        if not os.path.exists(self.file_path):
            separator = "| " + " | ".join([":---"] * len(self.headers)) + " |"
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write("# Stakeholders List\n\n")
                f.write(self.header_line + "\n")
                f.write(separator + "\n")

    def parse_command(self, text):
        """@stakeholders 뒤의 텍스트에서 Key: Value 쌍을 추출합니다."""
        pattern = r"@stakeholders\s*(.*)"
        match = re.search(pattern, text)
        if not match:
            return None

        content = match.group(1)
        # Key: Value 형태 추출 (예: Name: 홍길동, Role: PM)
        kv_pairs = re.findall(r"(\w+):\s*([^,]+)", content)
        data_dict = {k.strip(): v.strip() for k, v in kv_pairs}
        
        if not data_dict:
            return None
            
        data_dict["Last_Update"] = datetime.now().strftime("%Y-%m-%d")
        return data_dict

    def update_file(self, new_data):
        """Markdown Table을 읽어 데이터를 Upsert 합니다."""
        with open(self.file_path, "s", encoding="utf-8") as f:
            lines = f.readlines()

        # 테이블 시작 지점 찾기
        table_start_idx = -1
        for i, line in enumerate(lines):
            if self.header_line in line:
                table_start_idx = i
                break
        
        if table_start_idx == -1:
            return False

        # 기존 테이블 데이터 파싱 (Header와 Separator 제외)
        rows = []
        for i in range(table_start_idx + 2, len(lines)):
            line = lines[i].strip()
            if not line or line.startswith("#"): break
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= len(self.headers):
                row_dict = dict(zip(self.headers, parts))
                rows.append(row_dict)

        # Upsert 로직: Name 기준
        name_to_find = new_data.get("Name")
        updated_rows = [r for r in rows if r.get("Name") != name_to_find]
        
        # 새로운 데이터 채우기 (누락된 필드는 N/A)
        full_row = {h: new_data.get(h, "N/A") for h in self.headers}
        updated_rows.append(full_row)

        # 파일 재작성
        new_table_content = [self.header_line, "| " + " | ".join([":---"] * len(self.headers)) + " |"]
        for r in updated_rows:
            new_table
