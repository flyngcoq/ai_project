import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import sys
import os
import uuid

# ── 헬퍼 ──────────────────────────────────────────────────────
def emu(i):        return int(i * 914400)
def size(w, h):    return {"width":  {"magnitude": emu(w), "unit": "EMU"},
                            "height": {"magnitude": emu(h), "unit": "EMU"}}
def pos(x, y):     return {"scaleX": 1, "scaleY": 1,
                            "translateX": emu(x), "translateY": emu(y), "unit": "EMU"}
def rgb(r, g, b):  return {"red": r, "green": g, "blue": b}
def solid_fill(k): return {"solidFill": {"color": {"rgbColor": C[k]}}}
def font_size(k):  return {"magnitude": TYPE_SCALE[k], "unit": "PT"}
def uid(p=""):     return f"{p}_{uuid.uuid4().hex[:8]}"

# ── 팔레트 (EXECUTIVE) ────────────────────────────────────────
C = {
    "primary":    rgb(0.1020, 0.1529, 0.2667),  # #1A2744
    "primaryMid": rgb(0.1412, 0.2157, 0.3765),  # #243760
    "accent":     rgb(0.0000, 0.7765, 0.6824),  # #00C6AE
    "accentBlue": rgb(0.3098, 0.4980, 1.0000),  # #4F7FFF
    "white":      rgb(1.0000, 1.0000, 1.0000),  # #FFFFFF
    "surface":    rgb(0.9412, 0.9569, 1.0000),  # #F0F4FF
    "textMain":   rgb(0.1020, 0.1529, 0.2667),  # #1A2744
    "textSub":    rgb(0.5333, 0.6000, 0.7333),  # #8899BB
    "border":     rgb(0.8314, 0.8667, 0.9373),  # #D4DDEF
    "positive":   rgb(0.0627, 0.7255, 0.5059),  # #10B981
    "warning":    rgb(0.9608, 0.6196, 0.0431),  # #F59E0B
    "negative":   rgb(0.9373, 0.2667, 0.2667),  # #EF4444
}

# ── 타입 스케일 ───────────────────────────────────────────────
TYPE_SCALE = {
    "display": 44, "h1": 32, "h2": 24, "h3": 18,
    "bodyL": 16, "bodyM": 14, "bodyS": 12, "caption": 10, "micro": 8,
}

# ── 슬라이드 배경색 ───────────────────────────────────────────
def set_bg(requests, slide_id, color_key: str):
    requests.append({"updatePageProperties": {
        "objectId": slide_id,
        "pageProperties": {"pageBackgroundFill": solid_fill(color_key)},
        "fields": "pageBackgroundFill"
    }})

def add_header(requests, slide_id, title, prefix=None,
               bg="primary", line_color="accent",
               font_heading="Noto Serif KR"):
    sid = slide_id[:6]
    full_title = f"{prefix}{title}" if prefix else title

    # 배경
    requests.append({"createShape": {
        "objectId": f"{sid}_hdr_bg", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(10, 0.9), "transform": pos(0, 0)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{sid}_hdr_bg",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill(bg),
            "outline": {"outlineFill": solid_fill(bg)}},
        "fields": "shapeBackgroundFill,outline"}})

    # 강조선
    requests.append({"createShape": {
        "objectId": f"{sid}_hdr_line", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(10, 0.06), "transform": pos(0, 0.9)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{sid}_hdr_line",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill(line_color),
            "outline": {"outlineFill": solid_fill(line_color)}},
        "fields": "shapeBackgroundFill,outline"}})

    # 제목
    requests.append({"createShape": {
        "objectId": f"{sid}_hdr_txt", "shapeType": "TEXT_BOX",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(9, 0.9), "transform": pos(0.5, 0)}}})
    requests.append({"insertText": {
        "objectId": f"{sid}_hdr_txt", "text": full_title, "insertionIndex": 0}})
    requests.append({"updateTextStyle": {
        "objectId": f"{sid}_hdr_txt", "textRange": {"type": "ALL"},
        "style": {"bold": True, "fontSize": font_size("h2"),
                  "foregroundColor": {"opaqueColor": {"rgbColor": C["white"]}},
                  "fontFamily": font_heading},
        "fields": "bold,fontSize,foregroundColor,fontFamily"}})
    requests.append({"updateParagraphStyle": {
        "objectId": f"{sid}_hdr_txt", "textRange": {"type": "ALL"},
        "style": {"alignment": "START"}, "fields": "alignment"}})

