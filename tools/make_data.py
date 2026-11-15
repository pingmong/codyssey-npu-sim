"""샘플 data.json 생성기 (실제 미션 data.json 구조를 추정해서 만든 것)
실행: 프로젝트 루트에서  python -m tools.make_data  → data.sample.json
분석: python main.py 에서 2 선택 후 기본은 data.json. 샘플로 돌리려면 mode_json.run("data.sample.json")
키 규칙: filters.size_N.{cross|x}, patterns.size_N_idx.{input, expected}
의도적으로 넣은 함정: 라벨 표기 혼용('+', 'x', 'X'), 크기 불일치, 동점, 잘못된 expected, 비정상 키
"""
import json
import random

from src.matrix import make_cross, make_x

random.seed(42)


def noisy(matrix, flips):
    """셀 몇 개를 반전시켜 '비슷하지만 다른' 패턴을 만든다."""
    n = len(matrix)
    m = [row[:] for row in matrix]
    for _ in range(flips):
        i, j = random.randrange(n), random.randrange(n)
        m[i][j] = 1 - m[i][j]
    return m


data = {"filters": {}, "patterns": {}}
for n in (5, 13, 25):
    data["filters"]["size_%d" % n] = {"cross": make_cross(n), "x": make_x(n)}

idx = 0
for n in (5, 13, 25):
    flips = max(1, n // 4)
    cases = [
        (make_cross(n), "+"),
        (make_x(n), "x"),
        (noisy(make_cross(n), flips), "+"),
        (noisy(make_x(n), flips), "X"),
    ]
    for pattern, label in cases:
        data["patterns"]["size_%d_%d" % (n, idx)] = {"input": pattern, "expected": label}
        idx += 1

# 함정 1: 키는 size_5인데 실제 입력은 3×3 → 크기 불일치 FAIL
data["patterns"]["size_5_99"] = {"input": make_cross(3), "expected": "+"}
# 함정 2: 전부 1인 패턴 → Cross/X 점수가 같아 UNDECIDED
data["patterns"]["size_5_98"] = {"input": [[1] * 5 for _ in range(5)], "expected": "+"}
# 함정 3: expected가 잘못 적힘 (십자가인데 'x') → 판정 ≠ expected, 로직/데이터 의심
data["patterns"]["size_13_97"] = {"input": make_cross(13), "expected": "x"}
# 함정 4: 키 규칙 위반
data["patterns"]["pattern_bad"] = {"input": make_cross(5), "expected": "+"}

with open("data.sample.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("data.sample.json 생성:", len(data["patterns"]), "cases")
