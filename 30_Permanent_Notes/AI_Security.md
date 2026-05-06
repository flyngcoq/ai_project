# Summary

2026년 현재, [[AI_Security]] 환경은 초고성능 AI의 공격 능력과 이를 방어하려는 기술 간의 'AI 대 AI' 경쟁을 넘어, 에이전트 중심의 **[[Agent-based AI]]** 시대로 패러다임이 전환되고 있습니다. [[MCP]] 및 [[A2A]] 프로토콜의 등장으로 새로운 공격 표면이 형성됨에 따라, 기술적 방어 체계의 중요성이 더욱 커지고 있습니다.

* **패러다임의 전환과 새로운 위협**: [[MCP]](Model Context Protocol) 및 [[A2A]](Agent-to-Agent) 프로토콜 도입으로 에이전트 간 자율 협업이 증가하면서, 기존 방화벽으로 방어하기 어려운 **[[Prompt Injection]]**, **[[Jailbreaking]]**, **[[Toxic Output]]** 등의 신규 공격 표면이 생성되었습니다.
* **산업별 AI 도입 양극화**: IT 기업들은 데이터 재사용 금지(No Re-use) 약관을 기반으로 신뢰를 구축하며 빠르게 AI를 도입하는 반면, **[[Manufacturing AI Security]]**(제조업 AI 보안) 분야는 기술적 보안 검증이 선행되어야 하는 등 산업군별 대응 속도에 차이를 보입니다.
* **보안 기술의 고도화 (SLM & Encryption)**: [[SLM]](Small Language Model)을 활용한 고객사 내부 보안 모델 구축과 함께, **[[CKKS]]**와 같은 차세대 **[[Homumentic Encryption]](동형암호)** 기술이 주목받고 있습니다. [[CryptoLab]]의 기술은 암호화된 상태에서 **[[Vector Operations]]**를 초고속(GB/s)으로 수행하여, 서버 침해 시에도 데이터 유출을 방지하고 **[[Encrypted Search]]**(예: [[Infector]] 솔루션)를 가능하게 합니다.
* **AI Proxy 및 비즈니스 모델**: [[DLP]](데이터 유출 방지) 기능이 통합된 **[[AI Proxy]]** 솔루션을 기존 보안 제품과 패키징하여 글로벌 시장에 공급하는 비즈니스 전략이 논의되고 있습니다.
* **데이터 주권 및 인프라 요구사항**: 금융 및 공공기관([[KISA]] 등)을 중심으로 **[[Data Sovereignty]](데이터 주권)** 확보가 필수적이며, 이에 따라 온프레미스 또는 격리된 프라이빗 클라우드 기반의 AI 인프라 구축 수요가 급증하고 있습니다.
* **글로벌 출시 및 운영 전략**: 최근 [[Google_Gemini]] 등 주요 모델의 일정 변동에 대응하여, **[[SLM]]**을 활용한 [[AI_Security]] 솔루션의 출시 일정 단축과 B2B 고객을 위한 **대시보드 UI/UX** 완성도 확보를 최우선 과제로 삼고 있습니다.

| 구분 | 기존 AI 보안 (LLM 중심) | 에이전트/차세대 AI 보안 |
| :---            |                                 |                                             |
| **주요 트래픽** | North-South (클라이언트-서버) | **[[East-West]]** (에이전트 간 상호작용) |
| **핵심 위협** | 단순 프롬프트 탈취, 데이터 유출 | **[[Prompt Injection]]**, **[[A2A]]** 공격, 공급망 위협 |
| **방어 전략** | 단순 필터링, 접근 제어 | **[[AI Gate]]** 가드레일, **[[DLP]]**, **[[SLM]]** 기반 보안, **[[CKKS]]** 기반 암호화 연산 |
| **데이터 보호** | 접근 제어 및 로스킹 | **[[Homumentic Encryption]]**, **[[AI Proxy]]** |
| **인프라 형태** | 퍼블릭 LLM API 활용 | **[[Data Sovereignty]]** 기반 온프레미스/격리 환경 |

