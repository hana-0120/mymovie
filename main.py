from datetime import datetime, timedelta, timezone

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================================================
# 1. 스트림릿 앱 기본 설정
# =========================================================
st.set_page_config(
    page_title="날짜별 박스오피스",
    page_icon="🎬",
    layout="wide",
)

# 영화진흥위원회 KOBIS 일별 박스오피스 API 주소
API_URL = (
    "https://www.kobis.or.kr/kobisopenapi/webservice/rest/"
    "boxoffice/searchDailyBoxOfficeList.json"
)

# 한국 표준시(KST)는 UTC보다 9시간 빠릅니다.
KST = timezone(timedelta(hours=9))


# =========================================================
# 2. 화면 디자인
# =========================================================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #111827, #312e81);
        color: white;
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.2rem;
    }

    .hero p {
        margin: 0.6rem 0 0 0;
        color: #e5e7eb;
        line-height: 1.6;
    }

    .minimum-box {
        padding: 1rem 1.1rem;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        margin-top: 0.7rem;
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 0.9rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. 한국 시간 기준 날짜 계산
# =========================================================
def get_kst_today():
    """
    배포 서버 시간이 아니라 한국 시간 기준으로
    오늘 날짜를 계산합니다.
    """
    return datetime.now(KST).date()


def get_kst_yesterday():
    """한국 시간 기준 어제 날짜를 계산합니다."""
    return get_kst_today() - timedelta(days=1)


# =========================================================
# 4. 문자열 숫자를 정수로 바꾸는 함수
# =========================================================
def to_int(value):
    """
    KOBIS API의 숫자는 문자열로 전달됩니다.

    빈 문자열이나 잘못된 값이 들어오면
    오류 대신 0으로 처리합니다.
    """
    try:
        return int(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0


# =========================================================
# 5. 순위 증감 표시 함수
# =========================================================
def make_rank_change(rank_change):
    """
    rankInten 값을 화살표와 함께 표시합니다.

    양수: 전날보다 순위 상승
    음수: 전날보다 순위 하락
    0: 순위 변화 없음
    """
    if rank_change > 0:
        return f"🔺 +{rank_change}"

    if rank_change < 0:
        return f"🔻 {rank_change}"

    return "➖ 0"


# =========================================================
# 6. KOBIS API 호출
# =========================================================
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_boxoffice(api_key, target_date):
    """
    KOBIS 일별 박스오피스 API를 호출합니다.

    target_date는 yyyymmdd 형식의 문자열입니다.
    """
    params = {
        "key": api_key,
        "targetDt": target_date,
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=20,
    )

    # 인터넷 연결이나 서버 상태코드에 문제가 있으면
    # 예외를 발생시킵니다.
    response.raise_for_status()

    return response.json()


# =========================================================
# 7. 영화 목록을 데이터프레임으로 변환
# =========================================================
def make_boxoffice_dataframe(movie_list):
    """API 영화 목록을 표로 사용할 데이터프레임으로 바꿉니다."""
    rows = []

    for movie in movie_list:
        rank_change = to_int(
            movie.get("rankInten")
        )

        rows.append(
            {
                "순위": to_int(
                    movie.get("rank")
                ),
                "순위증감값": rank_change,
                "순위 변동": make_rank_change(
                    rank_change
                ),
                "영화명": str(
                    movie.get("movieNm", "")
                ).strip(),
                "개봉일": str(
                    movie.get("openDt", "")
                ).strip(),
                "관객수": to_int(
                    movie.get("audiCnt")
                ),
                "누적관객": to_int(
                    movie.get("audiAcc")
                ),
                "스크린수": to_int(
                    movie.get("scrnCnt")
                ),
                "상영횟수": to_int(
                    movie.get("showCnt")
                ),
            }
        )

    dataframe = pd.DataFrame(rows)

    if dataframe.empty:
        return dataframe

    return (
        dataframe
        .sort_values("순위")
        .reset_index(drop=True)
    )


# =========================================================
# 8. 영화명에 트로피와 해골 표시
# =========================================================
def add_movie_emojis(dataframe):
    """
    누적관객 100만 명 초과 영화에는 트로피를 붙이고,
    누적관객이 가장 적은 영화에는 해골을 붙입니다.
    """
    result = dataframe.copy()

    minimum_audience = result[
        "누적관객"
    ].min()

    def decorate_movie_name(row):
        movie_name = row["영화명"]
        emojis = []

        # 100만 명을 '넘은' 영화만 표시합니다.
        if row["누적관객"] > 1_000_000:
            emojis.append("🏆")

        # 최소 누적관객과 같은 영화에는 해골을 표시합니다.
        if row["누적관객"] == minimum_audience:
            emojis.append("💀")

        if emojis:
            return f"{movie_name} {' '.join(emojis)}"

        return movie_name

    result["표시 영화명"] = result.apply(
        decorate_movie_name,
        axis=1,
    )

    return result


# =========================================================
# 9. 오류 확인 안내
# =========================================================
def show_checklist(message):
    """오류 발생 시 빈 화면 대신 확인할 내용을 안내합니다."""
    st.error(message)

    st.info(
        """
        다음 항목을 확인해 주세요.

        1. Streamlit Cloud의 **Settings → Secrets**에
           `KOBIS_KEY`가 등록되어 있는지 확인합니다.
        2. 인증키 앞뒤에 공백이 들어가지 않았는지 확인합니다.
        3. KOBIS 오픈 API 인증키가 사용 가능한 상태인지 확인합니다.
        4. KOBIS 서버에 일시적인 장애가 없는지 확인합니다.
        5. 선택한 날짜의 박스오피스 자료가 집계되었는지 확인합니다.
        """
    )


# =========================================================
# 10. 제목과 날짜 선택
# =========================================================
yesterday = get_kst_yesterday()

st.markdown(
    """
    <div class="hero">
        <h1>🎬 날짜별 박스오피스</h1>
        <p>
            달력에서 날짜를 선택하면 해당 날짜의
            KOBIS 일별 박스오피스 순위를 보여 줍니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

selected_date = st.date_input(
    "조회 날짜 선택",
    value=yesterday,
    max_value=yesterday,
    help=(
        "오늘 자료는 아직 집계되지 않을 수 있으므로 "
        "한국 시간 기준 어제까지만 선택할 수 있습니다."
    ),
)

target_date = selected_date.strftime(
    "%Y%m%d"
)

display_date = selected_date.strftime(
    "%Y년 %m월 %d일"
)

st.caption(
    f"선택한 조회 날짜: {display_date}"
)


# =========================================================
# 11. 비밀 금고에서 인증키 불러오기
# =========================================================
try:
    api_key = st.secrets["KOBIS_KEY"]

except Exception:
    show_checklist(
        "KOBIS 인증키를 찾지 못했습니다."
    )
    st.stop()

api_key = str(api_key).strip()

if not api_key:
    show_checklist(
        "KOBIS 인증키가 비어 있습니다."
    )
    st.stop()


# =========================================================
# 12. API 요청
# =========================================================
try:
    with st.spinner(
        f"{display_date}의 박스오피스를 불러오는 중입니다."
    ):
        result = fetch_boxoffice(
            api_key,
            target_date,
        )

except requests.Timeout:
    show_checklist(
        "KOBIS 서버의 응답 시간이 너무 오래 걸렸습니다."
    )
    st.stop()

except requests.RequestException as error:
    show_checklist(
        "KOBIS API 요청에 실패했습니다."
    )

    with st.expander(
        "오류 상세 정보"
    ):
        st.code(str(error))

    st.stop()

except ValueError as error:
    show_checklist(
        "KOBIS 응답을 JSON 형식으로 읽지 못했습니다."
    )

    with st.expander(
        "오류 상세 정보"
    ):
        st.code(str(error))

    st.stop()


# =========================================================
# 13. faultInfo 오류 상자 확인
# =========================================================
# KOBIS는 인증키가 틀려도 HTTP 상태코드 200을 반환하고
# 응답 안에 faultInfo를 넣을 수 있습니다.
if "faultInfo" in result:
    fault_info = result.get(
        "faultInfo",
        {},
    )

    fault_message = fault_info.get(
        "message",
        "KOBIS API에서 오류 응답을 보냈습니다.",
    )

    show_checklist(
        f"KOBIS 오류: {fault_message}"
    )
    st.stop()


# =========================================================
# 14. 영화 목록 확인
# =========================================================
boxoffice_result = result.get(
    "boxOfficeResult"
)

if not boxoffice_result:
    show_checklist(
        "응답에서 boxOfficeResult를 찾지 못했습니다."
    )
    st.stop()

movie_list = boxoffice_result.get(
    "dailyBoxOfficeList",
    [],
)

if not movie_list:
    st.warning(
        "그날은 아직 집계 전입니다."
    )
    st.info(
        "다른 날짜를 선택하거나 잠시 후 다시 확인해 주세요."
    )
    st.stop()


# =========================================================
# 15. 데이터프레임 생성
# =========================================================
boxoffice_df = make_boxoffice_dataframe(
    movie_list
)

if boxoffice_df.empty:
    st.warning(
        "그날은 아직 집계 전입니다."
    )
    st.stop()

boxoffice_df = add_movie_emojis(
    boxoffice_df
)


# =========================================================
# 16. 1위 영화 지표 카드
# =========================================================
number_one = boxoffice_df.iloc[0]

st.subheader(
    f"🏆 {display_date} 1위 영화"
)

card1, card2, card3 = st.columns(3)

card1.metric(
    "영화명",
    number_one["표시 영화명"],
)

card2.metric(
    "당일 관객수",
    f"{number_one['관객수']:,}명",
)

card3.metric(
    "누적 관객수",
    f"{number_one['누적관객']:,}명",
)


# =========================================================
# 17. 누적관객이 가장 적은 영화 안내
# =========================================================
minimum_row = boxoffice_df.loc[
    boxoffice_df["누적관객"].idxmin()
]

st.markdown(
    f"""
    <div class="minimum-box">
        <b>💀 누적관객이 가장 적은 영화</b><br>
        {minimum_row["영화명"]} 💀 ·
        누적관객 {minimum_row["누적관객"]:,}명
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 18. 관객수 상위 5편 막대그래프
# =========================================================
st.subheader(
    "📊 당일 관객수 상위 5편"
)

top5 = (
    boxoffice_df
    .nlargest(
        5,
        "관객수",
    )
    .sort_values(
        "관객수",
        ascending=True,
    )
)

figure = px.bar(
    top5,
    x="관객수",
    y="표시 영화명",
    orientation="h",
    text="관객수",
    labels={
        "관객수": "당일 관객수",
        "표시 영화명": "영화명",
    },
)

figure.update_traces(
    texttemplate="%{text:,}명",
    textposition="outside",
    cliponaxis=False,
)

figure.update_layout(
    height=430,
    margin=dict(
        l=20,
        r=80,
        t=20,
        b=20,
    ),
    showlegend=False,
    xaxis_tickformat=",",
    yaxis_title=None,
)

st.plotly_chart(
    figure,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


# =========================================================
# 19. 전체 박스오피스 표
# =========================================================
st.subheader(
    "🎞️ 전체 박스오피스 순위"
)

table_df = boxoffice_df[
    [
        "순위",
        "순위 변동",
        "표시 영화명",
        "개봉일",
        "관객수",
        "누적관객",
        "스크린수",
    ]
].copy()

table_df = table_df.rename(
    columns={
        "표시 영화명": "영화명",
    }
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "순위": st.column_config.NumberColumn(
            "순위",
            format="%d위",
        ),
        "순위 변동": st.column_config.TextColumn(
            "전날 대비",
            help=(
                "🔺는 순위 상승, "
                "🔻는 순위 하락, "
                "➖는 변동 없음을 뜻합니다."
            ),
        ),
        "영화명": st.column_config.TextColumn(
            "영화명",
            help=(
                "🏆는 누적관객 100만 명 초과, "
                "💀는 누적관객이 가장 적은 영화입니다."
            ),
        ),
        "개봉일": st.column_config.TextColumn(
            "개봉일",
        ),
        "관객수": st.column_config.NumberColumn(
            "관객수",
            format="%,d명",
        ),
        "누적관객": st.column_config.NumberColumn(
            "누적관객",
            format="%,d명",
        ),
        "스크린수": st.column_config.NumberColumn(
            "스크린수",
            format="%,d개",
        ),
    },
)

st.caption(
    "자료 출처: 영화진흥위원회 KOBIS 오픈 API"
)
