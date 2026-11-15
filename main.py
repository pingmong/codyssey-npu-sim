"""Mini NPU Simulator - 코디세이 미션 3 레퍼런스 구현

09. 실행 흐름: 모드 선택 → 모드별 처리

파일 구성 (미션 요구사항 번호 기준)
  src/matrix.py      01 데이터 구조 + 패턴 생성기
  src/mode_input.py  02 모드 1 (3×3 콘솔 입력)
  src/mode_json.py   03 모드 2 (data.json 로드/검증) + 08 결과 리포트
  src/judge.py       04 라벨 정규화 + 06 epsilon 판정
  src/mac.py         05 MAC 연산
  src/perf.py        07 성능 분석
"""

from src import mode_input
from src import mode_json


def main():
    print("===== Mini NPU Simulator =====")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    while True:
        choice = input("모드를 선택하세요 (1/2): ").strip()
        if choice == "1":
            mode_input.run()
            break
        if choice == "2":
            mode_json.run()
            break
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
