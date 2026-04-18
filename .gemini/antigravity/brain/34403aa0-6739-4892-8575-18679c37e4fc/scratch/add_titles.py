import json
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

titles = {
    "0001": "바둑돌 빼기",
    "0002": "모양에 알맞은 수 구하기",
    "0003": "벌레 먹은 셈 (뺄셈)",
    "0004": "국어와 수학을 모두 좋아하는 학생 수",
    "0005": "부등식을 만족하는 가장 큰 자연수",
    "0006": "수 카드로 만든 수의 차",
    "0007": "계산 결과가 가장 큰 식 만들기",
    "0008": "가전제품 소비전력 합산",
    "0009": "도형 복면산 뺄셈",
    "0010": "선분의 길이 계산하기"
}

# Find all semantic.json files and add title if missing or if it's 000x
for p in root.rglob("*.semantic.json"):
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    prob_id = data.get("problem_id", "")
    for num, title in titles.items():
        if num in prob_id:
            data["title"] = title
            break
    
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated title for {p.parent.name}")

print("Titles updated.")
