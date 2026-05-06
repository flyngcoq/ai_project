from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.auth import verify_tenant_api_key
from src.inspection import run_exaone_semantic_firewall
import httpx
import logging

# ==========================================
# 1. 초기 셋업 및 환경변수
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("safeai-proxy")

app = FastAPI(title="Safe AI MVP Proxy Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 고객사 도메인으로 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LG EXAONE 및 써드파티 통신 타임아웃
HTTPX_TIMEOUT = 5.0

# ==========================================
# 2. 라우팅: OpenAI Drop-in Replacement
# ==========================================
@app.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_to_llm(path: str, request: Request, tenant_info: dict = Depends(verify_tenant_api_key)):
    """
    고객사의 OpenAI 표준 트래픽을 가로채서 백엔드 LLM으로 쏴주는 역방향 프록시 핵심 뼈대
    """
    logger.info(f"Traffic via Tenant: {tenant_info['tenant_id']} | Path: /v1/{path}")
    
    # 1. 여기서 멀티모달 & EXAONE Semantic Filter 모듈(비동기) 호출 구역 
    try:
        body_json = await request.json()
        is_safe, masked_body_json = await run_exaone_semantic_firewall(body_json, tenant_info) 
        if not is_safe:
            raise HTTPException(status_code=403, detail="DLP or Semantic rule violation detected (e.g., Core Tech / .py file upload blocked).")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Inspection Engine Failure: {e}")
        # Fail-closed 정책 적용
        raise HTTPException(status_code=403, detail="Blocked: Safety Inspection Engine timed out or failed.")
    
    # 2. 외부 LLM(OpenAI/Claude) 서버로 전달
    target_url = f"https://api.openai.com/v1/{path}"
    
    headers = dict(request.headers)
    # Host 헤더 변조 방지 및 Content-Length 재계산(마스킹으로 길이 변경됨)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    # 마스킹된 바디 사용 (import json 필요)
    import json
    new_body = json.dumps(masked_body_json).encode("utf-8")
    
    async with httpx.AsyncClient(timeout=HTTPX_TIMEOUT) as client:
        try:
            proxy_req = client.build_request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=new_body
            )
            proxy_res = await client.send(proxy_req)
            return JSONResponse(
                content=proxy_res.json(),
                status_code=proxy_res.status_code
            )
        except httpx.RequestError as e:
            logger.error(f"Proxy Upstream Error: {e}")
            raise HTTPException(status_code=502, detail="Upstream LLM Server Error")

@app.get("/health")
async def health_check():
    """로드밸런서(ALB)용 상태 체크"""
    return {"status": "ok", "service": "safeai-gateway"}