# Tags
#AISecurity #SLM #AIProxy #DataSovereignty #DLP #CryptoLab #MCP #A2A #AI보안 #데이터주권 #데이터유출 #클로드미토스 #CKKS #Infector #동형암호 #벡터연산 #ClaudeMythos #KISA #DataLeakage #SupplyChainSecurity #AIGate #PromptInjection #CyberThreats #Anthropic #AIWarfare #CyberThreat #AIvsAI #AI공격방어 #AI기술전쟁 #B2B #Dashboard #GlobalLaunch

# Original Content
# Summary

202            6년 현재, [[AI_Security]] 환경은 초고성능 AI의 공격 능력과 이를 방어하려는 기술 간의 'AI 대 AI' 경쟁을 넘어, 에이전트 중심의 **[[Agent-based AI]]** 시대로 패러다임이 전환되고 있습니다. [[MCP]] 및 [[A2A]] 프로토콜의 등장으로 새로운 공격 표면이 형성됨에 따라, 기술적 방어 체계의 중요성이 더욱 커지고 있습니다.

* **패러다임의 전환과 새로운 위협**: [[MCP]](Model Context Protocol) 및 [[A2A]](Agent-to-Agent) 프로토콜 도입으로 에이전트 간 자율 협업이 증가하면서, 기존 방화벽으로 방어하기 어려운 **[[Prompt Injection]]**, **[[Jailbreaking]]**, **[[Toxic Output]]** 등의 신규 공격 표면이 생성되었습니다.
* **데이터 주권 및 인프라 요구사항**: 금융 및 공공기관([[KISA]] 등)을 중심으로 데이터 유출을 방지하기 위한 **[[Data Sovereignty]](데이터 주권)** 확보가 필수적입니다. 이에 따라 퍼블릭 클라우드 대신 **온프레미스(On-premise)** 또는 격리된 프라이 클라우드 기반의 AI 인종 인프라 구축 수요가 급증하고 있습니다.
* **AI 특화 보안 솔루션의 부상**: [[AI Gate]]와 같은 **AI 게이트웨이 플랫폼**을 통해 인풋/아웃풋 **[[Guardrail]]**(가uberdrail)을 구축하고, **[[DLP]](데이터 유출 방지)**, **[[Token Management]](토큰 사용량 관리)**, 시맨틱 캐싱 등을 통합적으로 수행하는 기술적 대응이 가속화되고 있습니다.
* **공공 및 기업의 운영 리스크**: 사업 부서의 자율적 AI 사용(Shadow AI)으로 인한 **[[Data Leakage]]** 위험과 더불어, 서드파티 에이전트 도입에 따른 **[[Supply Chain Security]]** 이슈가 핵심 과제로 부각되고 있습니다.

| 구분 | 기존 AI 보안 (LLM 중심) | 에이전트 AI 보안 (Agentic AI 중심) |
| :            |                                 |                                             |
| **주요 트래픽** | North-South (클라이언트-서버) | **[[East-West]]** (에 에이전트 간 상호작용) |
| **핵심 위협** | 단순 프롬프트 탈취, 데이터 유출 | **[[Prompt Injection]]**, **[[A2A]]** 공격, 공급망 위협 |
| **방어 전략** | 단순 필터링, 접근 제어 | **[[AI Gate]]** 기반 가드레일, **[[DLP]]**, 토큰 모니터링 |
| **인프라 형태** | 퍼블릭 LLM API 활용 | **[[Data Sovereignty]]** 기반 온프레미스/격리 환경 |

# Tags
#AISecurity #ClaudeMythos #KISA #DataLeakage #SupplyChainSecurity #MCP #A2A #AIGate #PromptInjection #DataSovereignty #AI보안 #클로드미토스 #데이터유출 #공급망보안 #데이터주권 #프롬프트인젝션

