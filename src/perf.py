"""07. 성능 분석 - 크기별 MAC 연산 시간 측정 (+ 보너스 1: 1차원 최적화 전/후 비교)"""

import time

from src.mac import mac, mac_flat
from src.matrix import flatten

REPEAT = 10  # 최소 반복 측정 횟수


def _measure_ms(func, a, b, repeat):
    """I/O를 제외하고 func(a, b) 호출 구간만 repeat회 측정한 평균(ms)."""
    elapsed = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        func(a, b)
        elapsed += time.perf_counter() - start
    return elapsed / repeat * 1000


def measure_mac_ms(pattern, filt, repeat=REPEAT):
    """2차원 기본 MAC의 평균 시간(ms)."""
    return _measure_ms(mac, pattern, filt, repeat)


def measure_mac_flat_ms(pattern, filt, repeat=REPEAT):
    """1차원 최적화 MAC의 평균 시간(ms). 변환(flatten) 시간은 측정에서 제외."""
    return _measure_ms(mac_flat, flatten(pattern), flatten(filt), repeat)


def print_perf_table(rows):
    """rows: [(n, avg_ms), ...] → '크기 / 평균 시간 / 연산 횟수' 표 출력"""
    print("\n[성능 분석] (각 크기 %d회 반복 평균)" % REPEAT)
    print("%-10s %-16s %-12s" % ("크기(N×N)", "평균 시간(ms)", "연산 횟수(N²)"))
    for n, avg_ms in rows:
        print("%-10s %-16.4f %-12d" % ("%dx%d" % (n, n), avg_ms, n * n))


def print_perf_compare_table(rows):
    """보너스 1: rows: [(n, ms_2d, ms_1d), ...] → 최적화 전/후 비교 표 출력"""
    print("\n[최적화 비교] 2차원 vs 1차원 (동일 입력, 각 %d회 반복 평균)" % REPEAT)
    print("%-10s %-14s %-14s %-10s" % ("크기(N×N)", "2차원(ms)", "1차원(ms)", "개선율"))
    for n, ms_2d, ms_1d in rows:
        gain = (1 - ms_1d / ms_2d) * 100 if ms_2d > 0 else 0.0
        print("%-10s %-14.4f %-14.4f %+.1f%%" % ("%dx%d" % (n, n), ms_2d, ms_1d, gain))