def add_info_card(requests, slide_id, obj_prefix,
                  x, y, w, h, title, body,
                  style="light", accent_bar=True, accent_color="accent"):
    bg        = "surface" if style == "light" else "primary"
    title_col = "textMain" if style == "light" else "white"
    bdr       = "border"   if style == "light" else accent_color
    bdr_w     = 0.75       if style == "light" else 1.0

    requests.append({"createShape": {
        "objectId": f"{obj_prefix}_bg", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{obj_prefix}_bg",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill(bg),
            "outline": {"outlineFill": solid_fill(bdr),
                        "weight": {"magnitude": bdr_w, "unit": "PT"}}},
        "fields": "shapeBackgroundFill,outline"}})

    if accent_bar:
        requests.append({"createShape": {
            "objectId": f"{obj_prefix}_bar", "shapeType": "RECTANGLE",
            "elementProperties": {"pageObjectId": slide_id,
                "size": size(0.08, h), "transform": pos(x, y)}}})
        requests.append({"updateShapeProperties": {
            "objectId": f"{obj_prefix}_bar",
            "shapeProperties": {
                "shapeBackgroundFill": solid_fill(accent_color),
                "outline": {"outlineFill": solid_fill(accent_color)}},
            "fields": "shapeBackgroundFill,outline"}})

    tx = x + (0.08 + 0.12 if accent_bar else 0.12)
    tw = w - (0.08 + 0.12 if accent_bar else 0.12) - 0.08

    for oid, text, sk, bold, col, dy, dh in [
        (f"{obj_prefix}_title", title, "h3",    True,  title_col, 0.08, 0.32),
        (f"{obj_prefix}_body",  body,  "bodyM", False, "textSub", 0.44, max(h-0.52, 0.2)),
    ]:
        requests.append({"createShape": {
            "objectId": oid, "shapeType": "TEXT_BOX",
            "elementProperties": {"pageObjectId": slide_id,
                "size": size(tw, dh), "transform": pos(tx, y + dy)}}})
        requests.append({"insertText": {"objectId": oid, "text": text, "insertionIndex": 0}})
        requests.append({"updateTextStyle": {"objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {"bold": bold, "fontSize": font_size(sk),
                      "foregroundColor": {"opaqueColor": {"rgbColor": C[col]}},
                      "fontFamily": "Noto Serif KR" if bold else "Noto Sans KR"},
            "fields": "bold,fontSize,foregroundColor,fontFamily"}})

def add_numbered_card(requests, slide_id, obj_prefix,
                      x, y, w, h, number, title, body,
                      num_color="accent"):
    num_w = 0.52

    # 카드 배경
    requests.append({"createShape": {
        "objectId": f"{obj_prefix}_bg", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{obj_prefix}_bg",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill("primaryMid"),
            "outline": {"outlineFill": solid_fill(num_color),
                        "weight": {"magnitude": 1.0, "unit": "PT"}}},
        "fields": "shapeBackgroundFill,outline"}})

    # 번호 블록
    requests.append({"createShape": {
        "objectId": f"{obj_prefix}_num_bg", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(num_w, h), "transform": pos(x, y)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{obj_prefix}_num_bg",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill(num_color),
            "outline": {"outlineFill": solid_fill(num_color)}},
        "fields": "shapeBackgroundFill,outline"}})
    requests.append({"createShape": {
        "objectId": f"{obj_prefix}_num_txt", "shapeType": "TEXT_BOX",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(num_w, h), "transform": pos(x, y)}}})
    requests.append({"insertText": {
        "objectId": f"{obj_prefix}_num_txt", "text": str(number), "insertionIndex": 0}})
    requests.append({"updateTextStyle": {
        "objectId": f"{obj_prefix}_num_txt", "textRange": {"type": "ALL"},
        "style": {"bold": True, "fontSize": font_size("h2"),
                  "foregroundColor": {"opaqueColor": {"rgbColor": C["primary"]}},
                  "fontFamily": "Noto Serif KR"},
        "fields": "bold,fontSize,foregroundColor,fontFamily"}})
    requests.append({"updateParagraphStyle": {
        "objectId": f"{obj_prefix}_num_txt", "textRange": {"type": "ALL"},
        "style": {"alignment": "CENTER"}, "fields": "alignment"}})

    # 제목·본문
    tx, tw = x + num_w + 0.12, w - num_w - 0.2
    for oid, text, sk, bold, col, dy, dh in [
        (f"{obj_prefix}_title", title, "bodyL", True,  "white",   0.08, 0.32),
        (f"{obj_prefix}_body",  body,  "bodyS", False, "textSub", 0.44, max(h-0.52, 0.2)),
    ]:
        requests.append({"createShape": {
            "objectId": oid, "shapeType": "TEXT_BOX",
            "elementProperties": {"pageObjectId": slide_id,
                "size": size(tw, dh), "transform": pos(tx, y + dy)}}})
        requests.append({"insertText": {"objectId": oid, "text": text, "insertionIndex": 0}})
        requests.append({"updateTextStyle": {"objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {"bold": bold, "fontSize": font_size(sk),
                      "foregroundColor": {"opaqueColor": {"rgbColor": C[col]}},
                      "fontFamily": "Noto Serif KR" if bold else "Noto Sans KR"},
            "fields": "bold,fontSize,foregroundColor,fontFamily"}})

