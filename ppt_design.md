# AI PPT 디자인 시스템 — Google Slides API
> Gemini + Google Slides API(Python)로 일관성 있는 프레젠테이션을 생성하기 위한 설계 기준서

---

## 목차

1. [디자인 원칙](#1-디자인-원칙)
2. [Google Slides API 핵심 개념](#2-google-slides-api-핵심-개념)
3. [단위 시스템 — EMU](#3-단위-시스템--emu)
4. [컬러 시스템](#4-컬러-시스템)
5. [타이포그래피](#5-타이포그래피)
6. [레이아웃 그리드](#6-레이아웃-그리드)
7. [컴포넌트 라이브러리](#7-컴포넌트-라이브러리)
8. [슬라이드 템플릿](#8-슬라이드-템플릿)
9. [Gemini 프롬프트 설계](#9-gemini-프롬프트-설계)
10. [QA 체크리스트](#10-qa-체크리스트)
11. [코드 스니펫 레퍼런스](#11-코드-스니펫-레퍼런스)
12. [환경 설정](#12-환경-설정)

---

## 1. 디자인 원칙

### 원칙 1 — 위계 우선

모든 슬라이드에서 시각적 위계는 명확해야 한다. AI가 슬라이드를 구성할 때 아래 순서를 지킨다.

```
1순위: 슬라이드 제목 (무엇을 말하는가)
2순위: 핵심 수치 또는 키워드 (가장 중요한 한 가지)
3순위: 지지 내용 (근거, 설명, 데이터)
4순위: 출처, 날짜, 페이지 번호
```

### 원칙 2 — 슬라이드 1장 = 메시지 1개

슬라이드 제목은 주제어가 아닌 주장 문장으로 작성한다.

| ❌ 주제어 | ✅ 주장 문장 |
|---|---|
| MZ 세대 인터뷰 결과 | MZ 세대 내 보안 가치관은 180° 다르다 |
| 시장 경쟁력 | Safe AI는 양극단 사용자를 동시에 포섭한다 |
| 비용 분석 | 초기 투자 대비 18개월 내 ROI 전환 가능 |

### 원칙 3 — 여백은 낭비가 아니다

슬라이드의 최소 30%는 여백이어야 한다. AI는 공간을 채우려는 경향이 있으므로 텍스트 상한을 명시적으로 지시한다.

```
제목:         최대 15자
본문 1개 항목: 최대 25자
항목 수:      최대 5개
```

### 원칙 4 — 색은 의미를 전달한다

색은 반드시 아래 역할 중 하나를 수행한다. 장식용 색은 사용하지 않는다.

- **구분**: 섹션 또는 카테고리를 나눌 때
- **강조**: 가장 중요한 정보를 부각할 때
- **상태**: 긍정(초록) / 부정(빨강) / 중립(회색)

### 원칙 5 — 텍스트는 덜할수록 좋다

슬라이드는 책이 아니다. 청중은 발표자를 들으며 슬라이드를 스캔한다.

---

## 2. Google Slides API 핵심 개념

### 2.1 작동 원리

Google Slides API는 "무엇을 만들어라"가 아니라 "무엇을 바꿔라" 방식으로 동작한다.

```
1. 빈 프레젠테이션 생성  →  presentationId 획득
2. 슬라이드 추가         →  slideId 획득
3. 도형·텍스트박스 생성  →  objectId 획득
4. 스타일 적용           →  objectId 참조
5. 위 3~4를 requests 배열에 모아 batchUpdate 1회 호출
```

### 2.2 requests 배열 패턴

모든 변경사항을 `requests` 리스트에 딕셔너리로 쌓고, 슬라이드 완성 후 한 번만 전송한다.

```python
requests = []

# 도형 생성
requests.append({
    "createShape": {
        "objectId": "myRect_01",
        "shapeType": "RECTANGLE",
        "elementProperties": {
            "pageObjectId": slide_id,
            "size": size(w, h),
            "transform": pos(x, y)
        }
    }
})

# 스타일 적용 (반드시 createShape 이후)
requests.append({
    "updateShapeProperties": {
        "objectId": "myRect_01",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill("primary"),
            "outline": {"outlineFill": solid_fill("primary")}
        },
        "fields": "shapeBackgroundFill,outline"
    }
})

# 슬라이드 완성 후 한 번에 전송
slides_svc.presentations().batchUpdate(
    presentationId=pid,
    body={"requests": requests}
).execute()
```

### 2.3 objectId 작명 규칙

같은 프레젠테이션 내 objectId는 고유해야 한다.

```
형식: {슬라이드번호}_{요소역할}_{순번}

예시:
  s01_hdr_bg        슬라이드 1 — 헤더 배경
  s01_hdr_line      슬라이드 1 — 헤더 강조선
  s01_card_01       슬라이드 1 — 첫 번째 카드 배경
  s01_card_01_title 슬라이드 1 — 첫 번째 카드 제목
  s03_kpi_01_val    슬라이드 3 — 첫 번째 KPI 수치
```

### 2.4 텍스트 삽입 순서

순서가 바뀌면 스타일이 적용되지 않는다.

```
createShape(TEXT_BOX) → insertText → updateTextStyle → updateParagraphStyle
```

```python
requests.append({"createShape": {"objectId": "tb_01", "shapeType": "TEXT_BOX",
    "elementProperties": {"pageObjectId": slide_id,
        "size": size(w, h), "transform": pos(x, y)}}})

requests.append({"insertText": {
    "objectId": "tb_01", "text": "내용", "insertionIndex": 0}})

requests.append({"updateTextStyle": {"objectId": "tb_01",
    "textRange": {"type": "ALL"},
    "style": {
        "bold": True,
        "fontSize": {"magnitude": 18, "unit": "PT"},
        "foregroundColor": {"opaqueColor": {"rgbColor": C["white"]}},
        "fontFamily": "Noto Sans KR"
    },
    "fields": "bold,fontSize,foregroundColor,fontFamily"}})

requests.append({"updateParagraphStyle": {"objectId": "tb_01",
    "textRange": {"type": "ALL"},
    "style": {"alignment": "START"},
    "fields": "alignment"}})
```

---

## 3. 단위 시스템 — EMU

### 3.1 기본 변환

```
1 인치 = 914,400 EMU
1 cm  = 360,000 EMU
1 pt  = 12,700 EMU
```

### 3.2 헬퍼 함수

Gemini에게 코드 생성 시 반드시 포함하도록 지시한다.

```python
def emu(inches: float) -> int:
    return int(inches * 914400)

def size(w_inch, h_inch) -> dict:
    return {
        "width":  {"magnitude": emu(w_inch), "unit": "EMU"},
        "height": {"magnitude": emu(h_inch), "unit": "EMU"}
    }

def pos(x_inch, y_inch) -> dict:
    return {
        "scaleX": 1, "scaleY": 1,
        "translateX": emu(x_inch),
        "translateY": emu(y_inch),
        "unit": "EMU"
    }

def rgb(r: float, g: float, b: float) -> dict:
    """0.0~1.0 범위 float"""
    return {"red": r, "green": g, "blue": b}
```

### 3.3 슬라이드 치수 기준값

```
슬라이드 W:        9,144,000  (10")
슬라이드 H:        5,143,500  (5.625")
마진 좌우:           365,760  (0.4")
마진 상하:           457,200  (0.5")
헤더 H:              822,960  (0.9")
헤더 강조선 H:        54,864  (0.06")
콘텐츠 시작 Y:       914,400  (1.0")
푸터 시작 Y:       4,754,880  (5.2")
카드 gap:            182,880  (0.2")
카드 accent bar W:    73,152  (0.08")
카드 내부 padding:   109,728  (0.12")
번호블록 W:          475,488  (0.52")
```

### 3.4 자주 쓰는 EMU 변환표

| 인치 | EMU |
|---|---|
| 0.06 | 54,864 |
| 0.08 | 73,152 |
| 0.12 | 109,728 |
| 0.2  | 182,880 |
| 0.4  | 365,760 |
| 0.52 | 475,488 |
| 0.9  | 822,960 |
| 1.0  | 914,400 |
| 2.9  | 2,651,760 |
| 4.5  | 4,114,800 |
| 9.2  | 8,412,480 |
| 10.0 | 9,144,000 |

---

## 4. 컬러 시스템

Google Slides API는 색상을 `{red, green, blue}` float 형태로 받는다. 아래 팔레트를 그대로 붙여넣어 사용한다.

### 4.1 팔레트 구조

| 역할 | 설명 | 사용 비율 |
|---|---|---|
| Primary | 헤더, 배경, 강조 요소 | 60% |
| Accent | 핵심 수치, 강조선, CTA | 15% |
| Neutral | 배경, 본문, 구분선 | 20% |
| Semantic | 상태 표현 (성공/경고/오류) | 5% |

### 4.2 팔레트 5종

---

#### 🎯 EXECUTIVE — 경영진 보고, 투자자 발표

```python
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
```

---

#### 💡 INNOVATION — 스타트업, 신사업 제안 (다크)

```python
C = {
    "primary":      rgb(0.0588, 0.0902, 0.1647),  # #0F172A
    "primaryMid":   rgb(0.1176, 0.1608, 0.2314),  # #1E293B
    "accent":       rgb(0.0235, 0.7137, 0.8314),  # #06B6D4
    "accentPurple": rgb(0.6588, 0.3333, 0.9686),  # #A855F7
    "white":        rgb(0.9725, 0.9804, 0.9882),  # #F8FAFC
    "surface":      rgb(0.1176, 0.1608, 0.2314),  # #1E293B
    "textMain":     rgb(0.9725, 0.9804, 0.9882),  # #F8FAFC
    "textSub":      rgb(0.5804, 0.6392, 0.7216),  # #94A3B8
    "border":       rgb(0.2000, 0.2549, 0.3333),  # #334155
    "positive":     rgb(0.2039, 0.8275, 0.6000),  # #34D399
    "warning":      rgb(0.9843, 0.7490, 0.1412),  # #FBBF24
    "negative":     rgb(0.9725, 0.4431, 0.4431),  # #F87171
}
```

---

#### 🔬 TECHNICAL — 개발, 데이터, 기술 문서

```python
C = {
    "primary":     rgb(0.0667, 0.0941, 0.1529),  # #111827
    "primaryMid":  rgb(0.1216, 0.1608, 0.2157),  # #1F2937
    "accent":      rgb(0.2314, 0.5098, 0.9647),  # #3B82F6
    "accentGreen": rgb(0.0627, 0.7255, 0.5059),  # #10B981
    "white":       rgb(1.0000, 1.0000, 1.0000),  # #FFFFFF
    "surface":     rgb(0.9765, 0.9804, 0.9843),  # #F9FAFB
    "textMain":    rgb(0.0667, 0.0941, 0.1529),  # #111827
    "textSub":     rgb(0.4196, 0.4471, 0.5020),  # #6B7280
    "border":      rgb(0.8980, 0.9059, 0.9176),  # #E5E7EB
    "positive":    rgb(0.0235, 0.5882, 0.4118),  # #059669
    "warning":     rgb(0.8510, 0.4706, 0.0392),  # #D97706
    "negative":    rgb(0.8627, 0.1490, 0.1490),  # #DC2626
}
```

---

#### 🌿 WELLBEING — HR, ESG, 교육, 문화

```python
C = {
    "primary":    rgb(0.1098, 0.2392, 0.1804),  # #1C3D2E
    "primaryMid": rgb(0.1765, 0.3529, 0.2588),  # #2D5A42
    "accent":     rgb(0.4863, 0.7882, 0.6078),  # #7CC99B
    "accentGold": rgb(0.9608, 0.7843, 0.2588),  # #F5C842
    "white":      rgb(0.9804, 0.9804, 0.9686),  # #FAFAF7
    "surface":    rgb(0.9412, 0.9529, 0.9333),  # #F0F4EE
    "textMain":   rgb(0.1098, 0.2392, 0.1804),  # #1C3D2E
    "textSub":    rgb(0.4196, 0.5490, 0.4667),  # #6B8C77
    "border":     rgb(0.8196, 0.8902, 0.8471),  # #D1E3D8
    "positive":   rgb(0.0863, 0.6392, 0.2902),  # #16A34A
    "warning":    rgb(0.7922, 0.5412, 0.0157),  # #CA8A04
    "negative":   rgb(0.8627, 0.1490, 0.1490),  # #DC2626
}
```

---

#### ⚡ BOLD — 마케팅, 캠페인, 대외 발표

```python
C = {
    "primary":      rgb(0.1020, 0.0196, 0.2000),  # #1A0533
    "primaryMid":   rgb(0.1765, 0.0706, 0.3412),  # #2D1257
    "accent":       rgb(0.9137, 0.2784, 0.3412),  # #E84757
    "accentYellow": rgb(0.9608, 0.8275, 0.1647),  # #F5D32A
    "white":        rgb(1.0000, 1.0000, 1.0000),  # #FFFFFF
    "surface":      rgb(0.1765, 0.0706, 0.3412),  # #2D1257
    "textMain":     rgb(1.0000, 1.0000, 1.0000),  # #FFFFFF
    "textSub":      rgb(0.7020, 0.6157, 0.8549),  # #B39DDB
    "border":       rgb(0.2902, 0.1608, 0.5020),  # #4A2980
    "positive":     rgb(0.1804, 0.8000, 0.4431),  # #2ECC71
    "warning":      rgb(1.0000, 0.6235, 0.2627),  # #FF9F43
    "negative":     rgb(0.9137, 0.2784, 0.3412),  # #E84757
}
```

---

### 4.3 색상 사용 규칙

```
✅ 허용
- 동일 팔레트 내 색상만 조합
- 슬라이드당 Accent 색상 최대 2종
- 어두운 배경 → 텍스트 white 또는 surface
- 밝은 배경 → 텍스트 textMain

❌ 금지
- 팔레트 외 임의 색상 추가
- Primary와 Accent를 동일 비중으로 병치
- 텍스트·배경 명도 대비 WCAG AA 기준(4.5:1) 미달
- 빨강·초록 동시 사용 (색맹 접근성)
```

### 4.4 solidFill 헬퍼

```python
def solid_fill(key: str) -> dict:
    return {"solidFill": {"color": {"rgbColor": C[key]}}}

def font_size(key: str) -> dict:
    return {"magnitude": TYPE_SCALE[key], "unit": "PT"}
```

---

## 5. 타이포그래피

### 5.1 Google Fonts 사용

fontFamily 문자열만으로 Google Fonts 전체를 사용할 수 있다. 별도 설치 없이 한글 폰트를 바로 쓸 수 있다.

### 5.2 추천 폰트 페어링

| 페어링 | 제목 폰트 | 본문 폰트 | 어울리는 팔레트 |
|---|---|---|---|
| Korean Executive | `Noto Serif KR` | `Noto Sans KR` | EXECUTIVE |
| Korean Modern | `Black Han Sans` | `Noto Sans KR` | INNOVATION, BOLD |
| Korean Warm | `Nanum Myeongjo` | `Nanum Gothic` | WELLBEING |
| Korean Clean | `Noto Sans KR` 700 | `Noto Sans KR` 400 | TECHNICAL |
| Mixed Premium | `Playfair Display` | `Noto Sans KR` | EXECUTIVE (영문 강조) |

### 5.3 타입 스케일

```python
TYPE_SCALE = {
    "display": 44,  # 표지 메인 제목
    "h1":      32,  # 섹션 제목
    "h2":      24,  # 슬라이드 제목 (헤더 바)
    "h3":      18,  # 카드·박스 소제목
    "bodyL":   16,  # 여유 레이아웃 본문
    "bodyM":   14,  # 표준 본문
    "bodyS":   12,  # 보조 설명·캡션
    "caption": 10,  # 출처·날짜·페이지
    "micro":    8,  # 태그·라벨 (최솟값)
}
```

### 5.4 텍스트 스타일 규칙

```
✅ 허용
- 제목: bold=True + 제목 폰트
- 인용: italic=True
- 핵심 수치: bold=True + accent 색상

❌ 금지
- 동일 텍스트박스에 3가지 이상 폰트 크기
- underline 강조 (링크로 혼동)
- 8pt 미만 폰트
- 본문 전체 대문자
```

---

## 6. 레이아웃 그리드

### 6.1 기준 상수

```python
SLIDE = {"w": 9144000, "h": 5143500}

GRID = {
    "margin_x":       365760,  # 0.4" 좌우 안전 마진
    "margin_y":       457200,  # 0.5" 상하 안전 마진
    "header_h":       822960,  # 0.9" 헤더 바
    "accent_line_h":   54864,  # 0.06" 헤더 강조선
    "content_y":      914400,  # 1.0" 콘텐츠 시작
    "content_h":     3932100,  # 4.3" 콘텐츠 영역
    "footer_y":      4754880,  # 5.2" 푸터 시작
    "footer_h":       365760,  # 0.4" 푸터
    "content_w":     8412480,  # 9.2" 마진 제외 너비
    "card_gap":       182880,  # 0.2" 카드 간격
    "card_padding":   109728,  # 0.12" 카드 내부 오프셋
    "accent_bar_w":    73152,  # 0.08" 좌측 강조선
    "num_block_w":    475488,  # 0.52" 번호 블록
}
```

### 6.2 컬럼 레이아웃 (인치 기준 — 호출 시 emu() 변환)

```python
COL = {
    "full":  {"x": 0.4,  "w": 9.2},          # 1컬럼

    "2L":    {"x": 0.4,  "w": 4.5},           # 2컬럼 50/50
    "2R":    {"x": 5.1,  "w": 4.5},

    "2_40":  {"x": 0.4,  "w": 3.8},           # 2컬럼 40/60
    "2_60":  {"x": 4.3,  "w": 5.4},

    "3_1":   {"x": 0.4,  "w": 2.9},           # 3컬럼 equal
    "3_2":   {"x": 3.55, "w": 2.9},
    "3_3":   {"x": 6.7,  "w": 2.9},

    "4_1":   {"x": 0.4,  "w": 2.1},           # 4컬럼 equal
    "4_2":   {"x": 2.7,  "w": 2.1},
    "4_3":   {"x": 5.0,  "w": 2.1},
    "4_4":   {"x": 7.3,  "w": 2.3},
}
```

---

## 7. 컴포넌트 라이브러리

### 7.1 헤더 바

```python
def add_header(requests, slide_id, title, prefix=None,
               bg="primary", line_color="accent",
               font_heading="Noto Serif KR"):
    """
    모든 콘텐츠 슬라이드 공통 헤더.
    prefix 예시: "01  " (번호 + 전각 공백 2칸)
    """
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
```

### 7.2 정보 카드

```python
def add_info_card(requests, slide_id, obj_prefix,
                  x, y, w, h, title, body,
                  style="light", accent_bar=True, accent_color="accent"):
    """
    style="light": surface 배경
    style="dark":  primary 배경
    """
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
```

### 7.3 번호 카드

```python
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
        "style": {"bold": True, "fontSize": font_size("h1"),
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
```

### 7.4 KPI 수치 블록

```python
def add_kpi_block(requests, slide_id, obj_prefix,
                  x, y, w, h, value, unit_str, label,
                  trend=None, trend_positive=True):
    """value="87"  unit_str="%"  label="고객 만족도"  trend="▲3.2%" """

    requests.append({"createShape": {
        "objectId": f"{obj_prefix}_bg", "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
    requests.append({"updateShapeProperties": {
        "objectId": f"{obj_prefix}_bg",
        "shapeProperties": {
            "shapeBackgroundFill": solid_fill("surface"),
            "outline": {"outlineFill": solid_fill("border"),
                        "weight": {"magnitude": 0.75, "unit": "PT"}}},
        "fields": "shapeBackgroundFill,outline"}})

    items = [
        (f"{obj_prefix}_val",   value+unit_str, 36, True,  "accent",  "CENTER", 0.15, 0.72),
        (f"{obj_prefix}_label", label,          12, False, "textSub", "CENTER", 0.90, 0.28),
    ]
    if trend:
        items.append((f"{obj_prefix}_trend", trend, 10, False,
                      "positive" if trend_positive else "negative", "CENTER", 1.22, 0.22))

    for oid, text, pt_sz, bold, col, align, dy, dh in items:
        requests.append({"createShape": {
            "objectId": oid, "shapeType": "TEXT_BOX",
            "elementProperties": {"pageObjectId": slide_id,
                "size": size(w-0.24, dh), "transform": pos(x+0.12, y+dy)}}})
        requests.append({"insertText": {"objectId": oid, "text": text, "insertionIndex": 0}})
        requests.append({"updateTextStyle": {"objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {"bold": bold,
                      "fontSize": {"magnitude": pt_sz, "unit": "PT"},
                      "foregroundColor": {"opaqueColor": {"rgbColor": C[col]}},
                      "fontFamily": "Noto Serif KR" if bold else "Noto Sans KR"},
            "fields": "bold,fontSize,foregroundColor,fontFamily"}})
        requests.append({"updateParagraphStyle": {"objectId": oid,
            "textRange": {"type": "ALL"},
            "style": {"alignment": align}, "fields": "alignment"}})
```

---

## 8. 슬라이드 템플릿

### T-01: 표지

```
배경:         set_bg → primary
좌측 세로선:  x=0  w=0.12  h=5.625  fill=accent
우측 장식:    x=7.5  w=2.5  fill=primaryMid
태그 칩:      x=0.3  y=0.55  h=0.32  fill=accent  텍스트 primary
메인 타이틀:  display 44pt  bold  white+accent 조합  x=0.3  y=1.2
서브타이틀:   15pt  italic  textSub  x=0.3  y=3.2
구분선:       createLine  y=3.8  color=textSub
메타 정보:    11pt  textSub  y=4.0
Agenda 칩:   4개 가로 배열  y=4.75  h=0.38  fill=primaryMid  border=accentBlue
```

### T-02: 목차

```
add_header
add_numbered_card × N (세로 배열)
카드 높이: (5.625 - 1.0 - 0.4) / N  (최소 0.75"  최대 1.1")
섹션별 num_color 순환: accent → accentBlue → warning → negative
```

### T-03: 인사이트

```
add_header
경고 배너:   x=0.3  y=1.05  w=9.4  h=0.5  fill=warning
좌측 (55%): 인용 블록  fill=primary  텍스트 italic white
우측 (40%): add_info_card × 2  style=light
하단 결론:  x=0.3  w=9.4  h=0.42  fill=primary  텍스트 accent
```

### T-04: 비교

```
add_header
Before 카드: fill=rgb(0.996,0.949,0.949)  border=negative  레이블 "BEFORE ❌"
After 카드:  fill=rgb(0.941,0.992,0.961)  border=positive  레이블 "AFTER ✅"
2컬럼 50/50
하단 결론 배너
```

### T-05: 데이터

```
add_header
add_kpi_block × 3~4 (상단 배열)
차트: 공개 이미지 URL → add_image
인사이트 텍스트 (우측 또는 하단)
```

### T-06: CTA

```
배경:         set_bg → primary
상단 강조선:  x=0  y=0  w=10  h=0.08  fill=accent
섹션 레이블:  h3  accent  y=0.18
핵심 메시지:  h1  bold  white+accent 조합  y=0.8
add_numbered_card × 3 (세로 배열)
클로징 문장:  caption  italic  textSub  align=CENTER  y=5.1
```

### T-07: 섹션 구분

```
배경:        set_bg → primary
번호 장식:   display  accent  (배경 레이어, 투명도 낮게)
섹션 제목:   h1  white  align=CENTER
서브타이틀:  h3  textSub  italic  align=CENTER
```

---

## 9. Gemini 프롬프트 설계

### 9.1 표준 프롬프트 템플릿

```markdown
## 역할
당신은 Google Slides API와 Python으로 프레젠테이션을 생성하는 전문가입니다.
아래 디자인 시스템을 엄격히 준수하여 코드를 작성하세요.

## 환경
- Python 3
- google-api-python-client
- 인증: service_account.json (경로: ./service_account.json)

## 디자인 시스템 규칙
- 팔레트: [팔레트 이름]  (색상 코드 첨부)
- 폰트: 제목=[제목폰트]  본문=[본문폰트]
- 슬라이드 크기: W=9144000  H=5143500 (EMU)
- 좌표·크기: emu() 헬퍼로 변환
- 색상: {red, green, blue} float (0.0~1.0)
- objectId: {슬라이드번호}_{역할}_{순번} 형식, 전체 고유
- requests 순서: createShape → updateShapeProperties
                 → insertText → updateTextStyle → updateParagraphStyle
- batchUpdate: 슬라이드 완성 후 1회 호출

## 슬라이드 목록
[번호]: [템플릿] — [제목] — [콘텐츠 요약]

## 출력
완전한 Python 실행 가능 코드. 마지막에 Google Slides URL 출력.
```

### 9.2 슬라이드별 콘텐츠 명세 형식

```markdown
### 슬라이드 4 — T-03 (인사이트)
헤더: prefix="02  "  title="MZ 인터뷰의 배신: 페르소나의 함정"
경고 배너 텍스트: "⚠️ 우리의 가설은 틀렸다 — 같은 MZ 세대 안에서도 보안 가치관이 180° 달랐습니다"
경고 배너 색: warning

좌측 인용 블록: (obj_prefix: s04_quote)
  배경: primary
  인용: "어느 한 기업이 내 인생의 모든 것을 아는 건 소름 끼쳐요..."
  출처: "User A — The Protector"

우측 카드 1: (obj_prefix: s04_card_a)
  style=light  accent_color=accentBlue
  title: "🛡️ User A — The Protector"
  body: "핵심 니즈: 개인 데이터 완전 통제권\n행동 패턴: BeReal·Micro-share 선호"

우측 카드 2: (obj_prefix: s04_card_b)
  style=light  accent_color=accent
  title: "⚡ User B — The Optimizer"
  body: "핵심 니즈: 최대한의 AI 자동화·편의성\n행동 패턴: 보안은 회사 책임, 효율 극대화"

하단 결론: "핵심 교훈: '평균적 페르소나'는 아무도 만족시킬 수 없다 → Extreme User에 집중"
```

### 9.3 오류 교정 지시

| 증상 | 교정 지시 |
|---|---|
| `Invalid requests[N].createShape` | "전체 objectId를 점검하고 고유하게 재작성해라 — 형식: s{슬라이드번호}_{역할}_{순번}" |
| 텍스트가 보이지 않음 | "insertText가 createShape 뒤에 오는지, updateTextStyle fields에 fontFamily가 있는지 확인해라" |
| 색상 오류 `Invalid value` | "모든 red/green/blue가 0.0~1.0 범위인지 확인해라. 255 초과 값은 255.0으로 나눠라" |
| 도형이 슬라이드 밖으로 나감 | "translateX+width ≤ 9144000, translateY+height ≤ 5143500 조건을 확인하고 수정해라" |
| 슬라이드 배경색 미적용 | "배경은 updatePageProperties를 사용해야 한다. updateShapeProperties가 아님을 확인해라" |
| 선이 생성 안 됨 | "선은 createShape가 아닌 createLine을 사용해야 한다" |
| batchUpdate 오류 | "모든 requests를 하나의 리스트로 합쳐 batchUpdate를 1회만 호출해라" |

---

## 10. QA 체크리스트

### 코드 실행 전

```
[ ] 전체 프레젠테이션에서 objectId가 모두 고유한가?
[ ] 텍스트 requests 순서: createShape → insertText → updateTextStyle → updateParagraphStyle?
[ ] 모든 색상 float 값이 0.0~1.0 범위인가?
[ ] translateX + width  ≤ 9,144,000
[ ] translateY + height ≤ 5,143,500
[ ] batchUpdate가 슬라이드당 1회인가?
[ ] 슬라이드 배경은 updatePageProperties로 설정했는가?
[ ] 선(LINE) 생성에 createLine을 사용했는가?
```

### 생성 결과 시각 검토

```
[ ] 헤더 바가 모든 슬라이드에서 동일한 위치·높이인가?
[ ] 텍스트가 박스 경계를 벗어나지 않는가?
[ ] 좌우 마진 0.4" 이상 확보되어 있는가?
[ ] 카드 간격이 균등한가?
[ ] 팔레트 외 색상이 사용되지 않았는가?
[ ] 폰트가 정상 로드되는가? (Google Fonts, 인터넷 필요)
```

### 콘텐츠 검토

```
[ ] 슬라이드당 메시지가 하나인가?
[ ] 제목이 주장 문장인가?
[ ] 항목 수 ≤ 5, 항목당 글자 수 ≤ 25자인가?
[ ] 수치에 단위와 기준 시점이 있는가?
```

---

## 11. 코드 스니펫 레퍼런스

### 11.1 프로젝트 초기화 전체 템플릿

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account
import uuid

# ── 인증 ──────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]
creds = service_account.Credentials.from_service_account_file(
    "service_account.json", scopes=SCOPES
)
slides_svc = build("slides", "v1", credentials=creds)
drive_svc  = build("drive",  "v3", credentials=creds)

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

# ── 프레젠테이션 생성 ─────────────────────────────────────────
def create_presentation(title: str) -> str:
    pres = slides_svc.presentations().create(body={"title": title}).execute()
    pid  = pres["presentationId"]
    print(f"URL: https://docs.google.com/presentation/d/{pid}/edit")
    return pid

# ── 슬라이드 추가 ─────────────────────────────────────────────
def add_slide(pid: str) -> str:
    sid = f"slide_{uuid.uuid4().hex[:8]}"
    slides_svc.presentations().batchUpdate(
        presentationId=pid,
        body={"requests": [{"insertSlide": {
            "slideLayoutReference": {"predefinedLayout": "BLANK"},
            "objectId": sid,
        }}]}
    ).execute()
    return sid

# ── 슬라이드 배경색 ───────────────────────────────────────────
def set_bg(requests, slide_id, color_key: str):
    requests.append({"updatePageProperties": {
        "objectId": slide_id,
        "pageProperties": {"pageBackgroundFill": solid_fill(color_key)},
        "fields": "pageBackgroundFill"
    }})

# ── 사각형 ────────────────────────────────────────────────────
def add_rect(requests, slide_id, obj_id, x, y, w, h,
             fill=None, border=None, border_pt=0.75):
    requests.append({"createShape": {
        "objectId": obj_id, "shapeType": "RECTANGLE",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
    sp = {}
    if fill:   sp["shapeBackgroundFill"] = solid_fill(fill)
    if border: sp["outline"] = {"outlineFill": solid_fill(border),
                                 "weight": {"magnitude": border_pt, "unit": "PT"}}
    elif fill: sp["outline"] = {"outlineFill": solid_fill(fill)}
    if sp:
        requests.append({"updateShapeProperties": {
            "objectId": obj_id, "shapeProperties": sp,
            "fields": ",".join(sp.keys())}})

# ── 텍스트박스 ────────────────────────────────────────────────
def add_text(requests, slide_id, obj_id, x, y, w, h, text,
             font="Noto Sans KR", scale="bodyM", color="textMain",
             bold=False, italic=False, align="START"):
    requests.append({"createShape": {
        "objectId": obj_id, "shapeType": "TEXT_BOX",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})
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

# ── 수평선 ────────────────────────────────────────────────────
def add_line(requests, slide_id, obj_id, x, y, length,
             color="border", weight=0.75, dash="SOLID"):
    requests.append({"createLine": {
        "objectId": obj_id, "lineCategory": "STRAIGHT",
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(length, 0), "transform": pos(x, y)}}})
    requests.append({"updateLineProperties": {
        "objectId": obj_id,
        "lineProperties": {
            "lineFill": {"solidFill": {"color": {"rgbColor": C[color]}}},
            "weight": {"magnitude": weight, "unit": "PT"},
            "dashStyle": dash},
        "fields": "lineFill,weight,dashStyle"}})

# ── 이미지 ────────────────────────────────────────────────────
def add_image(requests, slide_id, obj_id, x, y, w, h, url: str):
    """공개 URL 또는 Google Drive 공유 URL"""
    requests.append({"createImage": {
        "objectId": obj_id, "url": url,
        "elementProperties": {"pageObjectId": slide_id,
            "size": size(w, h), "transform": pos(x, y)}}})

# ── batchUpdate 전송 ─────────────────────────────────────────
def send(pid: str, requests: list):
    if not requests:
        return
    slides_svc.presentations().batchUpdate(
        presentationId=pid, body={"requests": requests}
    ).execute()
    requests.clear()
```

### 11.2 환경 테스트

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file(
    "service_account.json",
    scopes=["https://www.googleapis.com/auth/presentations"]
)
svc  = build("slides", "v1", credentials=creds)
pres = svc.presentations().create(body={"title": "테스트"}).execute()
print("성공:", pres["presentationId"])
```

---

## 12. 환경 설정

### 12.1 패키지 설치

```bash
pip install google-api-python-client google-auth google-auth-oauthlib
```

### 12.2 Google Cloud 설정

```
1. console.cloud.google.com → 프로젝트 선택 또는 생성
2. API 및 서비스 → 라이브러리에서 활성화:
   - Google Slides API
   - Google Drive API
3. API 및 서비스 → 사용자 인증 정보 → 서비스 계정 만들기
4. 서비스 계정 → 키 → 새 키 추가 → JSON 다운로드
   → service_account.json 으로 저장
5. 서비스 계정 이메일을 대상 Drive 폴더에 편집자로 추가
```

### 12.3 Gemini 활용 방식

**방식 A — 로컬 실행 (권장)**
이 문서를 Gemini 컨텍스트로 제공 → 코드 생성 → `python main.py` 실행

**방식 B — Google AI Studio Code Execution**
service_account.json을 환경에 업로드 후 AI Studio에서 직접 실행

**방식 C — Google Apps Script**
Workspace 내 완결형. JavaScript 문법으로 별도 구현 필요

---

## 부록: API 주의사항

```
1. objectId는 프레젠테이션 전체에서 고유해야 함
2. requests 순서:
   createShape → updateShapeProperties
   → insertText → updateTextStyle → updateParagraphStyle
3. 색상: red/green/blue 모두 0.0~1.0 float
4. batchUpdate는 슬라이드당 1회 호출 권장
5. 슬라이드 배경: updatePageProperties (updateShapeProperties 아님)
6. 선 생성: createLine (createShape 아님)
7. Google Fonts: fontFamily 문자열로 직접 지정 가능
8. 이미지: 공개 URL 또는 Drive 공유 URL만 가능
9. Slides + Drive API 모두 활성화 필요
```
