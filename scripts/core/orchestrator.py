import re
import threading
import datetime
import json
from pathlib import Path
from core.llm_client import generate_with_ollama, stream_with_ollama

PROJECT_ROOT = Path(__file__).parent.parent.parent
AGENTS_ROOT = PROJECT_ROOT / "_agents"

def orchestrate_agents(user_text, context_data="", history=None):
    """
    Simplified orchestration for non-streaming calls.
    """
    gen = stream_orchestrate(user_text, context_data, history)
    full_text = ""
    for chunk in gen:
        full_text += chunk
    return full_text

def stream_orchestrate(user_text, context_data="", history=None):
    """
    Simplified & Streaming Orchestration with History support.
    """
    # 1. Quick Complexity Check
    is_complex = len(user_text) > 40 or any(kw in user_text for kw in ["보고서", "분석", "개발", "정리", "검색", "기획"])
    
    needed_agents = []
    agent_reports = []
    
    # Format history for prompt
    history_text = ""
    if history:
        history_text = "\n[최근 대화 내역]\n" + "\n".join([f"{m['role']}: {m['content']}" for m in history])

    if is_complex:
        available_agents = [d.name for d in AGENTS_ROOT.iterdir() if d.is_dir()]
        planning_prompt = f"""당신은 최고 경영자(CEO)입니다. 다음 요청을 해결하기 위해 전문 에이전트들의 도움이 필요한지 판단하세요.
사용 가능한 에이전트: {", ".join(available_agents)}
{history_text}
사용자 요청: {user_text}
[규칙]
1. 필요한 에이전트 이름만 쉼표로 구분하거나, 직접 답변 가능하면 'NONE'이라고만 하세요.
"""
        plan_res = generate_with_ollama(planning_prompt, "Planning...")
        if plan_res and "NONE" not in plan_res.upper():
            needed_agents = [a.strip().lower() for a in plan_res.split(",") if a.strip().lower() in available_agents]
            for agent in needed_agents:
                a_dir = AGENTS_ROOT / agent
                a_prompt = ""
                if (a_dir / "prompt.md").exists():
                    with open(a_dir / "prompt.md", "r", encoding="utf-8") as f:
                        a_prompt = f.read()
                a_system = f"당신은 {agent.upper()} 전문가입니다.\n{a_prompt}\n\n[최근 대화]\n{history_text}\n\n[미션] 다음 요청에 대해 전문적인 의견을 제출하세요."
                report = generate_with_ollama(a_system, user_text)
                if report:
                    agent_reports.append(f"[{agent.upper()} 보고서]\n{report}")

    # 2. Synthesis (Streaming)
    from core.google_gas_client import list_calendar_events, add_calendar_event, list_unread_emails
    from core.web_search_client import web_search
    
    synthesis_prompt = f"""당신은 Antigravity의 CEO이며, 로컬 모델 Gemma(젬마)입니다.
사용자는 당신을 '@gemma' 또는 '@젬마'로 호출할 수 있습니다.
모든 답변의 맨 첫 줄은 반드시 "**gemma의 답변**"으로 시작해야 합니다.
대화 내역과 참고 자료를 활용해 답변하세요.
{history_text}

[에이전트 보고서]
{chr(10).join(agent_reports) if agent_reports else "CEO 직접 판단"}

[참고 문서 컨텍스트]
{context_data if context_data else "없음"}

[사용자 요청]
{user_text}

[도구 사용 가이드 (중요)]
- 실시간 정보나 외부 지식이 필요하면 반드시 [WEB_SEARCH: 검색어] 태그를 답변에 포함하세요.
- 일정 확인이 필요하면 답변에 [CALENDAR_LIST] 태그를 포함하세요.
- 메일 확인이 필요하면 답변에 [GMAIL_LIST] 태그를 포함하세요.

한국어로 자연스럽게 답변하세요.
"""
    
    response_buffer = ""
    for chunk in stream_with_ollama(synthesis_prompt, "응답 생성 중..."):
        response_buffer += chunk
        yield chunk

    # 3. Tool Execution
    from core.google_gas_client import list_calendar_events, add_calendar_event, list_unread_emails
    tool_results = []
    
    # Check for Web Search
    search_match = re.search(r"\[WEB_SEARCH:\s*(.*?)\]", response_buffer)
    if search_match:
        query = search_match.group(1)
        yield f"\n\n🔍 **웹에서 '{query}' 검색 중...**\n"
        search_results = web_search(query)
        tool_results.append(f"[웹 검색 결과]\n{search_results}")

    if "[CALENDAR_LIST]" in response_buffer:
        tool_results.append(f"[캘린더 내역]\n{json.dumps(list_calendar_events(), indent=2, ensure_ascii=False)}")
    if "[GMAIL_LIST]" in response_buffer:
        tool_results.append(f"[메일 내역]\n{json.dumps(list_unread_emails(), indent=2, ensure_ascii=False)}")
    
    if tool_results:
        final_prompt = synthesis_prompt + "\n\n[도구 실행 결과]\n" + "\n".join(tool_results)
        yield "\n\n--- 🌐 웹 검색 및 도구 데이터 기반 최종 답변 ---\n\n"
        for chunk in stream_with_ollama(final_prompt, "최종 정리 중..."):
            response_buffer += chunk
            yield chunk

    # 4. Asynchronous Memory Update
    if response_buffer:
        threading.Thread(target=update_agent_memories, args=(user_text, response_buffer, needed_agents)).start()

def update_agent_memories(user_text, final_reply, involved_agents):
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
다음 대화에서 꼭 기억해야 할 새로운 사실이나 사용자 취향을 1~2줄로 요약하세요. 
내용이 없으면 'SKIP'이라고만 하세요.
사용자: {user_text}
최종 답변: {final_reply}
"""
        new_insights = generate_with_ollama(reflection_prompt, "Insight Extraction")
        if new_insights and "SKIP" not in new_insights.upper():
            updated_memory = current_memory.strip() + f"\n\n### 📝 추가 학습 ({datetime.datetime.now().strftime('%Y-%m-%d')})\n" + new_insights.strip()
            with open(m_path, 'w', encoding='utf-8') as f:
                f.write(updated_memory)
