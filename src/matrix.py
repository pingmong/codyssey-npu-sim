"""01. 데이터 구조 - n×n 2차원 리스트 + 패턴 생성기(보너스 2) + 1차원 변환(보너스 1)"""


def make_matrix(n, fill=0):
    """n×n 2차원 리스트 생성. [[0]*n]*n 으로 만들면 행이 공유되므로 주의."""
    return [[fill for _ in range(n)] for _ in range(n)]


def get_cell(matrix, row, col):
    return matrix[row][col]


def set_cell(matrix, row, col, value):
    matrix[row][col] = value


def is_square(matrix, n=None):
    """정사각 행렬인지, (n이 주어지면) 크기가 n인지 검사."""
    if not isinstance(matrix, list) or len(matrix) == 0:
        return False
    size = len(matrix)
    if n is not None and size != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != size:
            return False
    return True


def flatten(matrix):
    """보너스 1: 2차원 n×n → 1차원 길이 n² 리스트. (i, j) → i*n + j"""
    flat = []
    for row in matrix:
        for value in row:
            flat.append(value)
    return flat


def print_matrix(matrix, name=None):
    """행렬을 보기 좋게 출력. 1은 ■, 0은 □ 로도 함께 표시."""
    if name:
        print(name)
    for row in matrix:
        cells = " ".join("%g" % v for v in row)
        shape = " ".join("■" if v else "□" for v in row)
        print("  %s    %s" % (cells, shape))


# ──────────────────────────────────────────────────────────────
# 보너스 2. 패턴 생성기
# ──────────────────────────────────────────────────────────────
def make_cross(n):
    """N×N 십자가 패턴 생성. (짝수 N이면 가운데가 n//2 한 줄로 치우친다)"""
    m = make_matrix(n)
    mid = n // 2
    for i in range(n):
        m[i][mid] = 1
        m[mid][i] = 1
    return m


def make_x(n):
    """N×N X 패턴 생성 (두 대각선)."""
    m = make_matrix(n)
    for i in range(n):
        m[i][i] = 1
        m[i][n - 1 - i] = 1
    return m
