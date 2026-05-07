import re

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/40_Projects/Work/Safe_AI/Design_Thinking_Report_Script.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Time Table
content = re.sub(
    r"## ⏱️ 1\. \[1시간 세션\] 시간 배분 계획 \(Time Table\).*?---",
    """## ⏱️ 1. [1시간 세션] 시간 배분 계획 (Time Table)

*   **00'~10' (10분):** [Empathize] 출장 개요 및 현장에서 마주한 '날것의 고객'
*   **10'~25' (15분):** [Define] MZ 인터뷰의 배신과 '세분화(Segmentation)'의 발견 ⭐️ (Highlight)
*   **25'~40' (15분):** [Ideate & Prototype] Safe AI의 3B 기술 전략과 B2B 구독형 비즈니스 모델 💎
*   **40'~50' (10분):** [Test] 진심과 맥락의 소통을 통한 가설 검증 (Q&A)
*   **50'~60' (10분):** **Closing & 경영진 스폰서십 요청 (Call to Action)** 🚀

---""",
    content,
    flags=re.DOTALL
)

# Replace Part 2 (MZ 인터뷰)
content = re.sub(
    r"## 🗣️ 3\. 발표 스크립트: \[Part 2\. MZ 인터뷰 & 페르소나의 해체\].*?---",
    """## 🗣️ 3. 발표 스크립트: [Empathize & Define] MZ 인터뷰 & 페르소나의 해체
*(발표의 중반부, 가장 에너지가 높고 청중의 이목이 집중될 때 아래 스크립트를 활용합니다.)*

> "여러분, 이번 출장에서 저희가 가장 먼저 한 일은 타겟 고객에게 다가가 깊이 **공감(Empathize)**하는 것이었습니다. 바로 현지 MZ 세대들을 대상으로 진행한 프로토타입 심층 인터뷰였습니다.
>
> 우리는 흔히 '디지털 네이티브니까 AI에 거부감이 없을 거야'라는 은연중의 가설을 가집니다. 하지만 실제 인터뷰 결과는 달랐습니다. 그들은 대기업이 만든 매끄러운 가짜 완벽함보다, 날것 그대로의 '진정성(Authenticity)'을 갈망했습니다. 꾸밈없는 'BeReal'에 열광하고, 소소한 일상을 나누는 '마이크로셰어'에 반응했죠.
>
> 무엇보다 보안과 프라이버시에 대해 **정반대의 양극단**이 존재했습니다."

*(화면 전환: 슬라이드에 극단적으로 대비되는 두 사용자의 멘트 띄움)*

*   🛡️ **User A (The Protector):** "어느 한 기업이 내 인생의 모든 것을 아는 건 소름 끼쳐요. 완벽한 프라이버시가 최우선입니다."
*   ⚡️ **User B (The Optimizer):** "보안은 회사 책임이죠. AI가 내 메일을 대신 써준다면, 내 비밀번호라도 공유할 용의가 있습니다."

> "보셨습니까? 같은 세대 안에서도 가치관이 180도 다릅니다. 이 지점에서 우리는 문제를 새롭게 **정의(Define)**해야 했습니다.
> 
> CEO님께서 항상 강조하셨던 말씀이 있습니다. **'고객을 이해하기 가장 좋은 방법은 세분화이며, 그 세그먼트만의 숨은 니즈와 페인포인트가 보인다.'**
> 
> 뭉뚱그려진 평균적인 페르소나를 버리고, 이처럼 극단적인 사용자(Extreme User)로 **세그먼트를 잘게 쪼개어 깊게 파고드는 것(Segment deep)**. 그것이 우리가 발견한 첫 번째 해답입니다."

---""",
    content,
    flags=re.DOTALL
)

# Replace Part 3 (Safe AI가 그릴 미래)
content = re.sub(
    r"## 🪞 3\. \[Self-Reflection & Business Value\] Safe AI가 그릴 미래.*?## 🤝 4\. \[Closing\] 경영진 스폰서십 요청 \(Call to Action\)",
    """## 🪞 4. [Ideate & Prototype] Safe AI가 그릴 미래와 3B 전략

*(이전의 충격을 내부의 문제로 자연스럽게 연결하며, 우리 서비스가 가진 폭발적인 매력도와 시장성을 강력하게 어필합니다.)*

> "세분화된 페르소나를 바탕으로, 저희는 해결책을 **도출(Ideate)**하고 파일럿을 **프로토타입(Prototype)**으로 만들어내고 있습니다.
> 
> 사용자마다 보안 감수성이 다르다면, 답은 하나입니다. 사용자에게 **'개인화된 보안 통제권'**을 쥐어주는 것입니다. 
> CEO님께서 말씀하신 **풀(Pull) 마케팅의 토대**가 바로 여기에 있습니다. 이 작은, 그러나 명확한 니즈를 가진 세그먼트에서 먼저 1등을 하고 성공 경험을 확산하는 전략입니다. (Pull, Promoter, Partnership의 3P 마케팅)
>
> 이 아이디어를 현실로 만들기 위해, 저희는 기술 스택을 **3B (Buy, Borrow, Build)** 관점으로 안목 있게 확보하고 있습니다. 모든 것을 직접 만들려 고집하지 않고, 최고의 외부 기술을 유연하게 빌리거나 사들여 우리만의 강력한 솔루션으로 결합하는 것이죠.
> 
> 이를 통해 Safe AI는 궁극적으로 **B2B 통신 인접 영역에서 자산 효율성이 매우 높은, 고부가가치 구독형 사업모델**로 자리 잡을 것입니다."

## 🤝 5. [Test & Closing] 경영진 스폰서십 요청 (Call to Action)""",
    content,
    flags=re.DOTALL
)

# Replace Closing
content = re.sub(
    r"## 🤝 5\. \[Test & Closing\] 경영진 스폰서십 요청 \(Call to Action\).*?---",
    """## 🤝 5. [Test & Closing] 경영진 스폰서십 요청 (Call to Action)

*(발표의 대미를 장식하는 섹션입니다. 바텀업 프로젝트의 한계를 돌파하기 위해, 경영진의 확신과 지원을 이끌어내는 승부수입니다.)*

> "지금까지 말씀드린 U+Safe AI 프로젝트는 실무진들의 치열한 고민에서 시작된 바텀업 이니셔티브입니다. 
> 
> 디자인씽킹의 마지막 단계는 끊임없는 **검증(Test)**입니다. 저희는 진심과 맥락에 기반한 소통으로 고객의 피드백을 수용하고 계속해서 제품을 개선해 나갈 것입니다.
> 
> 이 여정에서 저희에게 가장 필요한 것은 경영진의 강력한 스폰서십입니다. 특히 회사의 핵심 가치인 **TRUST**가 저희 팀의 심장과도 같습니다.
> 
> *   **U**nited Around the hardest challengers: 가장 어려운 문제에 맞서 하나로 뭉치고,
> *   **S**egment deep, act smart: 세그먼트를 깊게 파고들어 영리하게 행동하며,
> *   **T**hrive on Trust: 경영진의 신뢰를 바탕으로 성장하고 싶습니다.
> 
> 저희가 작은 세그먼트에서 첫 번째 성공 경험을 확실히 만들어낼 수 있도록, 길을 열어주시고 든든한 방패가 되어 주십시오. 
> 
> 우리가 함께 만든 Safe AI가 반드시 시장의 게임 체인저가 될 것이라 확신합니다. 감사합니다."


---""",
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