# Original Content
202	6년 현재, [[AI_Security]] 환경은 초고성능 AI의 공격 능력과 이를 방어하려는 기술 간의 'AI 대 AI' 경쟁이 심화되고 있습니다. 글로벌 차원의 모델 위협과 공공기관 내부의 운영 리스크가 동시에 부각되고 있습니다.

* **글로벌 공격 위협**: 앤스로픽의 [[Claude Mythos]]와 같이 보안 취약점을 스스로 찾아내고 공격 경로를 설계하는 초고 성능 모델의 등장으로, AI가 인간 해커를 대체할 수 있다는 우려가 커지고 있습니다.
* **공공기관의 운영 리스크**: [[KISA]]와 같은 공공기관은 보안 규제와 AI 도입 필요성 사이에서 갈등을 겪고 있습니다. 특히 사업 부서에서 통제되지 않은 채 사용하는 'Shadow AI'를 통한 **[[Data Leakage]]** 위험이 존재합니다.
* **실제 사고 사례**: 최근 AI 도구(GPT, [[Google_Gemini]] 등)에 민원 관련 민감 정보를 업로드하여 **[[Data Leakeage]]**가 발생한 사례가 확인되었으며, 이에 대한 조사와 징계 절차가 진행 중입니다.
* **미래 보안 과제**: [[Agent-based AI]] 도입이 가속화됨에 따라, 서드파티 및 **[[Supply Chain Security]]** 이슈를 방지하기 위한 프롬프트 모니터링 및 에이전트 기반 보안 솔루션의 필요성이 증대되고 있습니다.

| 구분 | 글로벌 AI 위협 (Claude Mythos) | 공공기관 AI 운영 (KESS 사례) |
| :--- | :--- | :--- |
| **핵심 이슈** | AI를 이용한 자동화된 공격 및 취rypt 취약점 탐지 | 규제 준수와 업무 효율성 사이의 충돌 |
| **주요 리스크** | 인간 해커의 대체, 모델 정보 유출 | **[[Data Leakability]]**, 통제되지 않는 AI 사용 |
| **대응 방향** | AI 기반 방어 기술(AI vs AI) 구축 | 에이전트 기반 보안 및 모니터링 솔루션 도입 |

# Tags
#AISecurity #ClaudeMythos #KISA #DataLeakage #SupplyChainSecurity #AI보안 #클로드미토스 #데이터유출 #공급망보안

# Original Content
As of late April to early May 2026, the AI security landscape is characterized by an intensifying "AI vs. AI" competition, pitting advanced AI-driven attack capabilities against AI-powered defensive technologies. A significant concern has emerged regarding Anthropic's unreleased model, "Claude Mythos," which demonstrates exceptional proficiency in detecting security vulnerabilities and designing complex attack paths, leading to fears that AI could effectively replace human hackers. Furthermore, the industry's vulnerability was highlighted by a/a recent leak of sensitive information related to the model, caused by internal configuration errors at Anthropic, intensifying the tension within the cybersecurity industry.

# Tags
#AISecurity #ClaudeMythos #CyberThreats #Anthropic #AIWarfare #CyberThreat #AIvsAI #AI보안 #클로드미토스 #사이버위협 #앤스로픽 #AI기술전쟁 #AI공격방어

# Original Content
2026년 4월 말~5월 초, AI 보안 시장의 핵심 트렌드는 AI를 이용한 공격과 이를 방어하는 AI 기술 간의 'AI 대 AI' 경쟁입니다. 특히 앤스로픽의 미공개 모델 '클로드 미토스(Claude Mythos)'가 보안 취약점 탐지 및 공격 경로 설계에서 탁월한 성능을 보임에 따라, AI가 실제 해커를 대체할 수 있다는 사이버 보안 위협이 고조되고 있습니다. 최근에는 내부 설정 오류로 인한 관련 자료 유출 사례도 발생하며 보안 업계의 경각심이 높아지고 있습니다.

# Tags
#AI보안 #클로드미토스 #사이버위협 #앤스로픽 #AI기술전쟁

