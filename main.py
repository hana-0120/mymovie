import streamlit as st

# ---------------------------------------------------------
# 페이지 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# MBTI별 추천 정보
# ※ MBTI는 진로 탐색의 참고 자료이며, 직업 적합성을 단정하지 않습니다.
# ---------------------------------------------------------
MBTI_DATA = {
    "ISTJ": {
        "nickname": "꼼꼼한 현실주의자",
        "emoji": "📘",
        "color": "#4F46E5",
        "description": "책임감이 강하고 정해진 기준과 절차에 따라 정확하게 일하는 데 강점이 있어요.",
        "strengths": ["체계적인 계획", "높은 책임감", "정확한 자료 관리"],
        "work_style": "업무 기준이 분명하고, 결과를 차근차근 확인할 수 있는 환경",
        "jobs": [
            ("회계사", "숫자와 자료를 꼼꼼하게 분석해 재무 정보를 관리해요.", "수학·경제"),
            ("공무원", "정해진 절차에 따라 공공서비스와 행정 업무를 수행해요.", "사회·행정"),
            ("데이터 관리자", "데이터를 정확하게 정리하고 안전하게 관리해요.", "정보·데이터"),
            ("품질관리 전문가", "제품과 서비스가 기준에 맞는지 점검하고 개선해요.", "공학·산업"),
        ],
    },
    "ISFJ": {
        "nickname": "따뜻한 수호자",
        "emoji": "🌿",
        "color": "#0F766E",
        "description": "상대의 필요를 세심하게 살피고 맡은 일을 성실하게 끝까지 수행하는 편이에요.",
        "strengths": ["세심한 배려", "꾸준한 실행", "협력과 지원"],
        "work_style": "사람을 직접 돕고 안정적으로 협력할 수 있는 환경",
        "jobs": [
            ("간호사", "환자의 상태를 살피고 치료와 회복을 지원해요.", "보건·의료"),
            ("초등교사", "학생의 성장 과정을 가까이에서 돕고 지도해요.", "교육"),
            ("사회복지사", "도움이 필요한 사람에게 상담과 복지 서비스를 연결해요.", "복지·상담"),
            ("도서관 사서", "자료를 체계적으로 관리하고 이용자의 정보 탐색을 도와요.", "문헌·정보"),
        ],
    },
    "INFJ": {
        "nickname": "통찰력 있는 조언자",
        "emoji": "🔮",
        "color": "#7C3AED",
        "description": "사람의 마음과 사회의 의미를 깊이 생각하며 가치 있는 변화를 만들고 싶어 해요.",
        "strengths": ["깊은 공감", "장기적 통찰", "의미 중심 사고"],
        "work_style": "사람의 성장이나 사회적 가치에 기여할 수 있는 환경",
        "jobs": [
            ("상담심리사", "대화를 통해 고민을 이해하고 심리적 성장을 도와요.", "심리·상담"),
            ("작가", "생각과 감정을 글로 표현해 독자에게 메시지를 전해요.", "문학·창작"),
            ("교육기획자", "학습자의 성장을 위한 프로그램과 콘텐츠를 설계해요.", "교육·기획"),
            ("사회혁신가", "사회문제를 발견하고 지속 가능한 해결책을 만들어요.", "사회·창업"),
        ],
    },
    "INTJ": {
        "nickname": "전략적인 설계자",
        "emoji": "♟️",
        "color": "#334155",
        "description": "복잡한 문제의 구조를 파악하고 장기적인 전략을 세우는 데 강점이 있어요.",
        "strengths": ["논리적 분석", "전략 설계", "독립적 문제 해결"],
        "work_style": "전문성을 발휘하며 복잡한 문제를 깊이 탐구할 수 있는 환경",
        "jobs": [
            ("인공지능 연구원", "데이터와 알고리즘을 활용해 새로운 AI 기술을 연구해요.", "정보·AI"),
            ("소프트웨어 설계자", "복잡한 프로그램의 구조와 작동 방식을 설계해요.", "컴퓨터공학"),
            ("전략 컨설턴트", "조직의 문제를 분석하고 실행 가능한 전략을 제안해요.", "경영·전략"),
            ("과학 연구원", "가설을 세우고 실험과 분석으로 새로운 지식을 발견해요.", "과학·연구"),
        ],
    },
    "ISTP": {
        "nickname": "침착한 문제 해결사",
        "emoji": "🛠️",
        "color": "#0369A1",
        "description": "도구와 원리를 직접 다루며 문제가 생겼을 때 빠르게 원인을 찾아 해결하는 편이에요.",
        "strengths": ["실전 문제 해결", "도구 활용", "위기 대응"],
        "work_style": "직접 만들고 시험하며 결과를 바로 확인할 수 있는 환경",
        "jobs": [
            ("기계공학자", "기계와 장치의 원리를 분석하고 새로운 제품을 설계해요.", "기계·공학"),
            ("항공정비사", "항공기의 상태를 점검하고 안전하게 정비해요.", "항공·정비"),
            ("보안 전문가", "시스템의 약점을 찾아 사이버 공격을 예방해요.", "정보보안"),
            ("응급구조사", "긴급 상황에서 환자의 상태를 판단하고 응급처치를 해요.", "보건·안전"),
        ],
    },
    "ISFP": {
        "nickname": "감각적인 예술가",
        "emoji": "🎨",
        "color": "#DB2777",
        "description": "자신만의 감각을 중요하게 여기고, 사람과 환경을 세심하게 관찰하는 편이에요.",
        "strengths": ["미적 감각", "유연한 적응", "세심한 관찰"],
        "work_style": "자율적으로 표현하고 실제 결과물을 만들 수 있는 환경",
        "jobs": [
            ("그래픽 디자이너", "이미지와 글자를 조합해 효과적인 시각물을 만들어요.", "디자인"),
            ("패션 디자이너", "색과 소재를 활용해 의상과 패션 제품을 기획해요.", "패션·예술"),
            ("반려동물 전문가", "동물의 건강과 행동을 관찰하고 돌봐요.", "동물·생명"),
            ("푸드 스타일리스트", "음식이 매력적으로 보이도록 구성하고 연출해요.", "식품·콘텐츠"),
        ],
    },
    "INFP": {
        "nickname": "상상력 있는 중재자",
        "emoji": "🌙",
        "color": "#9333EA",
        "description": "자신의 가치와 개성을 중요하게 여기며 창의적인 방식으로 사람의 마음을 움직여요.",
        "strengths": ["창의적 상상력", "가치 중심 판단", "섬세한 표현"],
        "work_style": "개성과 가치관을 존중받으며 창작과 소통을 할 수 있는 환경",
        "jobs": [
            ("콘텐츠 작가", "영상, 웹툰, 광고 등에 필요한 이야기와 문장을 만들어요.", "미디어·창작"),
            ("웹툰 작가", "그림과 이야기로 자신만의 세계를 표현해요.", "예술·콘텐츠"),
            ("심리상담사", "상대의 감정과 고민을 이해하고 회복을 도와요.", "심리·상담"),
            ("환경 활동가", "환경문제를 알리고 더 나은 변화를 위한 활동을 기획해요.", "환경·사회"),
        ],
    },
    "INTP": {
        "nickname": "호기심 많은 논리학자",
        "emoji": "🧩",
        "color": "#2563EB",
        "description": "왜 그런지 원리를 파고들며 새로운 아이디어와 해결 방법을 탐구하는 것을 좋아해요.",
        "strengths": ["논리적 탐구", "아이디어 확장", "복잡한 문제 분석"],
        "work_style": "호기심을 바탕으로 자유롭게 연구하고 실험할 수 있는 환경",
        "jobs": [
            ("데이터 과학자", "많은 데이터에서 의미 있는 패턴과 정보를 찾아요.", "데이터·통계"),
            ("게임 개발자", "프로그래밍과 아이디어를 결합해 게임을 만들어요.", "게임·정보"),
            ("물리학자", "자연 현상의 원리를 수학과 실험으로 탐구해요.", "물리·연구"),
            ("UX 연구원", "사용자의 행동을 분석해 더 편리한 제품을 설계하도록 도와요.", "디자인·연구"),
        ],
    },
    "ESTP": {
        "nickname": "에너지 넘치는 도전자",
        "emoji": "⚡",
        "color": "#EA580C",
        "description": "변화가 빠른 상황에서 즉시 판단하고 사람들과 활발하게 소통하는 데 강점이 있어요.",
        "strengths": ["빠른 판단", "현장 대응", "적극적인 소통"],
        "work_style": "활동적이고 변화가 많으며 즉각적인 성과를 확인할 수 있는 환경",
        "jobs": [
            ("스포츠 마케터", "스포츠 콘텐츠와 행사를 활용해 브랜드를 홍보해요.", "스포츠·마케팅"),
            ("소방관", "재난 현장에서 사람을 구조하고 안전을 지켜요.", "안전·공공"),
            ("방송 리포터", "현장의 정보를 빠르게 취재해 시청자에게 전달해요.", "방송·언론"),
            ("창업가", "새로운 아이디어를 빠르게 실행해 사업 기회를 만들어요.", "경영·창업"),
        ],
    },
    "ESFP": {
        "nickname": "분위기를 밝히는 엔터테이너",
        "emoji": "🎤",
        "color": "#F43F5E",
        "description": "사람들과 즐겁게 어울리며 자신의 매력과 감각을 표현하는 것을 좋아해요.",
        "strengths": ["친화력", "표현력", "현장 분위기 조성"],
        "work_style": "다양한 사람을 만나고 즐거움과 경험을 제공하는 환경",
        "jobs": [
            ("방송인", "말과 행동으로 정보와 재미를 전달해요.", "방송·미디어"),
            ("공연기획자", "공연의 주제, 출연진, 무대와 진행 과정을 기획해요.", "문화·기획"),
            ("호텔리어", "고객이 편안하고 즐거운 경험을 하도록 서비스를 제공해요.", "관광·서비스"),
            ("메이크업 아티스트", "사람의 특징과 목적에 맞는 이미지를 연출해요.", "뷰티·예술"),
        ],
    },
    "ENFP": {
        "nickname": "열정적인 아이디어 뱅크",
        "emoji": "🌈",
        "color": "#D946EF",
        "description": "새로운 가능성을 발견하고 사람들과 아이디어를 나누며 일을 시작하는 데 에너지가 넘쳐요.",
        "strengths": ["풍부한 아이디어", "긍정적 소통", "새로운 가능성 발견"],
        "work_style": "다양한 사람과 협력하며 새 프로젝트를 만들어 갈 수 있는 환경",
        "jobs": [
            ("광고기획자", "사람들의 관심을 끌 수 있는 광고 아이디어와 전략을 만들어요.", "광고·기획"),
            ("유튜브 콘텐츠 기획자", "시청자가 좋아할 영상 주제와 구성을 기획해요.", "미디어·콘텐츠"),
            ("진로상담사", "개인의 흥미와 강점을 발견하도록 돕고 진로 정보를 제공해요.", "교육·상담"),
            ("브랜드 매니저", "브랜드의 이미지와 상품을 종합적으로 기획하고 관리해요.", "경영·마케팅"),
        ],
    },
    "ENTP": {
        "nickname": "재치 있는 발명가",
        "emoji": "💡",
        "color": "#7C3AED",
        "description": "기존 방식을 새롭게 바라보고 토론하며 독창적인 해결책을 만드는 것을 즐겨요.",
        "strengths": ["창의적 문제 해결", "논리적 토론", "빠른 아이디어 전환"],
        "work_style": "새로운 시도를 장려하고 자유롭게 의견을 제시할 수 있는 환경",
        "jobs": [
            ("스타트업 기획자", "새로운 서비스 아이디어를 구체적인 사업으로 발전시켜요.", "창업·기획"),
            ("변리사", "새로운 기술과 아이디어의 권리를 보호하는 일을 해요.", "법·기술"),
            ("제품 기획자", "사용자에게 필요한 제품의 기능과 방향을 설계해요.", "IT·기획"),
            ("과학 커뮤니케이터", "어려운 과학 지식을 재미있고 이해하기 쉽게 전달해요.", "과학·미디어"),
        ],
    },
    "ESTJ": {
        "nickname": "든든한 운영 관리자",
        "emoji": "📋",
        "color": "#1D4ED8",
        "description": "목표와 규칙을 분명하게 정하고 사람과 일을 효율적으로 관리하는 데 강점이 있어요.",
        "strengths": ["실행력", "조직 관리", "명확한 의사결정"],
        "work_style": "목표와 역할이 분명하고 성과를 체계적으로 관리하는 환경",
        "jobs": [
            ("경영 관리자", "조직의 목표를 세우고 인력과 업무를 효율적으로 운영해요.", "경영·관리"),
            ("경찰관", "법과 질서를 유지하고 시민의 안전을 보호해요.", "공공·안전"),
            ("프로젝트 매니저", "팀의 일정, 역할, 예산을 관리해 목표 달성을 이끌어요.", "기획·관리"),
            ("금융 전문가", "재무 정보를 분석하고 자산 관리와 금융 의사결정을 지원해요.", "경제·금융"),
        ],
    },
    "ESFJ": {
        "nickname": "친절한 협력가",
        "emoji": "🤝",
        "color": "#E11D48",
        "description": "사람들과 조화롭게 협력하고 필요한 도움을 빠르게 제공하는 데 강점이 있어요.",
        "strengths": ["협력과 배려", "책임 있는 소통", "관계 형성"],
        "work_style": "사람들과 자주 소통하고 도움에 대한 반응을 직접 확인하는 환경",
        "jobs": [
            ("교사", "학생의 학습과 생활을 지도하며 성장을 지원해요.", "교육"),
            ("승무원", "승객의 안전을 책임지고 편안한 서비스를 제공해요.", "항공·서비스"),
            ("행사기획자", "여러 사람과 협력해 행사 전체 과정을 준비하고 운영해요.", "문화·기획"),
            ("인사 담당자", "조직 구성원의 채용, 교육, 복지와 관계를 관리해요.", "경영·인사"),
        ],
    },
    "ENFJ": {
        "nickname": "성장을 이끄는 리더",
        "emoji": "🌟",
        "color": "#C026D3",
        "description": "사람의 가능성을 발견하고 공동의 목표를 향해 함께 나아가도록 이끄는 편이에요.",
        "strengths": ["공감형 리더십", "동기 부여", "설득과 소통"],
        "work_style": "사람의 성장과 팀의 변화를 이끌 수 있는 협력적 환경",
        "jobs": [
            ("교사", "학생의 잠재력을 발견하고 배움과 성장을 이끌어요.", "교육"),
            ("아나운서", "정확한 언어와 표현으로 다양한 정보를 전달해요.", "언론·방송"),
            ("HRD 전문가", "조직 구성원의 역량을 높이는 교육 프로그램을 설계해요.", "교육·경영"),
            ("홍보 전문가", "조직의 가치와 메시지를 대중에게 효과적으로 전달해요.", "홍보·소통"),
        ],
    },
    "ENTJ": {
        "nickname": "목표를 향한 지휘관",
        "emoji": "🚀",
        "color": "#B91C1C",
        "description": "큰 목표를 세우고 필요한 자원을 조직해 빠르게 성과를 만드는 데 강점이 있어요.",
        "strengths": ["목표 설정", "전략적 리더십", "결단력"],
        "work_style": "도전적인 목표를 세우고 의사결정 권한과 책임을 가질 수 있는 환경",
        "jobs": [
            ("기업 경영자", "조직의 방향을 정하고 중요한 의사결정을 내려요.", "경영"),
            ("경영 컨설턴트", "기업의 문제를 분석해 성장 전략과 개선안을 제시해요.", "전략·컨설팅"),
            ("검사·변호사", "법률을 분석하고 논리적으로 사건을 해결해요.", "법률"),
            ("IT 프로젝트 책임자", "기술 프로젝트의 목표와 팀을 총괄해 결과를 만들어요.", "IT·관리"),
        ],
    },
}

