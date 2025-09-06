import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd

def leaf_centers(N:int, theta_deg:float, c:float=18.0) -> np.ndarray:
    """잎들의 중심점 좌표를 나선형으로 계산
    
    피보나치 나선 형태로 N개 잎의 (x,y) 좌표를 생성
    Args:
        N: 잎 개수
        theta_deg: 회전각 (도 단위, 보통 황금각 137.5°)
        c: 간격 상수 (잎 사이 거리 조절)
    Returns:
        Nx2 배열 형태의 (xk, yk) 좌표
    """
    theta = np.deg2rad(theta_deg)  # 도를 라디안으로 변환
    ks = np.arange(N, dtype=float)  # 잎 번호 (0, 1, 2, ..., N-1)
    r = c * np.sqrt(ks)  # 중심에서의 거리: r = c√k
    ang = ks * theta     # 각도: k번째 잎의 각도 = k × θ
    
    # 극좌표를 직교좌표로 변환
    xk = r * np.cos(ang)
    yk = r * np.sin(ang)
    return np.stack([xk, yk], axis=1)

def union_area_raster(centers:np.ndarray, a:float, b:float, box_size:int=600, res:float=1.0):
    """래스터 방식으로 타원들의 합집합 영역을 계산
    
    각 잎을 타원으로 모델링하고 픽셀 단위로 중첩 영역을 계산
    Args:
        centers: 잎 중심점들의 좌표 배열
        a: 타원의 장축 반지름
        b: 타원의 단축 반지름  
        box_size: 시뮬레이션 영역 크기 (픽셀)
        res: 격자 해상도 (작을수록 정밀)
    Returns:
        (합집합_면적, 합집합_마스크, X좌표_격자, Y좌표_격자)
    """
    half = box_size // 2  # 중심에서 경계까지 거리
    
    # 시뮬레이션 격자 생성 (-half ~ +half)
    xs = np.arange(-half, half, res)
    ys = np.arange(-half, half, res) 
    X, Y = np.meshgrid(xs, ys)
    
    # 합집합 마스크 초기화 (False로 시작)
    union_mask = np.zeros_like(X, dtype=bool)
    
    # 각 잎(타원)에 대해 내부 영역 계산 후 합집합 구성
    for (xk, yk) in centers:
        # 타원 방정식: ((x-xk)/a)² + ((y-yk)/b)² ≤ 1
        inside = ((X - xk)/a)**2 + ((Y - yk)/b)**2 <= 1.0
        union_mask |= inside  # OR 연산으로 합집합 구성
    
    # 면적 계산 (True인 픽셀 개수 × 픽셀 면적)
    pixel_area = res * res
    union_area = union_mask.sum() * pixel_area
    return union_area, union_mask, X, Y

def simulate_once(N:int, theta_deg:float, a:float=20.0, b:float=5.0, c:float=18.0, box_size:int=600, res:float=1.0):
    """단일 파라미터 조합에 대한 잎 배치 시뮬레이션 실행
    
    주어진 조건에서 광합성 가능 영역과 잎 중첩 영역을 계산
    Args:
        N: 잎 개수
        theta_deg: 배치 각도 (도)
        a, b: 타원 잎의 장축/단축
        c: 잎 간격 상수
        box_size: 시뮬레이션 영역 크기
        res: 격자 해상도
    Returns:
        시뮬레이션 결과 딕셔너리
    """
    # 1. 잎들의 중심점 좌표 계산
    centers = leaf_centers(N, theta_deg, c=c)
    
    # 2. 타원들의 합집합 영역 계산 (광합성 가능 영역)
    S, union_mask, X, Y = union_area_raster(centers, a=a, b=b, box_size=box_size, res=res)
    
    # 3. 개별 잎 면적 (문제에서 주어진 조건: a×b=100일 때 면적=100π)
    leaf_area = 100.0 * pi
    
    # 4. 중첩 면적 = 전체 잎 면적 - 합집합 면적
    overlap = N * leaf_area - S
    
    # 결과 반환
    return {
        "N": N,
        "theta_deg": theta_deg,
        "S_union_area": S,          # 광합성 가능 영역 (합집합)
        "overlap_area": overlap,     # 잎 중첩 영역
        "mask": union_mask,          # 시각화용 마스크
        "X": X,                     # X 좌표 격자
        "Y": Y,                     # Y 좌표 격자
        "centers": centers,          # 잎 중심점들
        "params": {"a": a, "b": b, "c": c, "box_size": box_size, "res": res}
    }

def sweep_theta(N:int, thetas:list, a:float=20.0, b:float=5.0, c:float=18.0, box_size:int=600, res:float=1.0) -> pd.DataFrame:
    """여러 각도에 대해 일괄 시뮬레이션 실행
    
    최적 배치 각도를 찾기 위해 각도 범위를 스윕하며 시뮬레이션
    Args:
        N: 잎 개수
        thetas: 테스트할 각도들의 리스트
        나머지: simulate_once와 동일
    Returns:
        각도별 결과를 정리한 DataFrame (theta_deg, S, overlap 컬럼)
    """
    rows = []
    # 각 각도에 대해 시뮬레이션 실행
    for th in thetas:
        r = simulate_once(N, th, a=a, b=b, c=c, box_size=box_size, res=res)
        # 핵심 결과만 추출하여 저장
        rows.append({
            "N": N, 
            "theta_deg": th, 
            "S": r["S_union_area"],    # 광합성 가능 영역
            "overlap": r["overlap_area"]  # 중첩 영역
        })
    
    # DataFrame으로 변환하고 각도 순으로 정렬
    return pd.DataFrame(rows).sort_values("theta_deg").reset_index(drop=True)

def show_union_mask(result:dict, title:str=None):
    """잎들의 합집합 영역(광합성 가능 영역)을 시각화
    
    Args:
        result: simulate_once()의 결과 딕셔너리
        title: 그래프 제목 (None이면 자동 생성)
    """
    mask = result["mask"]  # 합집합 마스크 (True/False 배열)
    box_size = result["params"]["box_size"]
    half = box_size // 2
    
    # 시각화 생성
    plt.figure()
    plt.imshow(mask, extent=[-half, half, -half, half], origin='lower')
    
    # 제목 설정 (기본값: 파라미터 정보 표시)
    plt.title(title or f"N={result['N']}, θ={result['theta_deg']}° (union)")
    plt.xlabel("x"); plt.ylabel("y")
    plt.show()
