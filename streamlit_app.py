# 필요한 라이브러리 임포트
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from simul.model import simulate_once, sweep_theta

# Streamlit 페이지 설정
st.set_page_config(page_title="Leaf Overlap Simulator", layout="centered")

# 메인 제목
st.title("Leaf Overlap Simulator (Raster)")

# 파라미터 입력 UI를 2개 컬럼으로 배치
col1, col2 = st.columns(2)

# 첫 번째 컬럼: 기본 시뮬레이션 파라미터
with col1:
    N = st.selectbox("N (number of leaves)", [5,8,13,21], index=1)  # 잎 개수 선택
    theta = st.slider("theta (degrees)", min_value=60.0, max_value=180.0, value=137.5, step=0.5)  # 배치 각도
    c = st.slider("spacing c", min_value=8.0, max_value=40.0, value=18.0, step=1.0)  # 잎 간격

# 두 번째 컬럼: 잎 모양 및 시뮬레이션 설정
with col2:
    a = st.number_input("ellipse a", value=20.0, step=0.5)  # 타원 장축
    b = st.number_input("ellipse b", value=5.0, step=0.5)   # 타원 단축
    box = st.slider("box size (pixels)", min_value=400, max_value=1000, value=600, step=100)  # 시뮬레이션 영역

# 해상도 설정 (낮을수록 정확하지만 느림)
res = st.selectbox("resolution (lower = more accurate, slower)", [1.5, 1.0, 0.5, 0.25], index=1)

# 잎 면적 조건 확인 (a×b=100일 때 면적=100π)
if abs(a*b - 100) > 1e-6:
    st.info("Tip: a*b=100 이어야 한 잎 면적이 100π가 됩니다.")

# 단일 시뮬레이션 실행 버튼
if st.button("Run simulation"):
    # 시뮬레이션 실행
    result = simulate_once(N, theta, a=a, b=b, c=c, box_size=box, res=res)
    
    # 주요 결과 추출
    S = result["S_union_area"]    # 광합성 가능 영역 (합집합)
    overlap = result["overlap_area"]  # 잎 중첩 영역
    
    # 결과를 메트릭으로 표시
    st.metric("Light area S (union)", f"{S:.1f}")
    st.metric("Overlap area", f"{overlap:.1f}")

    # 합집합 마스크 시각화
    mask = result["mask"]
    half = box // 2
    
    # matplotlib 그래프 생성
    fig, ax = plt.subplots()
    ax.imshow(mask, extent=[-half, half, -half, half], origin='lower')
    ax.set_title(f"N={N}, θ={theta}° (union)")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    
    # Streamlit에 그래프 표시
    st.pyplot(fig)

# 각도 스위핑 섹션
st.subheader("Local scan around current θ")

# 스위핑 파라미터 설정
span = st.slider("± span (degrees)", 2.0, 20.0, 10.0, 1.0)  # 현재 각도 기준 ±span 범위
step = st.slider("step (degrees)", 0.5, 5.0, 1.0, 0.5)      # 스위핑 단계

# 각도 스위핑 실행 버튼
if st.button("Scan"):
    # 스위핑할 각도 범위 생성
    thetas = list(np.arange(theta - span, theta + span + 1e-9, step))
    
    # 각 각도에 대해 시뮬레이션 실행
    df = sweep_theta(N, thetas, a=a, b=b, c=c, box_size=box, res=res)
    
    # 결과 테이블 표시
    st.dataframe(df)

    # 광합성 영역 vs 각도 그래프 생성
    fig2, ax2 = plt.subplots()
    ax2.plot(df["theta_deg"], df["S"])  # S값 플롯
    ax2.axvline(theta)  # 현재 설정된 각도에 수직선 표시
    ax2.set_title(f"S vs theta (N={N}, c={c})")
    ax2.set_xlabel("theta (deg)"); ax2.set_ylabel("S (union)")
    
    # Streamlit에 그래프 표시
    st.pyplot(fig2)