MBTI_GROUPS = {
    "분석가형 NT": ["INTJ", "INTP", "ENTJ", "ENTP"],
    "외교관형 NF": ["INFJ", "INFP", "ENFJ", "ENFP"],
    "관리자형 SJ": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    "탐험가형 SP": ["ISTP", "ISFP", "ESTP", "ESFP"],
}

# ---------------------------------------------------------
# 디자인
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: "Pretendard", "Apple SD Gothic Neo", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(139, 92, 246, .16), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(59, 130, 246, .13), transparent 25%),
            linear-gradient(180deg, #F8FAFF 0%, #FFFFFF 55%, #F5F3FF 100%);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3rem 2.2rem;
        border-radius: 30px;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 48%, #DB2777 100%);
        box-shadow: 0 24px 60px rgba(79, 70, 229, .25);
        color: white;
        margin-bottom: 1.6rem;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -55px;
        top: -75px;
        border-radius: 50%;
        background: rgba(255,255,255,.12);
    }

    .hero-label {
        display: inline-block;
        padding: .42rem .8rem;
        border-radius: 999px;
        background: rgba(255,255,255,.18);
        font-size: .9rem;
        font-weight: 700;
        margin-bottom: .8rem;
    }

    .hero-title {
        font-size: clamp(2rem, 5vw, 3.6rem);
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: -.04em;
        margin: 0;
    }

    .hero-subtitle {
        max-width: 720px;
        font-size: 1.05rem;
        line-height: 1.7;
        opacity: .92;
        margin-top: 1rem;
        margin-bottom: 0;
    }

    .guide-box {
        background: rgba(255,255,255,.86);
        border: 1px solid rgba(99,102,241,.14);
        border-radius: 20px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 10px 28px rgba(30,41,59,.06);
        margin-bottom: 1.3rem;
    }

    .result-head {
        padding: 1.8rem;
        border-radius: 24px;
        color: white;
        box-shadow: 0 18px 40px rgba(15,23,42,.16);
        margin: 1.2rem 0 1.4rem;
    }

    .result-code {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: .04em;
    }

    .result-name {
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: .15rem;
    }

    .result-desc {
        font-size: 1rem;
        line-height: 1.7;
        margin-top: .8rem;
        opacity: .94;
    }

    .info-card, .job-card {
        background: rgba(255,255,255,.94);
        border: 1px solid #E8EAF6;
        border-radius: 21px;
        padding: 1.25rem;
        height: 100%;
        box-shadow: 0 10px 28px rgba(15,23,42,.07);
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 34px rgba(79,70,229,.14);
    }

    .job-title {
        font-size: 1.18rem;
        font-weight: 800;
        color: #172033;
        margin-bottom: .45rem;
    }

    .job-desc {
        min-height: 3.2rem;
        color: #475569;
        font-size: .94rem;
        line-height: 1.55;
    }

    .job-tag {
        display: inline-block;
        margin-top: .8rem;
        padding: .32rem .66rem;
        border-radius: 999px;
        background: #EEF2FF;
        color: #4F46E5;
        font-size: .78rem;
        font-weight: 700;
    }

    .chip {
        display: inline-block;
        padding: .4rem .7rem;
        margin: .18rem .2rem .18rem 0;
        border-radius: 999px;
        background: #F1F5F9;
        color: #334155;
        font-size: .88rem;
        font-weight: 700;
    }

    .section-title {
        margin-top: 1.4rem;
        margin-bottom: .75rem;
        font-size: 1.35rem;
        font-weight: 800;
        color: #172033;
    }

    .notice {
        background: #FFF7ED;
        color: #9A3412;
        border: 1px solid #FED7AA;
        border-radius: 16px;
        padding: .9rem 1rem;
        font-size: .9rem;
        line-height: 1.55;
        margin-top: 1.5rem;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px;
        min-height: 54px;
        border: 1.5px solid #C7D2FE;
        background: rgba(255,255,255,.96);
    }

    .stButton > button {
        width: 100%;
        min-height: 52px;
        border: 0;
        border-radius: 16px;
        color: white;
        font-weight: 800;
        font-size: 1rem;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        box-shadow: 0 10px 22px rgba(79,70,229,.22);
    }

    .stButton > button:hover {
        color: white;
        border: 0;
        transform: translateY(-1px);
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    @media (max-width: 700px) {
        .hero { padding: 2.2rem 1.4rem; border-radius: 22px; }
        .result-code { font-size: 2.25rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 화면 상단
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">🎯 고등학생 진로 탐색 프로젝트</div>
        <h1 class="hero-title">MBTI로 만나는<br>나의 미래 직업</h1>
        <p class="hero-subtitle">
            나의 MBTI를 선택하면 성향의 강점을 살릴 수 있는 직업을 추천해 드려요.
            결과를 친구들과 비교하며 새로운 진로 가능성도 발견해 보세요!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="guide-box">
        <b>✨ 이용 방법</b><br>
        ① 자신의 MBTI를 선택하고 &nbsp; ② 결과 보기 버튼을 누르면 &nbsp;
        ③ 추천 직업과 탐색 질문을 확인할 수 있어요.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 선택 영역
# ---------------------------------------------------------
left, right = st.columns([3, 1])

with left:
    selected_mbti = st.selectbox(
        "나의 MBTI를 선택하세요",
        options=list(MBTI_DATA.keys()),
        index=None,
        placeholder="예: ENFP",
    )

with right:
    st.write("")
    st.write("")
    show_result = st.button("🔍 직업 추천받기", use_container_width=True)

# 선택값은 버튼 클릭 후에도 유지
if show_result:
    if selected_mbti is None:
        st.warning("먼저 MBTI를 선택해 주세요.")
    else:
        st.session_state["result_mbti"] = selected_mbti

result_mbti = st.session_state.get("result_mbti")

# ---------------------------------------------------------
# 결과 영역
# ---------------------------------------------------------
if result_mbti:
    data = MBTI_DATA[result_mbti]

    st.markdown(
        f"""
        <div class="result-head" style="background: linear-gradient(135deg, {data['color']}, #7C3AED);">
            <div class="result-code">{data['emoji']} {result_mbti}</div>
            <div class="result-name">{data['nickname']}</div>
            <div class="result-desc">{data['description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    info1, info2 = st.columns(2)

    with info1:
        strength_chips = "".join(
            f'<span class="chip">#{strength}</span>' for strength in data["strengths"]
        )
        st.markdown(
            f"""
            <div class="info-card">
                <div class="section-title" style="margin-top:0;">💪 나의 강점 키워드</div>
                {strength_chips}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="section-title" style="margin-top:0;">🏫 잘 맞을 수 있는 업무 환경</div>
                <div style="color:#475569; line-height:1.7;">{data['work_style']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">🌟 추천 직업 TOP 4</div>', unsafe_allow_html=True)

    job_columns = st.columns(4)
    job_icons = ["🥇", "🥈", "🥉", "✨"]

    for column, icon, job in zip(job_columns, job_icons, data["jobs"]):
        job_name, job_description, job_field = job
        with column:
            st.markdown(
                f"""
                <div class="job-card">
                    <div style="font-size:1.45rem;">{icon}</div>
                    <div class="job-title">{job_name}</div>
                    <div class="job-desc">{job_description}</div>
                    <span class="job-tag">{job_field}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">🧭 진로 탐색 미션</div>', unsafe_allow_html=True)

    mission1, mission2, mission3 = st.columns(3)
    missions = [
        ("1", "가장 관심 있는 직업 하나를 선택해 실제 하는 일을 조사해 보세요."),
        ("2", "그 직업에 필요한 전공, 자격, 능력을 세 가지 이상 찾아보세요."),
        ("3", "추천에 없더라도 내가 좋아하는 활동과 연결되는 직업을 추가해 보세요."),
    ]

    for column, mission in zip([mission1, mission2, mission3], missions):
        number, text = mission
        with column:
            st.markdown(
                f"""
                <div class="info-card">
                    <div style="font-size:1.5rem; font-weight:800; color:{data['color']};">
                        MISSION {number}
                    </div>
                    <div style="margin-top:.55rem; color:#475569; line-height:1.65;">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="notice">
            <b>📌 꼭 기억하세요.</b><br>
            MBTI는 흥미와 성향을 돌아보는 참고 자료일 뿐, 직업 능력이나 미래를 결정하지 않아요.
            진로를 정할 때는 관심 분야, 교과 역량, 가치관, 경험을 함께 살펴보는 것이 중요합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.info("위에서 MBTI를 선택하면 추천 결과가 나타납니다.")

# ---------------------------------------------------------
# 하단 전체 유형 보기
# ---------------------------------------------------------
with st.expander("📚 MBTI 16가지 유형 한눈에 보기"):
    for group_name, mbti_list in MBTI_GROUPS.items():
        st.markdown(f"**{group_name}**")
        st.write(" · ".join(
            f"{code} {MBTI_DATA[code]['emoji']} {MBTI_DATA[code]['nickname']}"
            for code in mbti_list
        ))
