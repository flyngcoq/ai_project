import sys
from pathlib import Path
import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from core.llm_client import generate_with_ollama

PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_ROOT = PROJECT_ROOT / "_agents"
REPORTS_DIR = PROJECT_ROOT / "40_Projects" / "Work"

def run_weekly_audit():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"Agent_Weekly_Audit_{today}.md"
    
    audit_results = []
    
    print("🚀 CEO 주간 성과 감사 및 프롬프트 최적화를 시작합니다...")
    
    # Get all agents
    agents = [d.name for d in AGENTS_ROOT.iterdir() if d.is_dir() and d.name != "ceo"]
    
    for agent in agents:
        print(f"🧐 [{agent.upper()}] 감사 중...")
        a_dir = AGENTS_ROOT / agent
        
        # Load current state
        files = {
            "prompt": a_dir / "prompt.md",
            "memory": a_dir / "memory.md",
            "goal": a_dir / "goal.md"
        }
        
        data = {}
        for key, path in files.items():
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data[key] = f.read()
            else:
                data[key] = f"{key} 정보 없음"

        # CEO Audit Prompt
        audit_prompt = f"""당신은 최고 경영자(CEO)입니다. [{agent.upper()}] 에이전트의 한 주간 성과와 학습 내용을 바탕으로 감사를 진행하세요.

[현재 프롬프트]
{data['prompt']}

[최근 메모리 (학습 내용)]
{data['memory']}

[설정된 목표]
{data['goal']}

[미션]
1. 에이전트가 한 주 동안 학습한 내용 중 '프롬프트'에 고정적으로 반영해야 할 핵심 지침을 추출하세요.
2. 현재 프롬프트의 문제점이나 개선 방향을 제안하세요.
3. 에이전트의 목표 달성률을 평가하세요 (0~100%).
4. **최종적으로 업데이트된 프롬프트 내용 전체**를 작성하세요.

응답 형식:
AUDIT_SUMMARY: [성과 요약 및 평가]
GOAL_PROGRESS: [달성률 %]
IMPROVED_PROMPT: [여기에 수정된 프롬프트 내용 전체 작성]
"""
        audit_res = generate_with_ollama(audit_prompt, "주간 감사를 실시하세요.")
        
        if audit_res:
            import re
            summary = re.search(r"AUDIT_SUMMARY:\s*(.*)", audit_res, re.DOTALL)
            progress = re.search(r"GOAL_PROGRESS:\s*(.*)", audit_res)
            new_prompt = re.search(r"IMPROVED_PROMPT:\s*(.*)", audit_res, re.DOTALL)
            
            if new_prompt:
                # Update the prompt file
                with open(files['prompt'], 'w', encoding='utf-8') as f:
                    f.write(new_prompt.group(1).strip())
                print(f"✅ [{agent.upper()}] 프롬프트 최적화 완료.")
            
            audit_results.append(f"""### 🤖 {agent.upper()} (진행률: {progress.group(1).strip() if progress else "N/A"})
**성과 요약**: 
{summary.group(1).strip() if summary else "요약 실패"}

**주요 변경 사항**:
- 프롬프트에 새로운 학습 내용 반영 완료.
""")

    # Generate Master Audit Report
    report_content = f"""# 🧭 에이전트 주간 성과 감사 보고서 ({today})
📅 작성자: CEO 에이전트

본 보고서는 한 주간의 에이전트별 대화 히스토리와 메모리를 바탕으로 성과를 평가하고, 각 에이전트의 페르소나를 최적화한 결과입니다.

---

## 📊 에이전트별 감사 결과

{chr(10).join(audit_results)}

---

## 💡 CEO 총평 및 향후 전략
- 모든 에이전트가 사용자님의 'Work/Wealth' 이원화 체계에 잘 적응하고 있음.
- 향후 더욱 능동적인 자산 분석 및 업무 제안이 가능하도록 프롬프트 고도화를 지속할 예정.

#Audit #Weekly #Agent #Optimization #CEO
"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"🎉 주간 감사 보고서가 생성되었습니다: {report_path.name}")

if __name__ == "__main__":
    run_weekly_audit()
