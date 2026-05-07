import re

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/40_Projects/Work/Safe_AI/Design_Thinking_Report_Script.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Team Intro
content = content.replace(
    "(이 자리에 팀원들 소개자료)",
    "*(슬라이드 전환: 썸띵 바이브 팀원들의 역할과 유쾌한 사진이 담긴 소개 장표 띄움)*\n\n> \"저희 팀원들입니다. 각자의 자리에서 치열하게 기획하고, 디자인하고, 코딩하며 이 썸띵 바이브를 만들어가고 있습니다.\""
)

# 2. Education Process
content = content.replace(
    "문샷을 배우고 MZ의 고민을 해결해주는 서비스를 기획하고 등등 교육 과정을 서술...하는 영역(Enpathize -> Define -> ideate -> prototype(claude code 기반) -> Test)",
    "> \"실리콘밸리에서 저희는 10%의 개선이 아닌 10배의 혁신을 추구하는 **'문샷 씽킹(Moonshot Thinking)'**을 배웠습니다. 이를 바탕으로 MZ세대의 진짜 고민을 해결하는 서비스를 기획하기 위해, 5단계의 디자인씽킹 사이클을 쉼 없이 돌렸습니다. \n> \n> 고객의 삶에 깊이 들어가 **공감(Empathize)**하고, 진짜 문제를 **정의(Define)**한 후, 팀원들과 밤을 새워가며 아이디어를 **도출(Ideate)**했습니다. 그리고 U+Safe AI 환경에서 Claude 코드를 활용해 단 며칠 만에 작동하는 **프로토타입(Prototype)**을 만들어, 스탠포드 현지 학생들에게 직접 부딪히며 **검증(Test)**을 받았습니다.\""
)

# 3. Social Relationship Extremes
content = content.replace(
    "*   🛡️ **User A (The ????):** \"너무 바쁘지만 인간관계도 놓칠 수 없어서 열심히 약속을 잡는다.... 2주치 약속이 잡혀 있다.\"\n*   ⚡️ **User B (The ????):** \"약속을 잡고 누군가를 만나는 과정이 너무 어렵다. 혼자 있는 시간에 비디오 게임을 하지만 외롭다.\"",
    "*   🗓️ **User A (The Over-connector, 과연결자):** \"너무 바쁘지만 인간관계도 절대 놓칠 수 없어요. 사람들을 만나기 위해 열심히 약속을 잡다 보니 이미 2주 치 일정이 꽉 차 있습니다.\"\n*   🎮 **User B (The Hesitant Loner, 고립된 관찰자):** \"먼저 약속을 잡고 누군가를 만나는 과정 자체가 너무 어렵고 에너지가 듭니다. 혼자 있는 시간에 주로 비디오 게임을 하지만, 사실 속으로는 외로워요.\""
)

# 4. Connecting Social Relationship to U+Safe AI
old_part_3 = """> "세분화된 페르소나를 바탕으로, 저희는 해결책을 **도출(Ideate)**하고 파일럿을 **프로토타입(Prototype)**으로 만들어내고 있습니다.
> 
> 사용자마다 보안 감수성이 다르다면, 답은 하나입니다. 사용자에게 **'개인화된 보안 통제권'**을 쥐어주는 것입니다. 
> CEO님께서 말씀하신 **풀(Pull) 마케팅의 토대**가 바로 여기에 있습니다. 이 작은, 그러나 명확한 니즈를 가진 세그먼트에서 먼저 1등을 하고 성공 경험을 확산하는 전략입니다. (Pull, Promoter, Partnership의 3P 마케팅)"""

new_part_3 = """> "세분화된 페르소나를 바탕으로, 저희는 해결책을 **도출(Ideate)**하고 파일럿을 **프로토타입(Prototype)**으로 만들어내고 있습니다.
> 
> 사용자마다 '관계 형성(Social Relationship)'에 대한 니즈가 극명하게 다르다면, 우리는 이 극단적인 세그먼트 각각에 맞는 '개인화된 맞춤형 서비스'를 기획해야 합니다. 
> 하지만 현업에서 이런 혁신적인 아이디어를 시도할 때마다, 우리는 항상 '보안'이라는 거대한 장벽에 부딪혀 좌절하곤 했습니다.
> 
> 그래서 우리가 만들고 있는 **'U+Safe AI'**가 중요합니다. 기획자와 개발자가 보안 걱정 없이, 마음껏 바이브(기획/개발)를 발산하며 타겟 고객에게 의미 있는 '썸띵'을 가장 빠르게 던져볼 수 있는(Prototype & Test) 강력한 환경을 제공하기 때문입니다.
> 
> CEO님께서 말씀하신 **풀(Pull) 마케팅의 토대**가 바로 여기에 있습니다. U+Safe AI를 통해 작고 뾰족한 세그먼트(예: 극단적 보안 주의자, 특정 사내 부서 등)의 문제를 먼저 완벽히 해결하여 1등을 하고, 그 성공 경험을 전사로 확산하는 전략입니다. (Pull, Promoter, Partnership의 3P 마케팅)"""

content = content.replace(old_part_3, new_part_3)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

