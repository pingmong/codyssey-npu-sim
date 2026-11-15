"""05. MAC 연산 (Multiply-Accumulate) - 외부 라이브러리 없이 반복문으로 구현"""


def mac(pattern, filt):
    """같은 위치끼리 곱해서 전부 더한다. N×N이면 곱셈 N²번 → O(N²).

    2차원 리스트를 그대로 사용하는 기본 버전.
    """
    total = 0
    n = len(pattern)
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def mac_flat(pattern_flat, filt_flat):
    """보너스 1: 1차원 배열(길이 N²) 버전.

    연산 횟수는 똑같이 N²이지만 반복문이 하나라서 인덱싱이 단순해진다.
    (pattern[i][j] 처럼 두 번 찾아가는 대신 pattern_flat[k] 한 번)
    실제 NPU/GPU 메모리도 2차원이 아니라 이렇게 한 줄로 늘어선 1차원이다.
    """
    total = 0
    for k in range(len(pattern_flat)):
        total += pattern_flat[k] * filt_flat[k]
    return total