def add_text(requests, slide_id, obj_id, x, y, w, h, text,
             font="Noto Sans KR", scale="bodyM", color="textMain",
             bold=False, italic=False, align="START", bg_color=None):
    requests.append({"createShape": {
        "objectId": obj_id, "shapeType": "TEXT_BOX",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
    
    if bg_color:
        requests.append({"updateShapeProperties": {
            "objectId": obj_id,
            "shapeProperties": {
                "shapeBackgroundFill": solid_fill(bg_color),
            },
            "fields": "shapeBackgroundFill"}})

    requests.append({"insertText": {
        "objectId": obj_id, "text": text, "insertionIndex": 0}})
    requests.append({"updateTextStyle": {
        "objectId": obj_id, "textRange": {"type": "ALL"},
        "style": {"bold": bold, "italic": italic,
                  "fontSize": font_size(scale),
                  "foregroundColor": {"opaqueColor": {"rgbColor": C[color]}},
                  "fontFamily": font},
        "fields": "bold,italic,fontSize,foregroundColor,fontFamily"}})
    requests.append({"updateParagraphStyle": {
        "objectId": obj_id, "textRange": {"type": "ALL"},
        "style": {"alignment": align}, "fields": "alignment"}})


def main():
    print("Google Slides API 연동 및 의존성을 확인하세요.")
    print("이 코드는 service_account.json이 필요합니다.")
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("필수 패키지가 설치되지 않았습니다. (google-api-python-client, google-auth-oauthlib)")
        return

    SCOPES = ["https://www.googleapis.com/auth/presentations", "https://www.googleapis.com/auth/drive"]
    creds = None
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "token.json")
    client_secret_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "credentials.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secret_path):
                print(f"오류: OAuth 클라이언트 시크릿 파일이 없습니다. ({client_secret_path})")
                return
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    try:
        slides_svc = build("slides", "v1", credentials=creds)
    except Exception as e:
        print(f"인증 오류: {e}")
        return

    print("프레젠테이션 생성 중...")
    pres = slides_svc.presentations().create(body={"title": "U+Safe AI 출장 결과 보고 (Google Slides)"}).execute()
    pid  = pres["presentationId"]
    print(f"프레젠테이션 URL: https://docs.google.com/presentation/d/{pid}/edit")

    # 서비스 계정이 생성한 파일에 사용자가 접근할 수 있도록 권한 부여 (링크 있는 누구나 편집 가능)
    try:
        drive_svc = build("drive", "v3", credentials=creds)
        drive_svc.permissions().create(
            fileId=pid,
            body={"type": "anyone", "role": "writer"},
            fields="id"
        ).execute()
        print("✅ 문서 접근 권한(링크 있는 누구나 편집 가능) 설정 완료")
    except Exception as e:
        print(f"권한 설정 중 오류 (수동으로 공유 필요): {e}")

    # 기존 빈 슬라이드 1장은 삭제하거나 남겨두고 새 슬라이드 생성
    requests = []

    def add_slide_req():
        sid = f"s_{uuid.uuid4().hex[:6]}"
        requests.append({"createSlide": {
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
            "objectId": sid,
        }})
        return sid

    # ==========================================================
    # 1. 표지 (T-01)
    # ==========================================================
    s1 = add_slide_req()
    set_bg(requests, s1, "primary")
    
    # 좌측 세로선
    requests.append({"createShape": {"objectId": f"{s1}_line1", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": s1, "size": size(0.12, 5.625), "transform": pos(0, 0)}}})
    requests.append({"updateShapeProperties": {"objectId": f"{s1}_line1",
        "shapeProperties": {"shapeBackgroundFill": solid_fill("accent"), "outline": {"outlineFill": solid_fill("accent")}},
        "fields": "shapeBackgroundFill,outline"}})
    
    # 우측 장식
    requests.append({"createShape": {"objectId": f"{s1}_dec1", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": s1, "size": size(2.5, 5.625), "transform": pos(7.5, 0)}}})
    requests.append({"updateShapeProperties": {"objectId": f"{s1}_dec1",
        "shapeProperties": {"shapeBackgroundFill": solid_fill("primaryMid"), "outline": {"outlineFill": solid_fill("primaryMid")}},
        "fields": "shapeBackgroundFill,outline"}})

    # 타이틀
    add_text(requests, s1, f"{s1}_t1", 0.3, 1.2, 7.0, 1.5, "SILICON VALLEY\nDESIGN THINKING", 
             font="Noto Serif KR", scale="display", color="white", bold=True)
    add_text(requests, s1, f"{s1}_t2", 0.3, 3.0, 7.0, 0.5, "Problem-Finding을 향한 리드 러너들의 여정", 
             font="Noto Sans KR", scale="h3", color="accent", italic=True)

    # 하단 텍스트
    add_text(requests, s1, f"{s1}_t3", 0.3, 4.0, 7.0, 0.3, "썸띵 바이브 PM 최연수 | U+Safe AI 프로젝트", 
             font="Noto Sans KR", scale="bodyM", color="textSub")

    # ==========================================================
    # 2. MZ 인터뷰 인사이트 (T-03 인사이트)
    # ==========================================================
    s2 = add_slide_req()
    add_header(requests, s2, "MZ세대 보안 가치관의 극단적 양극화", prefix="01  ")
    
    # 배너
    add_text(requests, s2, f"{s2}_b1", 0.4, 1.1, 9.2, 0.5, 
             "⚠️ 우리의 가설은 완전히 틀렸다 — 평균적인 디지털 네이티브는 존재하지 않습니다.", 
             font="Noto Sans KR", scale="bodyM", color="textMain", bold=True, bg_color="warning", align="CENTER")

    # 두 개의 카드 (과연결자 vs 고립된 관찰자)
    add_info_card(requests, s2, f"{s2}_c1", 0.4, 1.8, 4.5, 2.5, 
                  "🗓️ User A — The Over-connector", 
                  "- 인간관계 절대 놓칠 수 없음 (2주치 일정 꽉 참)\n- Micro-share 및 얕고 넓은 관계 지향\n- 편의를 위해 기꺼이 정보 제공 가능",
                  style="light", accent_color="accentBlue")

    add_info_card(requests, s2, f"{s2}_c2", 5.1, 1.8, 4.5, 2.5, 
                  "🎮 User B — The Hesitant Loner", 
                  "- 약속 잡는 것 자체가 에너지 소모\n- 완벽한 프라이버시가 최우선\n- 통제권 상실에 대한 강한 두려움",
                  style="light", accent_color="negative")

    add_text(requests, s2, f"{s2}_b2", 0.4, 4.5, 9.2, 0.42, 
             "핵심 교훈: '평균적 페르소나'를 버리고, 극단적 사용자(Extreme User)로 세그먼트를 깊게 파고들어야 한다.", 
             font="Noto Sans KR", scale="bodyM", color="accent", bold=True, bg_color="primary", align="CENTER")

    # ==========================================================
    # 3. 빅테크 B2B 인사이트
    # ==========================================================
    s3 = add_slide_req()
    add_header(requests, s3, "B2B AI 도입의 절대적 페인포인트", prefix="02  ")

    add_info_card(requests, s3, f"{s3}_c1", 0.4, 1.3, 4.5, 1.5,
                  "NVIDIA & META — 10배의 퍼포먼스",
                  "엔비디아 4만 명 전 직원 필수 사용 및 메타 10배 퍼포먼스 주문.\n강력한 Top-down 독려가 가능했던 이유는 '사내 데이터 완벽 보호' 가드레일이 세팅되었기 때문.",
                  style="light", accent_color="positive")

    add_info_card(requests, s3, f"{s3}_c2", 5.1, 1.3, 4.5, 1.5,
                  "TESLA & LUCID — 리스크와 보수적 접근",
                  "제조업 특성상 데이터 유출 리스크에 대한 우려.\n일부 부서에만 제한적으로 AI를 허용하는 등 확고한 보안 없이는 전사적 확산 불가능.",
                  style="light", accent_color="warning")

    add_text(requests, s3, f"{s3}_b1", 0.4, 3.2, 9.2, 1.5, 
             "결론: B2B 시장에서 전사적인 AI 도입을 이끌어내기 위한 가장 절대적인 페인포인트는\n결국 '완벽한 보안 가드레일의 구축'이다.", 
             font="Noto Sans KR", scale="h3", color="textMain", bold=True, bg_color="surface", align="CENTER")


    # ==========================================================
    # 4. Safe AI 3B 전략 (T-06 CTA 형태 차용)
    # ==========================================================
    s4 = add_slide_req()
    set_bg(requests, s4, "primary")
    
    add_text(requests, s4, f"{s4}_t1", 0.4, 0.6, 9.2, 0.5, "U+Safe AI의 B2B 전략", 
             font="Noto Sans KR", scale="h3", color="accent")
    add_text(requests, s4, f"{s4}_t2", 0.4, 1.0, 9.2, 0.6, "숨은 니즈 해결과 3B 마케팅의 결합", 
             font="Noto Serif KR", scale="h1", color="white", bold=True)

    add_numbered_card(requests, s4, f"{s4}_n1", 0.4, 2.0, 9.2, 0.8, 1, 
                      "작고 뾰족한 세그먼트 집중 (Pull Marketing)", 
                      "국내 B2B 인터뷰를 통해 발굴한 세그먼트들의 숨은 니즈를 완벽히 해결하여 작지만 확실한 1등 달성",
                      num_color="accent")
    
    add_numbered_card(requests, s4, f"{s4}_n2", 0.4, 3.0, 9.2, 0.8, 2, 
                      "3B (Buy, Borrow, Build) 관점의 기술 확보", 
                      "모든 것을 직접 만들지 않고, 외부 최고의 기술을 유연하게 빌리거나 사들여 우리만의 보안 솔루션으로 융합",
                      num_color="accentBlue")

    add_numbered_card(requests, s4, f"{s4}_n3", 0.4, 4.0, 9.2, 0.8, 3, 
                      "고부가가치 구독형 비즈니스로 확장", 
                      "안전한 AI 환경을 기반으로 버티컬 AI 워크에이전트 연계 판매 등 자산 효율성이 높은 B2B 사업모델로 안착",
                      num_color="positive")

    # ==========================================================
    # 5. 경영진 스폰서십 요청
    # ==========================================================
    s5 = add_slide_req()
    set_bg(requests, s5, "primaryMid")
    
    add_text(requests, s5, f"{s5}_t1", 0.4, 1.0, 9.2, 0.5, "CALL TO ACTION", 
             font="Noto Sans KR", scale="h3", color="accent", align="CENTER")
    add_text(requests, s5, f"{s5}_t2", 0.4, 1.5, 9.2, 0.8, "시장 선점을 위한 3대 핵심 스폰서십 요청", 
             font="Noto Serif KR", scale="display", color="white", bold=True, align="CENTER")

    add_text(requests, s5, f"{s5}_t3", 1.0, 2.3, 8.0, 2.0, 
             "① 보안 검토 패스트트랙 (Fast-track) 권한 부여\n"
             "  • 파일럿 프로젝트에 한해 3주 소요되던 보안/법무 검토를 3일로 단축\n\n"
             "② 인프라 샌드박스 예산 선제적 승인\n"
             "  • 빠른 프로토타입 검증을 위한 GPU 및 API 클라우드 테스트 자원 포괄적 허가\n\n"
             "③ 통신 보안 네트워크 전문가 단기 합류\n"
             "  • 3B 융합 전략 완성을 위해 전사 보안/네트워크 최고 전문가 2인의 TF 파견 지원", 
             font="Noto Sans KR", scale="bodyL", color="surface", align="LEFT")

    add_text(requests, s5, f"{s5}_t4", 0.4, 4.5, 9.2, 0.5, 
             "실무진은 현장에서 답을 찾겠습니다. B2B AI 시장의 판도를 바꿀 가장 강력한 성공 경험을 증명해 내겠습니다.", 
             font="Noto Sans KR", scale="bodyL", color="accent", bold=True, align="CENTER")


    # ── batchUpdate 전송 ─────────────────────────────────────────
    print(f"총 {len(requests)}개의 요청을 슬라이드에 반영합니다...")
    if requests:
        slides_svc.presentations().batchUpdate(
            presentationId=pid, body={"requests": requests}
        ).execute()
        print("슬라이드 생성 완료!")

if __name__ == "__main__":
    main()
