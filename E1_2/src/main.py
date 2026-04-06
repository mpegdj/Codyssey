import json
import os

# 1. 개별 퀴즈를 관리하는 클래스
class Quiz:
    def __init__(self, quiz, choices, answer):
        self.quiz = quiz
        self.choices = choices
        self.answer = answer  # 정답 번호 (int)

    def display(self):
        """질문과 선택지를 화면에 출력"""
        print(f"\n[문제] {self.quiz}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")

    def check_answer(self, user_answer):
        """사용자 입력값과 정답 비교 (숫자 변환 처리)"""
        try:
            return int(user_answer) == self.answer
        except ValueError:
            return False
    
    def run_quiz(self):
        """퀴즈 실행 흐름 제어"""
        self.display()
        user_answer = input("정답 번호를 입력하세요: ")
        if self.check_answer(user_answer):
            print("정답입니다! 🎉")
            return True
        else:
            print(f"틀렸습니다. 정답은 {self.answer}번입니다.")
            return False

# 2. 전체 게임 흐름을 관리하는 클래스
class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0

    def add_quiz(self, quiz_obj):
        self.quizzes.append(quiz_obj)

    def run_game(self):
        print("="*40)
        print("   도커 마스터 퀴즈 챌린지 (Docker Quiz)")
        print("="*40)
        
        for quiz in self.quizzes:
            if quiz.run_quiz():
                self.score += 1
        
        print(f"\n게임 종료! 최종 점수: {self.score}/{len(self.quizzes)}")

# 3. 데이터 초기화 및 JSON 관리 함수 (소스 내용 반영)
def initialize_data(file_path):
    """JSON 파일이 없으면 소스 기반 기본 문제를 생성하고 저장합니다."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # 소스 파일 내용을 바탕으로 구성한 기본 퀴즈 데이터
    default_data = {
        "quizzes": [
            {
                "question": "컨테이너 내부(eth0)와 호스트 브리지를 연결하는 '가상 랜선'은?",
                "choices": ["veth pair", "Network Namespace", "iptables", "vmenet"],
                "answer": 1 # [1]
            },
            {
                "question": "이미 실행 중인 컨테이너에 새로운 프로세스를 띄워 '뒷문으로 들어가듯' 접속하는 명령어는?",
                "choices": ["docker run", "docker attach", "docker exec", "docker start"],
                "answer": 3 # [2, 3]
            },
            {
                "question": "docker attach 사용 중 컨테이너를 종료하지 않고 안전하게 빠져나오는 키 조합은?",
                "choices": ["Ctrl + C", "Ctrl + Z", "exit", "Ctrl + P, Q"],
                "answer": 4 # [3]
            },
            {
                "question": "macOS 도커 환경에서 호스트의 ifconfig에 컨테이너 인터페이스가 직접 보이지 않는 이유는?",
                "choices": ["가상 NIC이 없어서", "가상 머신(VM) 내부에서 실행되어서", "보안 설정 때문", "포트 매핑 누락"],
                "answer": 2 # [4, 5]
            },
            {
                "question": "컨테이너 실행 시(docker run) 호스트 포트나 이름을 중복하여 설정하면 발생하는 현상은?",
                "choices": ["자동으로 변경됨", "에러가 발생하며 실행 실패", "기존 컨테이너가 덮어씌워짐", "성능이 저하됨"],
                "answer": 2 # [6, 7]
            }
        ]
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(default_data, f, ensure_ascii=False, indent=4)
    print(f"새로운 퀴즈 파일('{file_path}')이 생성되었습니다.")
    return default_data

# 4. 메인 실행부
if __name__ == "__main__":
    QUIZ_FILE = "quizzes.json"
    
    # 데이터 로드 및 초기화
    data = initialize_data(QUIZ_FILE)
    
    # 게임 객체 생성 및 문제 등록
    game = QuizGame()
    for q in data["quizzes"]:
        game.add_quiz(Quiz(q["question"], q["choices"], q["answer"]))
    
    # 게임 시작
    game.run_game()