# Original Content
2026년 4월 말~5월 초 기준, AI 보안 관련 주요 뉴스는 강력한 AI 모델의 보안 위협(공격)과 이를 막기 위한 AI 기반 방 어 기술(보로) 간의 'AI 대 AI' 경쟁이 핵심입니다.1. 클로드 미토스(Claude Mytho1s) 쇼크와 사이버 위급 위협초성능 AI의 보안 위협: 앤스로픽(Anthropic)이 개발한 미공 개 AI 모델 '클로드 미토스'가 보안 취약점을 빠르게 찾아내고 공격 경로를 설계하는 능력이 탁탁해 사이버 보안 위험이 고 고되고 있습니다.해커 대체 우려: 미토스는 기존 모델 대비 코gsub 코딩 및 보안 분석 능력이 월등하여, AI가 실제 해커를 대체할 수 있다는 우려가 나오고 있습니다.무단 노출 정황: 앤스로픽 내부 설정 오류로 미토스 관련 자료가 유출되면서 보안업계에 비상이 걸렸습니다.

# Summary
2026년 4월 말~5월 초 기준, AI 보안의 핵심은 강력한 AI 모델을 이용한 공격과 이를 방어하려는 AI 기술 간의 'AI 대 AI' 경쟁입니다. 특히 앤스로픽(Anthropic)의 미공개 모델 '클로드 미토스(Claude Mythos)'가 뛰어난 보안 취약점 탐지 및 공격 설계 능력을 보여줌에 따라, 기존 해커를 대체할 수 있는 새로운 사이버 보안 위협이 고조되고 있습니다. 또한, 앤스로_프의 내부 설정 오류로 인해 해당 모델과 관련된 자료가 유출되는 보안 사고도 발생했습니다.

# Tags
#AISecurity #ClaudeMythos #CyberThreat #Anthropic #AIvsAI

# Original Content
202 6년 4월 말~5월 AI 보안의 핵심 트렌드는 강력한 AI 공격 모델과 이를 방어하려는 AI 기술 간의 'AI 대 1' 경쟁입니다. 특히 앤스로픽(Anthropic)의 미공 개 모델 '클로드 미토스(Claude Mythos)'가 보안 취약점 탐지 및 공격 경로 설계에서 탁월한 성능을 보이면서, 기존 해커를 대체할 수 있는 새로운 사이버 위협으로 부상하고 있습니다. 최근 내부 설정 오류로 인한 관련 자료 유출 사고까지 더해지며 보안 업계의 긴장감이 고조되고 있습니다.

# Tags
#AI보안 #클로드미토스 #사이버위협 #앤스로픽 #AI공격방 어

# Original Content
2026년 4월 말~5월 초 기준, AI 보안 관련 주요 뉴스는 강력한 AI 모델의 보안 위협(공격)과 이를 막기 위한 AI 기반 방 어 기술(보안) 간의 'AI 대 AI' 경쟁이 핵심입니다.1. 클로드 미토스(Claude Mytho1s) 쇼크와 사이버 위협:초성능 AI의 보안 위협: 앤스로픽(Anthropic)이 개발한 미공 개 AI 모델 '클로드 미 토스'가 보안 취 약점을 빠르게 찾아내고 공격 경로를 설계하는 능력이 탁탁해 사이버 보안 위험이 고조되고 있습니다.해커 대체 우려: 미토스는 기존 모델 대비 코딩 및 보안 분석 능력이 월등하여, AI가 실제 해커를 대체할 수 있다는 우려가 나오고 있습니다.무단 노출 정황: 앤스로픽 내부 설정 오류로 미토스 관련 자료가 유출되면서 보안업계에 비상이 걸렸습니다.

