import os
import json
import base64
import urllib.request
import urllib.parse
from datetime import datetime

# ==========================================
# 1. 환경 변수 및 인증 설정 (.env 활용)
# ==========================================
env_vars = {}
env_path = r'C:\AG_Project\jira confl\.env'
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip()
except FileNotFoundError:
    print(f"Error: {env_path} 파일을 찾을 수 없습니다.")
    exit(1)

domain = env_vars.get('ATLASSIAN_DOMAIN', 'lgucorp.atlassian.net').rstrip('/')
email = env_vars.get('ATLASSIAN_EMAIL')
api_token = env_vars.get('ATLASSIAN_API_TOKEN')
project_key = env_vars.get('PROJECT_KEY', 'SAFEAI')
space_key = env_vars.get('SPACE_KEY', 'NewProdTF')
parent_page_id = env_vars.get('PARENT_PAGE_ID', '1240706693')

auth_str = f"{email}:{api_token}"
b64_auth = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
headers = {
    'Authorization': f'Basic {b64_auth}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# ==========================================
# 2. 마크다운 회의록 파일 읽기
# ==========================================
md_path = r'c:\AG_Project\Safe AI MVP\01_기획_및_목표\8. 화이트보드_논의사항_정리.md'
try:
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
except FileNotFoundError:
    print(f"Error: {md_path} 파일을 찾을 수 없습니다.")
    exit(1)

# Confluence 요건에 맞게 간단한 HTML로 변환 (완벽한 파서는 아니지만 기본 형태 유지)
# Confluence REST API는 Storage format (XHTML) 을 요구함
html_body = f"""
<h1>화이트보드 회의록: Pilot 단계 및 아키텍처 고도화 전략</h1>
<ac:structured-macro ac:name="info"><ac:rich-text-body>
본 문서는 오프라인 화이트보드 회의 결과를 디지털화하여 기록한 문서입니다.
</ac:rich-text-body></ac:structured-macro>
<pre>{md_content}</pre>
"""

# ==========================================
# 3. Confluence 페이지 생성
# ==========================================
today = datetime.now().strftime("%Y-%m-%d")
confluence_title = f"[YS_AI] 화이트보드 아키텍처/Pilot 논의 회의록 {today}"

conf_payload = {
    "title": confluence_title,
    "type": "page",
    "space": {"key": space_key},
    "body": {
        "storage": {
            "value": html_body,
            "representation": "storage"
        }
    }
}
if parent_page_id:
    conf_payload["ancestors"] = [{"id": parent_page_id}]

def make_request(url, method, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTPError for {url}: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
        raise e

print("Creating Confluence page...")
conf_url = f"https://{domain}/wiki/rest/api/content"
conf_page_link = ""
try:
    conf_res = make_request(conf_url, 'POST', conf_payload)
    conf_page_link = conf_res['_links']['base'] + conf_res['_links']['webui']
    print(f"✅ Confluence Page Created: {conf_page_link}")
except Exception as e:
    print(f"Failed to create confluence page: {e}")

# ==========================================
# 4. Jira 이슈(Action Items) 생성
# ==========================================
actions = [
    {
        "summary": "1개사 Phase 1 Pilot 맞춤형(Custom) 연동 및 SLA 검증",
        "desc": "목표 타겟 맞춤형 구현 진행 및 통신, 보안 요건 테스트"
    },
    {
        "summary": "멀티테넌트(N개사) 수용 아키텍처 도입 검토",
        "desc": "다중 고객사 확장을 고려하여 Safe AI 멀티테넌시 구조 설계"
    },
    {
        "summary": "MCP/A2A 기반 AI 트래픽 라우팅 방안 기획",
        "desc": "기존 Proxy 통신 외에 에이전트 간 통신(A2A) 및 도구 호출(MCP) 보호를 위한 라우팅 통제 전략 수립"
    },
    {
        "summary": "[시스템 고도화] 단일 파이프라인/단일 시스템 통합 아키텍처 수립",
        "desc": "파편화된 기존 시스템(프롬프트 기반 등)을 Skill / Tool 기반의 단일 솔루션으로 묶어내기 위한 개발 방향 협의"
    }
]

print("\nCreating Jira Issues...")
jira_url = f"https://{domain}/rest/api/3/issue"
issue_links = []

for action in actions:
    jira_summary = f"[YS_AI] Action Item: {action['summary']}"
    
    adf_desc = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": f"상세 내용: {action['desc']}"},
                    {"type": "hardBreak"},
                    {"type": "hardBreak"},
                    {"type": "text", "text": "참고 회의록: "},
                    {"type": "text", "text": conf_page_link if conf_page_link else "링크 생성 실패", 
                     "marks": [{"type": "link", "attrs": {"href": conf_page_link}}] if conf_page_link else []}
                ]
            }
        ]
    }
    
    jira_payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": jira_summary,
            "issuetype": {"name": "Task"},  # Jira 설정에 따라 '작업', 'Task' 등 확인 필요
            "description": adf_desc
        }
    }
    
    try:
        res = make_request(jira_url, 'POST', jira_payload)
        link = f"https://{domain}/browse/{res['key']}"
        issue_links.append(link)
        print(f"✅ Created Jira Issue: {res['key']}")
    except urllib.error.HTTPError as e:
        # Task 타입 실패 시 '작업' 으로 재시도
        # print("Task 타입 생성 실패. '작업' 타입으로 재시도합니다...")
        jira_payload["fields"]["issuetype"]["name"] = "작업"
        try:
            res = make_request(jira_url, 'POST', jira_payload)
            link = f"https://{domain}/browse/{res['key']}"
            issue_links.append(link)
            print(f"✅ Created Jira Issue: {res['key']}")
        except Exception as ex:
             print(f"Failed to create Jira issue: {ex}")

print("\n=== 최종 업로드 완료 요약 ===")
print(f"Confluence Link: {conf_page_link}")
for link in issue_links:
    print(f"Jira Task: {link}")
