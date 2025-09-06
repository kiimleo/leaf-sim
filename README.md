# Leaf Overlap Simulator

식물의 잎 배치 패턴이 광합성 효율에 미치는 영향을 시뮬레이션하는 도구입니다.

## 기능

- 피보나치 나선형 잎 배치 시뮬레이션
- 황금각(137.5°) 등 다양한 각도 테스트
- 잎 중첩도 및 광합성 가능 영역 계산
- 웹 UI와 명령줄 인터페이스 제공
- 각도 스위핑을 통한 최적 배치각 탐색

## 설치 방법

### 필수 요구사항
- Python 3.7 이상
- pip (Python 패키지 관리자)

### 설치 단계

1. **저장소 클론**
```bash
git clone https://github.com/YOUR_USERNAME/leaf-sim.git
cd leaf-sim
```

2. **가상환경 생성 (권장)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

## 사용 방법

### 웹 UI 실행
```bash
streamlit run streamlit_app.py
```
브라우저에서 `http://localhost:8501` 접속

### 명령줄 실행
```bash
# 단일 시뮬레이션
python -m simul.cli --N 8 --theta 137.5 --show

# 각도 스위핑
python -m simul.cli --N 8 --sweep --span 10 --step 1
```

## 파라미터 설명

- `N`: 잎 개수
- `theta`: 배치 각도 (도 단위, 기본값: 137.5° 황금각)
- `a, b`: 타원 잎의 장축/단축 (기본값: a=20, b=5)
- `c`: 잎 간격 상수 (기본값: 18.0)
- `box`: 시뮬레이션 영역 크기 (픽셀)
- `res`: 격자 해상도 (낮을수록 정확하지만 느림)

## 프로젝트 구조

```
leaf-sim/
├── simul/
│   ├── __init__.py
│   ├── model.py       # 핵심 시뮬레이션 로직
│   └── cli.py         # 명령줄 인터페이스
├── streamlit_app.py   # 웹 UI
├── requirements.txt   # 의존성 목록
└── README.md
```

## 수학적 배경

- 잎 배치: r = c√k, θ = k×각도 (k는 잎 번호)
- 타원 방정식: ((x-xk)/a)² + ((y-yk)/b)² ≤ 1
- 중첩도 = 전체 잎 면적 - 합집합 면적
- 최적각 탐색을 통한 광합성 효율 최대화

## 문제 해결

**가상환경 활성화 오류 (Windows)**
```bash
# PowerShell에서 실행 정책 변경이 필요할 수 있습니다
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**의존성 설치 오류**
```bash
# pip 업그레이드 후 재시도
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 라이선스

MIT License