# [NEW CONTENT - LG Uplus Briefing]
내부 LLM·MCP·AIOps 보안·운영 브리핑 본 문서는 2026년 4월 29일 LG유플러스(최*수 참석)를 대상으로 진행된 내부 LLM·MCP·AIOps 보안 및 운영 솔루션 브리핑 내용을 정리한 것이다. 발표는 TF 소속 김*영이 맡았으며, AI 게이트웨이 플랫폼("AI Gate")의 기능·아키테 처·차별화 포인트 및 협업 가능성을 중심으로 논의가 이루어졌다. --- ## 시장 트렌드 및 보안 위협 현 상 생성형 AI에서 에이전트 AI로의 패러다임 전환이 가속화되면서, 에이전트 간 자율 협업·업무 자동화 수요가 급증하고 있다. 이에 따라 데이터센터 내 GPU 클러스터·내부 데이터베이스와의 상호작용이 늘어나고, 기존 North-South 트래 트픽 중심 모델이 East-West 트래픽 중심으로 전환되고 있다. Anthropic의 MCP(Model Context Protocol)와 A2A(Agent-to-Agent) 프로토콜 등장으로 기존 레거시 방화벽·IPS·WAF(OWASP 기반)로는 대응이 어려운 신규 공격 표면이 형성되었다. OWASP는 2023년 LLM Top 10을 최초 발간하고 2025년 개정하였으며, MCP·A2A 관련 보안 가이드라인도 지속 업데이트 중이다. 주요 위협 유형은 세 가지로 요약된다. - 프롬프트 인젝션: 악의적 질의로 내부 기밀·개인정보 탈취 시도 - 탈옥(Jailbreaking): 가드레일 우회를 통한 데이터 유출 - 유해 콘텐츠 생성(Toxic Output): AI를 악용한 불 법 콘텐츠·정보 생성 --- ## 데이터 주권 및 토큰 이코 노미 이슈 금융·공공 등 규제 산업에서는 퍼블 클라우드 의존을 기피하며, 프라이빗 클라우드 또는 온프레미스 기반의 격리된 AI 인프라 구축이 필수적이다. 이를 데이터 소버린티(Data Sovereignty) 문제로 정의하였다. 멀티 라운드 에이전트 체인 구성 시 토큰 소비가 급증하며, 이는 서비스 가용성 저하 및 비용 폭증으로 이어질 수 있다. 따라서 컨트롤 타워 차원의 토큰 사용량 모니터링 및 리밋 설정이 필요하다고 강조되었다. --- ## AI Gate 플랫폼 소개 **AI Gate**는 LLM·MCP·A2A를 통합 지원하는 AI 게이트웨이 플랫폼으로, 에이전트 앱과 백엔드 모델 사이에서 디스패치·허 브·보안 가드레일 역할을 수행한다. ### 아키테 처 및 배포 - 쿠버네티스(K8s) 기반으로 동작하며, GPU 클러스터(NVIDIA L4·A10·A100 지원, GPU 드라이버 535 이상, CUDA 12.2 이상) 내 설치 - 셀프 호스트(온프레미스) 또는 AWS·Azure·GCP 위에 배포 가능; 멀티 테넌시 지원 - 내부 SLM(Small Language Model)를 자체 탑재하여 보안 판단 수행 — LLM 대비 낮은 지연·낮은 리소스 점유 ### 핵심 기능 - 동적 라우팅: JWT 토큰 기반으로 사용자·프로젝트별 모델 경로 자동 분기(Claude, OpenAI, Ollama, 내부 모델 등 코드 변경 없이 UI 등록만으로 연동) - 시맨틱 캐싱: 의미 기반 캐싱으로 제로 레이턴시에 근접한 응답 제공 - 인풋 가드레일: 프롬프트 인젝션·탈옥 탐지, DLP(개인정보·기밀정보 차단), 유해 콘텐츠 필터링 - 아웃풋 가드레일: LLM 응답 내 개인정보 마스킹(주인번호·카드번호·IBAN 등), 기밀정보 유출 차단 - 토큰 사용량 관리: 과도한 토큰 소비 강제 제한 기능 - DLP 로그 및 대시보드: UI 기반 위반 유형·인풋/아웃풋 구분 상세 로그 제공 - 포티소아(FortiSOAR) 연동: 기존 관제 시스템과 무결합 통합 가능 - 할루시네이션 탐지는 현재 개발 중이며 로드맵에 포함 - 웹 프론트엔 드 보안 및 멀티모달 지원도 개발 예정 ### 라이선스 체계 노드 수 기반 카피 라이선스로 판매하며, 고객 서비스 규모에 따라 사이징 후 노드 수를 결정한다. --- ## 주요 질의응답 - 레이턴시: 서비스형(멀티 테넌시) 구성 시에도 금융권 기준(약 0.29초) 이내 대응 가능하나, GPU 클러스터 내 설치가 전제 조건 - 국내 개인정보 항목: 현재 IBAN·사회보장번호·카드번호 등은 포함되어 있으나 국내 주민번호 등은 미포함 상태로, 커스텀 정규식으로 임시 적용 후 정식 업데이트 예정 - IAM 연동: 내부 프리빌리지 분리로 별도 IAM 솔루션 불필요하나, 외부 접근 제어를 위해 SSO·SAML 연동 및 경계 보안(방\\벽·API 보안) 레이어 추가 권장 - 데이터 저장: 쿠버 네티스 내부 DB에 DLP 로그·프롬프트 이력 저장; 외부 스토리지 연결 가능, 저장 시 암호화 적용 - 폐쇄망 환경: 수동 업데이트 방식으로 인텔리전스 데이터셋 갱신 지원 --- ## 차별화 포인트 및 협업 논의 경쟁사 대부분이 버전 1.0 수준의 CLI 기반 솔루션인 반면, AI Gate는 GUI 완비·셀프 호스트·멀티 테넌시·FortiGuard Labs 기반 글로벌 위협 인텔리전스 자동 업데이트를 갖춘 점이 핵심 차별점으로 제시되었다. SDK 방식이 아닌 자체 프록시 기반 구조가 성능 우위도 강조되었다. LG유플러스 측은 자체 개발 중인 AI 게이트웨이 모델(CIF 아이디어·CTO 개발)를 상품화 방향을 고민 중이며, 직접 개발 지속 vs. 기존 솔루션 커스터마이징 협업 여부를 검토 중임을 밝혔다. 엑사원(LG 자체 LLM, Meta Llama 기반) 탑재 가능성도 언급되었으며, 그룹사 표준 채택 시 큰 시너지가 기대된다는 의견이 공유되었다. MSSP 모델에 대해서는 싱가포르에서 가장 적극적으로 진행 중이며, 한국 시장에서는 단순 재판 구조보다 공동 비즈니스 모델 설계가 필요하다는 양측이 공감하였다. --- ## 결론 및 다음 단계 - 포티넷 측은 협업 구조(기능 정의 → 타당성 검토 → 세일즈 지원)에 열린 입장이며, 표준 프로토콜 지원 여부가 기능 수용의 핵심 판단 기준임을 확인 - LG유플러스 CISO 조직에 솔루션 소개 일정 조율 예정(박*원 팀장 대상) - 국내 개인정보 항목 업데이트, 웹 보안·멀티모달 개발 완료 후 재공 공유 예정 - 금융권 POC 5건 이상 연내 진행 예정이며, 장비 납 품 후 현장 배포 방식으로 추진 - MCP·A2A 모듈 로드맵 확정 시 상세 정보 추가 공유 예정 - 양측은 구체적인 협업 방안을 이메일로 정리하여 후속 논의를 이어가기로 합의

