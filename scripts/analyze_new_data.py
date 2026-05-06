import os
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
UPLOADED_NOTES = PROJECT_ROOT / "30_Permanent_Notes"
VAULT_WORK_DIR = PROJECT_ROOT / "Obsidian_Vault" / "40_Projects" / "Work" / "Safe_AI"
REPORT_PATH = PROJECT_ROOT / "Obsidian_Vault" / "40_Projects" / "Work" / "New_Data_Analysis_Report.md"

def analyze_and_move():
    if not UPLOADED_NOTES.exists():
        print("업로드된 30_Permanent_Notes 폴더를 찾을 수 없습니다.")
        return

    VAULT_WORK_DIR.mkdir(parents=True, exist_ok=True)
    
    analysis_log = []
    analysis_log.append("# 🚀 신규 데이터(Safe_AI) 분석 및 동기화 리포트\n")
    analysis_log.append("## 📁 1. 데이터 마이그레이션 현황\n")
    analysis_log.append("깃허브 루트 경로에 업로드된 대규모 프로젝트 데이터를 옵시디언 금고 내 `Work/Safe_AI` 프로젝트 폴더로 안전하게 이관했습니다.\n")
    
    categories = {}
    
    for root, _, files in os.walk(UPLOADED_NOTES):
        for file in files:
            if file == ".DS_Store": continue
            
            src_path = Path(root) / file
            rel_path = src_path.relative_to(UPLOADED_NOTES)
            
            # Categories based on top-level folder
            category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Uncategorized"
            if category not in categories:
                categories[category] = []
            categories[category].append(file)
            
            # Destination path
            dest_path = VAULT_WORK_DIR / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(src_path), str(dest_path))
    
    # Cleanup empty directory
    shutil.rmtree(UPLOADED_NOTES, ignore_errors=True)
    
    # Generate Report Content
    analysis_log.append("## 📊 2. 프로젝트 아키텍처 요약 (Category Breakdown)\n")
    for cat, files in categories.items():
        analysis_log.append(f"### 📂 {cat} ({len(files)}개 파일)")
        for f in files[:5]:
            analysis_log.append(f"- {f}")
        if len(files) > 5:
            analysis_log.append(f"- ... 및 {len(files)-5}개 파일 더 있음")
        analysis_log.append("\n")

    analysis_log.append("## 🤖 3. 에이전트별 후속 조치 제안 (CEO Agent)\n")
    analysis_log.append("- **[@developer]**: `src/` 폴더 내의 `auth.py`, `main.py` 등의 소스 코드를 리뷰하고, 현재 텔레그램 봇 시스템과 연동 가능한 부분이 있는지 아키텍처 분석 요망.\n")
    analysis_log.append("- **[@researcher]**: `04_경쟁력_및_차별화/` 내의 경쟁사 분석 및 신기술(동형암호) 관련 문서를 요약하여 CEO에게 브리핑할 것.\n")
    analysis_log.append("- **[@business]**: `03_세일즈_및_제안/` 폴더의 투자심의서 및 수익성 분석 자료를 바탕으로, 해당 프로젝트의 예상 ROI 시뮬레이션 요망.\n")
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(analysis_log))
        
    print(f"✅ 마이그레이션 완료! 종합 보고서 생성됨: {REPORT_PATH}")

if __name__ == "__main__":
    analyze_and_move()
