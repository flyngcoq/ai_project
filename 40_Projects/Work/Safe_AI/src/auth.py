from fastapi import Request, HTTPException
import logging

logger = logging.getLogger("safeai-proxy.auth")

# ==========================================
# 임시 고객사(Tenant) 데이터베이스 Mock
# 추후 PostgreSQL 또는 DynamoDB 연동
# ==========================================
MOCK_TENANT_DB = {
    "sk-safeai-test-tenant-a": {"tenant_id": "tenant-A", "tier": "premium", "rate_limit": 100},
    "sk-safeai-test-tenant-b": {"tenant_id": "tenant-B", "tier": "basic", "rate_limit": 10},
}

async def verify_tenant_api_key(request: Request) -> dict:
    """
    고객사가 헤더에 담아 보낸 Safe AI API Key를 검증하고 Tenant 정보를 반환합니다.
    (의존성 주입용 용도)
    """
    auth_header = request.headers.get("Authorization")
    api_key_header = request.headers.get("x-safeai-api-key")
    
    # Bearer 토큰 파싱
    extracted_key = None
    if auth_header and auth_header.startswith("Bearer "):
        extracted_key = auth_header.split(" ")[1]
    elif api_key_header:
        extracted_key = api_key_header
        
    if not extracted_key:
        raise HTTPException(
            status_code=401, 
            detail="Missing API Key. Provide it in 'Authorization' (Bearer) or 'x-safeai-api-key' header."
        )

    tenant_info = MOCK_TENANT_DB.get(extracted_key)
    if not tenant_info:
        logger.warning(f"Unauthorized API Key attempt: {extracted_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key or unauthorized tenant.")
        
    # TODO: rate limit 제어 로직 추가 (추후 Redis 연동)
    # check_rate_limit(tenant_info)
        
    return tenant_info