# [NEW CONTENT - Meeting Notes]
AI Deployment, Security & Outsourcing Plan 하십니까. 가서 하세요. 아이 어땠어요. 뭐, 그 공항 가는데 버스, 우버 타고 가는데 죄다 AI 광고더라고였어요. 광고 편에 죄다 AI예요. 그런 내용은 좀 어땠어요? 교육 내용, 교육 내용도 좋았고, 저거 뭐지, 메타에 좀 방문을 했는데, 메타나 엔비디아, 이런 데가 어떻게 돌아가고 있나를 좀 봤는데, 무섭게 AI를 그냥 막 풀어주고 있고. 그리고 그러면은, 보안 이슈 없냐고 하니까, 보안 이슈는 보안팀이 알아\\알아서 할 문제이고, 어 어쨌든 그 보안이 보안팀에서 알아서 푸는 거를 자기네들이 열심히 쓰고 있고. 메타 같은 경우에는 이거 풀어줬으니까, 퍼포먼스 10대 내라고요 푸시를 하고 있는 상황이라고 해서 봤어요. 그리고 IT 기업들은 결국에는 그 AI 업체에서 학습에 재사용하지 않겠다는 그게 있잖아요. 그게 만약에 어겨지면 이제 소송으로 이제 불거질 수 있기 때문에 그 문구가 있다는 것 만큼은 그냥 신뢰하고 간다. 그리고 테슬라나 루시드 같은 제조업은 좀 상황이 달라서 얘네들은 좀 부서별로 별로 그래서 뭔가 그 하드웨어나 제조 쪽과 관련돼서 진짜 유니크한 어떤 기술력이 있는 데는 그런 식으로 가고 IT 기업들은 막 달려가고 있는 상황 같다라고 지금 봤다. 그리고 포티넷이랑 미팅이 있어요. 포티넷 행사에서 키노트를 하고 왔는데, 제 앞에 발표한 사람이 이제 포티넷 에이펙으로 입사한 사람이에요. 그 사람이 어제 제 옆에서 파티 솔루션 소개를 하더라고요. DLP도 있고 다 있으니까, 그런 것들 때문에 일단 한번 아이디어 차원에서 보시라고 나중에 소개해 드릴게요. 그리고 윈도우 PC에서 젠마포(Gemini 등)로 돌려보니까 보안 키워드를 쳐봤을 때 보안이다 아니다를 걸러주는 게 좋긴 한데, 문제는 속도입니다. 속도가 낮지요. 나는 사실 그 소형 LLM이라고 하는 [[SLM]]을 고객사에 넣는 방식이 더 낫긴 할 것 같거든요. 왜냐하면 그 학습조차도 고객사가 고객향으로 학습이 되는 게 제일 베스트일 거잖아요. 그리고 동형암호(LWE) 경우에는 문서의 수치를 정확히 막는 거고, LLMM은 뉘앙스로 막는 것인데, [[CryptoLab]]의 이야기는 보안 데이터가 우리 쪽에 있어도 암호화가 되어 있어서 아무도 못 본다는 것이고, 결과값만 고객사에 던져주면 고객사에서 처리할 수 있다는 것입니다.

