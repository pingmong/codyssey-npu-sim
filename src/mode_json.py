"""03. 모드 2 - data.json 로드/스키마 검증 + 08. 결과 리포트

실패 원인은 세 분류로 태깅한다 (과제 목표: 데이터/스키마 vs 로직 vs 수치 비교).
  CAT_SCHEMA : 키 규칙, 크기 불일치, 라벨 해석 불가, 필터 누락, 숫자가 아닌 값
  CAT_LOGIC  : 판정이 expected와 다름 (MAC/판정 로직 또는 expected 자체를 의심)
  CAT_NUMERIC: 동점(UNDECIDED) → epsilon/부동소수점 비교 정책 문제
"""

import json

from src.judge import EPSILON, LABEL_CROSS, LABEL_X, UNDECIDED, judge, normalize_label
from src.mac import mac
from src.matrix import is_square, make_cross
from src.perf import (measure_mac_flat_ms, measure_mac_ms, print_perf_compare_table,
                      print_perf_table)

CAT_SCHEMA = "데이터/스키마"
CAT_LOGIC = "로직"
CAT_NUMERIC = "수치 비교"


def load_data(path="data.json"):
    """파일이 없거나 깨져도 프로그램이 죽지 않도록 None을 돌려준다."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("오류: %s 파일을 찾을 수 없습니다." % path)
    except json.JSONDecodeError as e:
        print("오류: %s 파싱 실패 - %s" % (path, e))
    return None


def parse_size_from_key(key):
    """'size_13_0' → 13. 규칙에 안 맞으면 None."""
    parts = key.split("_")
    if len(parts) < 2 or parts[0] != "size":
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


def load_filters(data):
    """filters.size_N.{cross|x} → {N: {Cross: matrix, X: matrix}}"""
    result = {}
    for size_key, filt_set in data.get("filters", {}).items():
        n = parse_size_from_key(size_key)
        if n is None or not isinstance(filt_set, dict):
            continue
        normalized = {}
        for raw_label, matrix in filt_set.items():
            label = normalize_label(raw_label)
            if label is not None and is_square(matrix, n):
                normalized[label] = matrix
        result[n] = normalized
    return result


def run_case(case_id, case, filters):
    """하나의 패턴 케이스를 처리해 결과 dict를 돌려준다. 절대 예외를 밖으로 던지지 않는다."""
    result = {"id": case_id, "status": "FAIL", "reason": "", "category": CAT_SCHEMA,
              "verdict": None, "expected": None, "score_cross": None, "score_x": None}

    n = parse_size_from_key(case_id)
    if n is None:
        result["reason"] = "키 규칙 위반 (size_{N}_{idx} 형식 아님)"
        return result

    pattern = case.get("input")
    if not is_square(pattern, n):
        result["reason"] = "패턴 크기 불일치 (키는 %d×%d, 실제 %s)" % (
            n, n, "%d행" % len(pattern) if isinstance(pattern, list) else "배열 아님")
        return result

    expected = normalize_label(case.get("expected"))
    result["expected"] = expected
    if expected is None:
        result["reason"] = "expected 라벨 해석 불가 (%r)" % case.get("expected")
        return result

    filt_set = filters.get(n)
    if not filt_set or LABEL_CROSS not in filt_set or LABEL_X not in filt_set:
        result["reason"] = "size_%d 필터 없음 또는 Cross/X 누락" % n
        return result

    try:
        score_cross = mac(pattern, filt_set[LABEL_CROSS])
        score_x = mac(pattern, filt_set[LABEL_X])
    except TypeError as e:
        result["reason"] = "숫자가 아닌 값 포함 (%s)" % e
        return result

    verdict = judge(score_cross, score_x)
    result.update(score_cross=score_cross, score_x=score_x, verdict=verdict)

    if verdict == expected:
        result["status"] = "PASS"
        result["category"] = None
    elif verdict == UNDECIDED:
        result["category"] = CAT_NUMERIC
        result["reason"] = "동점 (|%.6g - %.6g| < %g)" % (score_cross, score_x, EPSILON)
    else:
        result["category"] = CAT_LOGIC
        result["reason"] = "판정 %s ≠ expected %s" % (verdict, expected)
    return result


def print_case_table(results):
    print("\n[케이스별 판정]")
    print("%-12s %-12s %-12s %-10s %-9s %s" % (
        "케이스", "Cross 점수", "X 점수", "판정", "expected", "결과"))
    for r in results:
        print("%-12s %-12s %-12s %-10s %-9s %s" % (
            r["id"],
            "-" if r["score_cross"] is None else "%g" % r["score_cross"],
            "-" if r["score_x"] is None else "%g" % r["score_x"],
            r["verdict"] or "-", r["expected"] or "-", r["status"]))


def print_summary(results):
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    print("\n[결과 요약] 전체 %d / 통과 %d / 실패 %d" % (total, passed, total - passed))
    counts = {}
    for r in results:
        if r["status"] != "PASS":
            print("  - %-12s [%s] %s" % (r["id"], r["category"], r["reason"]))
            counts[r["category"]] = counts.get(r["category"], 0) + 1
    if counts:
        print("  실패 분류: " + ", ".join("%s %d건" % (k, v) for k, v in counts.items()))


def run(path="data.json"):
    data = load_data(path)
    if data is None:
        return

    filters = load_filters(data)
    print("필터 로드 완료: 크기 %s" % sorted(filters.keys()))

    results = []
    for case_id, case in data.get("patterns", {}).items():
        results.append(run_case(case_id, case if isinstance(case, dict) else {}, filters))
    print_case_table(results)

    # 성능 분석: 3×3은 생성기로, 나머지는 로드된 필터로
    targets = [(3, make_cross(3))]
    for n in sorted(filters.keys()):
        f = filters[n].get(LABEL_CROSS)
        if f is not None:
            targets.append((n, f))
    perf_rows = [(n, measure_mac_ms(f, f)) for n, f in targets]
    print_perf_table(perf_rows)

    # 보너스 1: 동일 입력·동일 반복으로 1차원 최적화 전/후 비교
    compare_rows = [(n, ms_2d, measure_mac_flat_ms(f, f))
                    for (n, f), (_, ms_2d) in zip(targets, perf_rows)]
    print_perf_compare_table(compare_rows)

    print_summary(results)
