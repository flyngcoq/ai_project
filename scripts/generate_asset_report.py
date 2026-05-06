import os
import datetime
import re
from pathlib import Path
from core.config import VAULT_DIR, FLEETING_DIR, PERM_DIR, LIT_DIR
from core.llm_client import generate_with_ollama

def generate_asset_report():
    print("🚀 통합 자산 보고서 생성을 시작합니다...")
    
    # 1. 관련 노트 찾기
    search_dirs = [FLEETING_DIR, PERM_DIR, LIT_DIR]
    stock_notes = []
    for d in search_dirs:
        for f in d.glob("*.md"):
            # 파일명에 '주식' 또는 '포트폴리오'가 포함된 경우
            if any(kw in f.name for kw in ["주식", "포트폴리오", "Stock", "Portfolio"]):
                stock_notes.append(f)
    
    if not stock_notes:
        print("분석할 주식 관련 노트를 찾지 못했습니다.")
        return

    # 2. 데이터 취합
    aggregated_data = ""
    for note_path in stock_notes:
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 가장 최근의 업데이트 섹션 추출 (보통 마지막에 있음)
            # 여기서는 파일 전체를 컨텍스트로 제공하여 AI가 판단하게 함
            aggregated_data += f"\n--- 문서: {note_path.name} ---\n{content}\n"

    # 3. 스타일 가이드 및 규칙 로드
    style_guide_path = VAULT_DIR / "99_System_Prompts" / "Summary_Style_Guide.md"
    style_guide = ""
    if style_guide_path.exists():
        with open(style_guide_path, 'r', encoding='utf-8') as f:
            style_guide = f.read()

    # 4. AI 분석 요청
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    analysis_prompt = f"""
당신은 개인 자산 관리 전문가(CFA)입니다. 
아래의 주식 포트폴리오 데이터와 분석 규칙을 준수하여 **통합 자산 관리 주간 보고서**를 작성해 주세요.

[작성 규칙 및 스타일 가이드]
{style_guide}

[포트폴리오 데이터]
{aggregated_data}

보고서 포함 항목 (한국어로 작성):
1. **전체 포트폴리오 요약**: 모든 포트폴리오를 통합한 전체 수익률 및 평가 금액.
2. **주요 변동 사항**: 지난 기록 대비 변화 및 전일 대비 등락과 수익률의 관계 분석.
3. **리스크 진단**: 섹터 집중도 및 변동성 분석.
4. **차주 투자 전략 추천**: 구체적인 액션 아이템.

출력은 깔끔한 마크다운 형식으로 해주세요.
"""
    
    report_content = generate_with_ollama(analysis_prompt)
    
    if report_content:
        # 4. 저장
        report_dir = VAULT_DIR / "40_Projects"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"Weekly_Asset_Report_{today}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 📊 통합 자산 관리 주간 보고서 ({today})\n\n")
            f.write(report_content)
            
        print(f"✅ 보고서 생성 완료: {report_path}")
        return report_path
    else:
        print("❌ 보고서 생성 실패.")
        return None

if __name__ == "__main__":
    generate_asset_report()
