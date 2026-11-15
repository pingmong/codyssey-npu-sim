"""02. 모드 1 - 3×3 필터 A, B와 패턴을 콘솔로 입력받아 판정
   (+ 보너스 2: N을 입력하면 십자가/X 패턴을 자동 생성해 같은 흐름에 재활용)"""

from src.judge import UNDECIDED, judge
from src.mac import mac
from src.matrix import make_cross, make_x, print_matrix
from src.perf import (measure_mac_flat_ms, measure_mac_ms, print_perf_compare_table,
                      print_perf_table)


def parse_number(text):
    """'1' → 1 (int), '0.5' → 0.5 (float). 정수로 쓸 수 있으면 정수로 둔다."""
    try:
        return int(text)
    except ValueError:
        return float(text)  # 여기서도 실패하면 ValueError가 호출부로 올라간다


def read_matrix(name, n=3):
    """n줄을 '공백 구분 숫자 n개'로 입력받는다. 실패 시 안내 후 재입력."""
    while True:
        print("\n%s (%d×%d) 를 한 줄씩 입력하세요. 예: 0 1 0" % (name, n, n))
        rows = []
        ok = True
        for i in range(n):
            line = input("%d행: " % (i + 1)).strip()
            parts = line.split()
            if len(parts) != n:
                print("입력 형식 오류: 각 줄에 %d개의 숫자를 공백으로 구분해 입력하세요." % n)
                ok = False
                break
            try:
                rows.append([parse_number(p) for p in parts])
            except ValueError:
                print("입력 형식 오류: 숫자만 입력할 수 있습니다. (입력값: %s)" % line)
                ok = False
                break
        if ok:
            return rows


def read_int(prompt, min_value=1, max_value=None):
    """정수 하나를 범위 검증과 함께 입력받는다."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("입력 형식 오류: 정수를 입력하세요. (입력값: %s)" % text)
            continue
        if value < min_value or (max_value is not None and value > max_value):
            print("허용 범위 오류: %d 이상%s 정수를 입력하세요." % (
                min_value, "" if max_value is None else " %d 이하" % max_value))
            continue
        return value


def read_manual():
    """직접 입력: 3×3 필터 A, B + 패턴."""
    filt_a = read_matrix("필터 A")
    print("필터 A 저장 완료:", filt_a)
    filt_b = read_matrix("필터 B")
    print("필터 B 저장 완료:", filt_b)
    pattern = read_matrix("패턴")
    return filt_a, filt_b, pattern


def read_generated():
    """보너스 2: N 입력 → 십자가 필터(A), X 필터(B) 자동 생성 → 패턴 선택."""
    n = read_int("패턴 크기 N을 입력하세요 (3~25, 홀수 권장): ", 3, 25)
    filt_a = make_cross(n)
    filt_b = make_x(n)
    print_matrix(filt_a, "\n필터 A = 십자가(Cross) %d×%d 자동 생성" % (n, n))
    print_matrix(filt_b, "\n필터 B = X %d×%d 자동 생성" % (n, n))

    print("\n패턴 선택: 1. 십자가  2. X  3. 직접 입력")
    choice = read_int("번호: ", 1, 3)
    if choice == 1:
        pattern = make_cross(n)
    elif choice == 2:
        pattern = make_x(n)
    else:
        pattern = read_matrix("패턴", n)
    return filt_a, filt_b, pattern


def run():
    print("\n입력 방식: 1. 직접 입력(3×3)  2. 자동 생성(N 입력, 보너스)")
    how = read_int("번호: ", 1, 2)
    filt_a, filt_b, pattern = read_manual() if how == 1 else read_generated()
    n = len(pattern)

    score_a = mac(pattern, filt_a)
    score_b = mac(pattern, filt_b)
    ms_a = measure_mac_ms(pattern, filt_a)
    ms_b = measure_mac_ms(pattern, filt_b)
    verdict = judge(score_a, score_b, "A", "B")

    print("\n[결과]")
    print("필터 A 점수: %g  (평균 %.4f ms)" % (score_a, ms_a))
    print("필터 B 점수: %g  (평균 %.4f ms)" % (score_b, ms_b))
    print("판정: %s" % ("판정 불가" if verdict == UNDECIDED else verdict))

    ms_2d = (ms_a + ms_b) / 2
    print_perf_table([(n, ms_2d)])

    # 보너스 1: 같은 입력으로 1차원 버전과 비교
    ms_1d = (measure_mac_flat_ms(pattern, filt_a) + measure_mac_flat_ms(pattern, filt_b)) / 2
    print_perf_compare_table([(n, ms_2d, ms_1d)])
