import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_ppt():
    prs = Presentation()
    
    # Define Colors based on Design System
    PURPLE = RGBColor(0x7B, 0x3C, 0xE9)
    BLACK = RGBColor(0x1F, 0x1F, 0x1F)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    GRAY = RGBColor(0x66, 0x66, 0x66)
    LIGHT_GRAY = RGBColor(0xF3, 0xF4, 0xF6)

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_title_slide(title_text, subtitle_text):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_slide_background(slide, BLACK)
        
        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(3), Inches(9), Inches(1.5))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.bold = True
        p.font.size = Pt(44)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.LEFT
        
        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.5), Inches(9), Inches(1))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = subtitle_text
        p.font.size = Pt(20)
        p.font.color.rgb = PURPLE
        p.alignment = PP_ALIGN.LEFT

    def add_content_slide(title_text, points):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_slide_background(slide, WHITE)
        
        # Header Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.4), Inches(0.1), Inches(0.5))
        line.fill.solid()
        line.fill.fore_color.rgb = PURPLE
        line.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.3), Inches(8), Inches(0.7))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.bold = True
        p.font.size = Pt(28)
        p.font.color.rgb = BLACK
        
        # Content
        top = 1.2
        for point in points:
            if isinstance(point, str):
                box = slide.shapes.add_textbox(Inches(0.5), Inches(top), Inches(9), Inches(0.5))
                tf = box.text_frame
                p = tf.paragraphs[0]
                p.text = "• " + point
                p.font.size = Pt(18)
                p.font.color.rgb = BLACK
                top += 0.4
            elif isinstance(point, list):
                for sub in point:
                    box = slide.shapes.add_textbox(Inches(0.8), Inches(top), Inches(8.5), Inches(0.4))
                    tf = box.text_frame
                    p = tf.paragraphs[0]
                    p.text = "  - " + sub
                    p.font.size = Pt(14)
                    p.font.color.rgb = GRAY
                    top += 0.3
                top += 0.2

    # 1. Title Slide
    add_title_slide("Next-Gen AI Security Strategy", "Beyond Gateway: 에이전틱 시대를 위한 초격차 보안 거버넌스")
    
    # 2. Market Context
    add_content_slide("시장 상황: Gateway 레드오션과 신규 기회", [
        "AI Gateway 시장 포화: 단순 트래픽 제어는 이미 Commodity화",
        "Agentic Shift: 인간의 개입 없는 '자율형 에이전트' 도입 가속화",
        "보안 패러다임의 변화:",
        ["Perimeter(입구) → Behavior(행위) 중심의 보안으로 이동", "정적 룰셋 → 실시간 문맥(Context) 분석 필요성 증대"]
    ])
    
    # 3. Strategy Pillar 1: AI-DSPM
    add_content_slide("전략 Pillar 1: AI-Native DSPM", [
        "벡터 DB 및 RAG 파이프라인 데이터 보안 형상 관리",
        "핵심 기능:",
        ["임베딩 데이터 내 민감 정보(PII) 의미적 스캔", "데이터 소스와 벡터 DB 간의 접근 권한 정합성 검증", "데이터 계보(Lineage) 추적을 통한 사고 발생 시 즉시 격리"]
    ])
    
    # 4. Strategy Pillar 2: Agent-SPM (The Killer Item)
    add_content_slide("전략 Pillar 2: Agent-SPM (Killer Item)", [
        "자율형 에이전트 행동 거버넌스 및 실시간 통제",
        "핵심 차별화 포인트:",
        ["NHI(비인간 ID) 자산 관리: 에이전트별 최소 권한(PoLP) 강제", "Semantic Firewall: 에이전트의 추론 과정(CoT) 감시 및 차단", "기계 간 통신(A2A) 셧다운 시스템: 에이전트 폭주 방어"]
    ])
    
    # 5. Field Insight: Shinhan Bank
    add_content_slide("현장 인사이트: 신한은행 미팅 기반 페인포인트 해결", [
        "행정 지옥 해소: 망분리 5호 예외 지정을 위한 'PaaS 래핑' 아키텍처",
        "지능형 필터링: '공일공' 등 문맥적 우회 유출을 막는 Semantic DLP",
        "실무 효율화:",
        ["금감원/감사 대응용 보안 증적 리포트 원클릭 자동 생성", "1,000명 동시 접속 '트래픽 쓰나미' 안정적 스로틀링"]
    ])
    
    # 6. K-Compliance Strategy
    add_content_slide("한국 시장 특화 전략 (K-Compliance)", [
        "망분리 완화 로드맵 대응: 하이브리드(내부/외부) 보안 브릿지 제공",
        "혁신금융서비스 샌드박스 Accelerator:",
        ["심사 통과를 위한 보안 검증 패키지 턴키 제공", "자율보안 체계 하에서의 '결과 책임' 방어권 확보"]
    ])
    
    # 7. Competitive Edge
    add_content_slide("경쟁 우위: 왜 Agent-SPM 인가?", [
        "Gateway(외산 벤더): 트래픽 관리는 잘하나 한국 규제 및 AI 문맥 이해 부족",
        "DSPM(데이터 보안): 유출 방지는 하나 자율형 에이전트의 행위 통제 불가",
        "Agent-SPM(U+):",
        ["국내 유일의 망분리 우회 컨설팅 결합", "AI의 자율성을 통제하는 독보적 런타임 보안 기술"]
    ])
    
    # 8. Policy & Compliance Alignment
    add_content_slide("정부 가이드라인(AI 보안 안내서) 대응 전략", [
        "Anti-Poisoning: 학습 데이터 오염 및 AI 편향성 실시간 차단",
        "Edge Security: AI 로봇/에지 기기의 무단 제어 및 탈취 방어",
        "AI-Audit: 가이드라인 권고 '지속적 모니터링 및 로깅' 요건 충족",
        "Result: 정부 지침을 100% 준수하는 '가장 안전한 금융 AI 인프라'"
    ])

    # 9. CISO Persuasion Logic
    add_content_slide("보안 담당자(CISO) 설득을 위한 Key Message", [
        "Accountability: AI 사고 발생 시 '면책 근거(Safe Harbor)' 제공",
        "Enabler: 혁신의 방해자가 아닌 '안전한 혁신(AX)의 조력자'로 위상 격상",
        "Asset Protection: 데이터 유출을 넘어 '직접적 재무 손실(환각/오작동)' 방어",
        "Compliance: 행정 지옥(샌드박스/보고서)으로부터의 완전한 해방"
    ])

    # 10. Service Operation Flow
    add_content_slide("U+ Safe AI 엔드투엔드 보안 프로세스", [
        "0. AI-SPM: 인프라 및 모델 자산의 안전성 상시 점검",
        "1. Semantic DLP: 사용자 요청의 문맥 분석 및 1차 필터링",
        "2. AI-DSPM: RAG 참조 데이터의 민감 정보 마스킹 및 오염 차단",
        "3. Agent-SPM: AI의 추론 과정(CoT) 실시간 감시 및 행위 통제",
        "4. Compliance XAI: 전수 로깅 및 규제 대응 보고서 자동 생성"
    ])

    # 11. CoT Monitoring Mechanism
    add_content_slide("초격차 기술: CoT(Chain of Thought) 실시간 감시", [
        "Why: 단순 프롬프트 필터링(신분증 검사)은 '내부 행동'을 보장하지 못함",
        "Case 1: 정상 요청 속에 숨겨진 '악의적 지시(Indirect Injection)' 탐지",
        "Case 2: AI의 논리적 비약 및 환각에 의한 '규정 위반 결정' 선제 차단",
        "Mechanism: 사고 노출 -> 토큰 인터셉트 -> Shadow Reasoning 검증",
        "Result: 우회 불가능한 '증명 가능한 지능(Provable Intelligence)' 구현"
    ])

    # 12. Performance Optimization
    add_content_slide("보안과 성능의 균형: 레이턴시 최적화 전략", [
        "Async Streaming: 생성과 동시에 보안 분석을 수행하여 대기 시간 최소화",
        "Lightweight Agents: 2B 이하의 초경량 보안 모델을 통한 연산 부하 5% 미만 억제",
        "Parallel Pipeline: 데이터 조회, 정제, 분석 과정을 병렬로 처리",
        "Result: 강력한 3중 보안에도 불구하고 기존 대비 95% 이상의 성능 유지"
    ])

    # 13. Final Message
    add_content_slide("Closing: AX 전환의 신뢰 가드레일", [
        "보안은 혁신의 걸림돌이 아니라, 혁신의 속도를 높여주는 브레이크",
        "Safe AI는 기업이 마음 놓고 AI를 현업에 투입하게 만드는 마지막 퍼즐",
        "U+ Safe AI: 가장 안전한 기업용 AI 업무 환경의 표준이 되겠습니다."
    ])

    save_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/Next_Gen_AI_Security_Strategy.pptx"
    prs.save(save_path)
    print(f"✅ PPT 생성 완료: {save_path}")

if __name__ == "__main__":
    create_ppt()
