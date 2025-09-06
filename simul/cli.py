"""
이 프로젝트 목적은 식물의 잎 배치 패턴이 광합성 효율에 미치는 영향을 시뮬레이션하는 도구입니다
"""

import argparse
import numpy as np
from simul.model import simulate_once, sweep_theta, show_union_mask

def main():
    # 명령줄 인자 파서 설정
    p = argparse.ArgumentParser(description="Leaf overlap simulation (raster)")
    
    # 시뮬레이션 기본 파라미터 설정
    p.add_argument("--N", type=int, default=8, help="number of leaves")  # 잎 개수
    p.add_argument("--theta", type=float, default=137.5, help="angle in degrees")  # 배치 각도 (황금각)
    p.add_argument("--c", type=float, default=18.0, help="spacing constant")  # 잎 간 간격 상수
    
    # 타원 모양 잎의 크기 파라미터
    p.add_argument("--a", type=float, default=20.0, help="ellipse a")  # 타원 장축
    p.add_argument("--b", type=float, default=5.0, help="ellipse b")   # 타원 단축
    
    # 시뮬레이션 해상도 설정
    p.add_argument("--box", type=int, default=600, help="box size (pixels)")  # 시뮬레이션 영역 크기
    p.add_argument("--res", type=float, default=1.0, help="grid resolution (lower=more accurate)")  # 격자 해상도
    
    # 실행 옵션
    p.add_argument("--show", action="store_true", help="show union mask image")  # 시각화 표시 여부
    p.add_argument("--sweep", action="store_true", help="sweep theta around current value")  # 각도 스위핑 모드
    
    # 스위핑 파라미터
    p.add_argument("--span", type=float, default=10.0, help="sweep +/- span degrees")  # 스위핑 범위
    p.add_argument("--step", type=float, default=1.0, help="sweep step degrees")       # 스위핑 단계
    
    args = p.parse_args()

    # 각도 스위핑 모드: 여러 각도에 대해 일괄 시뮬레이션
    if args.sweep:
        # 스위핑할 각도 범위 생성
        thetas = list(np.arange(args.theta - args.span, args.theta + args.span + 1e-9, args.step))
        # 각 각도에 대해 시뮬레이션 실행하고 결과를 DataFrame으로 정리
        df = sweep_theta(args.N, thetas, a=args.a, b=args.b, c=args.c, box_size=args.box, res=args.res)
        print(df.to_string(index=False))
    else:
        # 단일 시뮬레이션 모드: 지정된 파라미터로 한 번만 실행
        r = simulate_once(args.N, args.theta, a=args.a, b=args.b, c=args.c, box_size=args.box, res=args.res)
        
        # 결과 출력
        print(f"N={args.N}, theta={args.theta}°")
        print(f"S (light area) = {r['S_union_area']:.2f}")    # 광합성 가능 영역
        print(f"overlap area   = {r['overlap_area']:.2f}")     # 잎 중첩 영역
        
        # 시각화 옵션이 설정된 경우 합집합 마스크 표시
        if args.show:
            show_union_mask(r)

if __name__ == "__main__":
    main()
