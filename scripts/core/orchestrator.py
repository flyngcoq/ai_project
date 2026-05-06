import re
from pathlib import Path
from scripts.core.llm_client import generate_with_ollama
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
AGENTS_ROOT = PROJECT_ROOT / "_agents"

def orchestrate_agents(user_text, context_data=""):
    """
    Autonomous multi-agent orchestration logic.
    1. CEO plans
    2. Sub-agents execute
    3. CEO synthesizes
    """
    # 1. Load Available Agents
    available_agents = [d.name for d in AGENTS_ROOT.iterdir() if d.is_dir()]
    
    # 2. CEO Planning
    planning_prompt = f"""당신은 최고 경영자(CEO)입니다. 사용자의 다음 요청을 해결하기 위해 어떤 전문 에이전트들의 도움이 필요한지 판단하세요.
사용 가능한 에이전트 목록: {", ".join(available_agents)}

[사용자 요청]
{user_text}

[규칙]
1. 도움이 필요한 에이전트의 이름을 쉼표로 구분하여 답변하세요. (예: developer, researcher)
2. 만약 본인(CEO) 선에서 즉시 답변 가능하다면 'NONE'이라고 답변하세요.
3. 오직 에이전트 이름들 또는 'NONE'만 출력하세요.
"""
    plan_res = generate_with_ollama(planning_prompt, "어떤 에이전트가 필요합니까?")
    needed_agents = [a.strip().lower() for a in plan_res.split(",") if a.strip().lower() in available_agents]
    
    agent_reports = []
    if needed_agents and "none" not in plan_res.lower():
        for agent in needed_agents:
            # Load agent persona
            a_dir = AGENTS_ROOT / agent
            a_prompt = ""
            if (a_dir / "prompt.md").exists():
                with open(a_dir / "prompt.md", "r", encoding="utf-8") as f:
                    a_prompt = f.read()
            
            a_system = f"당신은 {agent.upper()} 전문가입니다.\n{a_prompt}\n\n[미션]\nCEO의 지시에 따라 다음 요청에 대해 전문적인 의견이나 결과물을 제출하세요."
            report = generate_with_ollama(a_system, user_text)
            if report:
                agent_reports.append(f"[{agent.upper()} 보고서]\n{report}")

    # 3. CEO Synthesis & Tool Execution
    from scripts.core.google_gas_client import list_calendar_events, add_calendar_event, list_unread_emails
    
    synthesis_prompt = f"""당신은 CEO입니다. 하급 에이전트들의 보고서와 사용 가능한 도구를 활용하여 최종 답변을 제공하세요.

[사용 가능한 도구 (Tool Tags)]
1. 구글 캘린더 조회: [CALENDAR_LIST] 라고 출력하면 향후 7일간의 일정을 가져옵니다.
2. 구글 캘린더 등록: [CALENDAR_ADD: 제목, 시작시간, 종료시간] (예: [CALENDAR_ADD: 미팅, 2026-05-06T15:00:00, 2026-05-06T16:00:00])
3. Gmail 조회: [GMAIL_LIST] 라고 출력하면 읽지 않은 메일 5건을 가져옵니다.

[에이전트 보고서 내역]
{chr(10).join(agent_reports) if agent_reports else "추가 보고서 없음 (CEO 직접 판단)"}

[참고 문서 컨텍스트]
{context_data if context_data else "관련 문서 없음"}

[사용자 요청]
{user_text}

[지침]
1. 도구가 필요하다면 도구 태그만 포함된 메시지를 먼저 보내세요. (예: "일정을 확인하겠습니다. [CALENDAR_LIST]")
2. 이미 도구 결과가 아래에 있다면, 그 결과를 포함하여 최종 답변을 작성하세요.
3. 한국어로 답변하세요.
"""
    # First Synthesis Call
    response = generate_with_ollama(synthesis_prompt, "응답을 생성하세요.")
    
    # Tool Execution Loop
    tool_results = []
    if "[CALENDAR_LIST]" in response:
        tool_results.append(f"[캘린더 내역]\n{json.dumps(list_calendar_events(), indent=2, ensure_ascii=False)}")
    if "[GMAIL_LIST]" in response:
        tool_results.append(f"[메일 내역]\n{json.dumps(list_unread_emails(), indent=2, ensure_ascii=False)}")
    # (Simplified CALENDAR_ADD logic for now)
    add_match = re.search(r"\[CALENDAR_ADD:\s*(.*?),\s*(.*?),\s*(.*?)\]", response)
    if add_match:
        res = add_calendar_event(add_match.group(1), add_match.group(2), add_match.group(3))
        tool_results.append(f"[캘린더 등록 결과]\n{res}")

    if tool_results:
        # Second Synthesis Call with Tool Data
        final_prompt = synthesis_prompt + "\n\n[도구 실행 결과]\n" + "\n".join(tool_results)
        final_reply = generate_with_ollama(final_prompt, "도구 결과를 포함하여 최종 답변을 작성하세요.")
    else:
        final_reply = response
    
    # 4. Async Memory Update (Self-Reflection)
    update_agent_memories(user_text, final_reply, needed_agents)
    
    return final_reply

def update_agent_memories(user_text, final_reply, involved_agents):
    """
    CEO reviews the interaction and updates the long-term memory of involved agents.
    """
    if not involved_agents:
        involved_agents = ["ceo"]
    elif "ceo" not in involved_agents:
        involved_agents.append("ceo")
        
    for agent in involved_agents:
        m_path = AGENTS_ROOT / agent / "memory.md"
        if not m_path.exists(): continue
        
        with open(m_path, 'r', encoding='utf-8') as f:
            current_memory = f.read()
            
        reflection_prompt = f"""당신은 {agent.upper()} 에이전트의 성장을 돕는 감사관입니다. 
다음 대화 내용을 보고, 이 에이전트가 앞으로 꼭 기억해야 할 '새로운 사실', '사용자의 취향', 또는 '업무 노하우'가 있다면 요약하여 제출하세요.

[기존 메모리]
{current_memory}

[최근 대화]
사용자: {user_text}
최종 답변: {final_reply}

[지침]
1. 기존 메모리와 중복되는 내용은 제외하세요.
2. 에이전트의 발전에 도움이 될 핵심 포인트만 1~3개 내외로 간결하게 정리하세요.
3. 한국어로 답변하세요.
4. 만약 업데이트할 내용이 없다면 'SKIP'이라고 답변하세요.
"""
        new_insights = generate_with_ollama(reflection_prompt, "메모리 업데이트 사항을 추출하세요.")
        
        if new_insights and "SKIP" not in new_insights.upper():
            updated_memory = current_memory.strip() + f"\n\n### 📝 추가 학습 ({datetime.datetime.now().strftime('%Y-%m-%d')})\n" + new_insights.strip()
            with open(m_path, 'w', encoding='utf-8') as f:
                f.write(updated_memory)
            print(f"Updated memory for {agent}.")

import datetime
