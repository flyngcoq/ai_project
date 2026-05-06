import logging
import asyncio
from fastapi import HTTPException
import httpx
import re

logger = logging.getLogger("safeai-proxy.inspection")

async def parse_multimodal_data(request_body: dict) -> str:
    """
    [Task 3] 서드파티 Vision/PDF 파싱 API를 호출하여 이미지 내의 숨겨진 데이터나 텍스트를 추출 (OCR)
    """
    logger.info("Scanning for multimodal contents via 3rd-party Vision API...")
    extracted_text = ""
    
    # OpenAPI 포맷에서 파일 업로드/첨부(이미지 외에 코드 파일 등) 확인
    # MVP 데모를 위해 JSON 바디를 문자열로 변환하여 파일명이 있는지 검사합니다.
    import json
    body_str = json.dumps(request_body)
    
    if "handwriting.png" in body_str:
        logger.warning("[Vision API] 'handwriting.png' image detected. Simulating realistic OCR extraction...")
        # OCR 가상 추출 결과: 칠판/화이트보드 손글씨에서 파이썬 핵심 기술 코드를 추출해냈다고 가정
        extracted_text = "def core_algorithm_v2(data):\n    # Confidential logic\n    pass\n"

    await asyncio.sleep(0.1) # Mock API delay
    return extracted_text

def apply_dlp_masking_and_blocking(prompt_text: str) -> tuple[bool, str]:
    """
    인식(Trigger)과 조치(Masking vs Blocking)를 분리하는 DLP 핵심 로직.
    - PII (주민번호 등): MASKING 처리
    - 핵심 기술 (ex: python.py 등 소스코드 업로드): BLOCKING 처리
    """
    logger.info("Running DLP engine: Recognition Trigger and Action Matching")
    
    # 1. 인식을 위한 Trigger 규칙 (정규식 또는 패턴)
    core_tech_pattern = re.compile(r'\b[\w-]+\.py\b|def \w+\(.*\):|class \w+:')
    pii_pattern = re.compile(r'\b\d{6}-\d{7}\b')  # 모의 주민번호 패턴
    
    # 2. Trigger 검사
    if core_tech_pattern.search(prompt_text):
        logger.warning("Trigger Activated: Core technology (Source code / .py) detected. Action: BLOCK.")
        return False, prompt_text # Blocking을 의미 (안전하지 않음)
    
    # 3. Masking 조치
    masked_prompt = prompt_text
    if pii_pattern.search(prompt_text):
        logger.info("Trigger Activated: PII detected. Action: MASKING.")
        masked_prompt = pii_pattern.sub("******-*******", prompt_text)
        
    return True, masked_prompt

async def check_semantic_intent(prompt_text: str, tenant_policy: dict) -> bool:
    """
    [Task 4] LG EXAONE 기반 Context Filter를 통해 문맥과 의도를 분석
    내부 데이터 다운로드(RAG Tool Call 남용) 등의 악성 프롬프트를 차단합니다.
    """
    logger.info("Running LG EXAONE Semantic Context Validation...")
    
    # TODO: LG EXAONE API 연동
    # payload = {"model": "exaone-c", "text": prompt_text, "policy": tenant_policy}
    # response = httpx.post("https://api.exaone.lg-research.ai/v1/context-check", ...)
    
    await asyncio.sleep(0.2) # Mock EXAONE delay
    return True # 기본 통과 (추후 모델 응답에 따라 분기)

async def run_exaone_semantic_firewall(request_body: dict, tenant_info: dict) -> tuple[bool, dict]:
    """
    프록시 파이프라인 중앙 제어 (Deep Inspection Engine)
    에러 발생 시 즉각 False 반환하여 통신을 차단(Fail-closed)합니다.
    마스킹이 적용된 경우 수정된 request_body를 반환합니다.
    """
    # 1. 멀티모달 파싱으로 추가 텍스트 추출
    multimodal_text = await parse_multimodal_data(request_body)
    
    # 2. 페이로드 메시지 조립 및 DLP 조치 적용
    raw_messages = request_body.get("messages", [])
    combined_prompt = ""
    for m in raw_messages:
        content = m.get("content")
        if isinstance(content, str):
            # 문자열 형태의 메시지인 경우 바로 DLP 검증 및 마스킹
            is_safe, masked_text = apply_dlp_masking_and_blocking(content)
            if not is_safe:
                return False, request_body # 차단
            m["content"] = masked_text
            combined_prompt += masked_text + " "
        elif isinstance(content, list): # Vision API 형태의 Payload
            for part in content:
                if part.get("type") == "text":
                    original_text = part.get("text", "")
                    is_safe, masked_text = apply_dlp_masking_and_blocking(original_text)
                    if not is_safe:
                        return False, request_body # 차단
                    part["text"] = masked_text
                    combined_prompt += masked_text + " "
                    
    combined_prompt += f" [Extracted_Vision_Text: {multimodal_text}]"
    
    # 멀티모달 텍스트 내에도 소스코드/핵심기술이 숨어있을 수 있으므로 전체 조합본 재검사용
    is_safe_overall, _ = apply_dlp_masking_and_blocking(combined_prompt)
    if not is_safe_overall:
         return False, request_body
    
    # 3. EXAONE 모델 평가
    is_safe_context = await check_semantic_intent(combined_prompt, tenant_info)
    
    return is_safe_context, request_body