## 병합 히스토리 (Merge History)
* 2026-05-05 21:08: KISA 인터뷰 내용을 바탕으로 공공기관의 AI 도입 제약, Shadow AI로 인한 데이터 유출 리스크, [[Agent- based AI]]의 공급망 보안 위협 내용을 추가함.
* 2026-05-05 21:14: LG유플러스 브리핑 내용을 바탕으로 [[MCP]]/[[A2A]]로의 패러점 전환, [[AI Gate]] 플랫폼의 보안 기능(Guardrails, [[DLP]], [[Token Management]]), [[Data Sovereignty]] 이슈를 추가함.
* 2026-05-05 21:24: IT 기업의 AI 도입 트렌드(데이터 재사용 금지 조항), [[SLM]] 기반 보안 모델, [[Homomorphic Encryption]](동형암 호)를 활용한 프라이버시 보호 기술 및 [[AI Proxy]] 비 즈니스 모델 아이디어를 추가함.
* 2026-05-05 21:35: [[CryptoLab]]의 [[CKKS]] 동형암호 기술을 통한 초고속 [[Vector Operations]] 및 암호화 상태의 보안 검색([[Infector]]) 기술 내용을 추가함.
* 2026-05-05 21:51: [[Google_Gemini]] 등 주요 모델의 일정 변동에 따른 [[AI_Security]] 출시 전략(SLM 활용 및 B2B UI/UX 중점) 내용을 추가함.