"""04. 라벨 정규화 + 06. 점수 비교 정책(epsilon)"""

EPSILON = 1e-9          # 허용오차
LABEL_CROSS = "Cross"   # 표준 라벨
LABEL_X = "X"
UNDECIDED = "UNDECIDED"


def normalize_label(raw):
    """data.json에 섞여 있는 표기('+', 'cross', 'x', 'X' …)를 표준 라벨로 통일."""
    if raw is None:
        return None
    key = str(raw).strip().lower()
    if key in ("+", "cross", "plus"):
        return LABEL_CROSS
    if key in ("x", "ex"):
        return LABEL_X
    return None  # 알 수 없는 라벨 → 호출부에서 FAIL 처리


def judge(score_a, score_b, label_a=LABEL_CROSS, label_b=LABEL_X):
    """두 점수를 허용오차 기준으로 비교. 동점이면 UNDECIDED.

    == 로 비교하면 0.1 + 0.2 == 0.3 이 False가 되는 부동소수점 오차에 걸린다.
    """
    if abs(score_a - score_b) < EPSILON:
        return UNDECIDED
    return label_a if score_a > score_b else label_b
