import json
from pathlib import Path

def enrich_0001(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Word Problem", "difficulty": "easy"}
    data["domain"] = {
        "objects": [
            {"id": "black_stones", "count": 374, "unit": "개"},
            {"id": "white_stones", "count": 558, "unit": "개"},
            {"id": "total_stones", "formula": "black_stones + white_stones", "value": 932},
            {"id": "remaining_stones", "count": 463, "unit": "개"},
            {"id": "removed_stones", "formula": "total_stones - remaining_stones", "value": 469}
        ],
        "goal": "removed_stones"
    }

def enrich_0002(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Equation Puzzle", "difficulty": "medium"}
    data["domain"] = {
        "objects": [{"id": "square", "symbol": "■"}, {"id": "triangle", "symbol": "▲"}],
        "relations": [
            {"id": "eq1", "expr": "800 - 347 + square = 650"},
            {"id": "eq2", "expr": "543 - triangle = square"}
        ],
        "values": {"square": 197, "triangle": 346},
        "goal": "triangle - square"
    }

def enrich_0003(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Vertical Arithmetic Puzzle", "difficulty": "hard"}
    data["domain"] = {
        "objects": [{"id": "a", "symbol": "㉠"}, {"id": "b", "symbol": "㉡"}, {"id": "c", "symbol": "㉢"}],
        "vertical_subtraction": {"minuend": "ab2", "subtrahend": "1ac", "difference": "314"},
        "values": {"a": 4, "b": 6, "c": 8},
        "goal": "a + b + c"
    }

def enrich_0004(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Set Theory Word Problem", "difficulty": "medium"}
    data["domain"] = {
        "groups": [{"id": "total", "count": 780}, {"id": "korean_lovers", "count": 621}, {"id": "math_lovers", "count": 348}],
        "logic": "N(A union B) = N(A) + N(B) - N(A intersect B)",
        "goal": "korean_lovers_and_math_lovers"
    }

def enrich_0005(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Inequality Puzzle", "difficulty": "medium"}
    data["domain"] = {
        "expression": "179 + 265 < 933 - square",
        "evaluation": {"left_sum": 444, "max_square_value": 488},
        "goal": "max_natural_number_square"
    }

def enrich_0006(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Card Number Puzzle", "difficulty": "hard"}
    data["domain"] = {
        "available_cards": [0, 2, 4, 6, 8],
        "conditions": [
            {"id": "num1", "description": "Three-digit, tens digit 8, second largest"},
            {"id": "num2", "description": "Three-digit, ones digit 8, second smallest"}
        ],
        "values": {"num1": 682, "num2": 248},
        "goal": "num1 - num2"
    }

def enrich_0007(data):
    data["metadata"]["education"] = {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"}
    data["metadata"]["classification"] = {"topic": "Addition and Subtraction", "sub_topic": "Expression Maximization", "difficulty": "hard"}
    data["domain"] = {
        "available_numbers": [365, 567, 827, 910],
        "formula_template": "box1 - box2 + box3",
        "optimal_selection": {"box1": 910, "box2": 365, "box3": 827},
        "goal": "maximum_result"
    }

enrich_funcs = {
    "0001": enrich_0001,
    "0002": enrich_0002,
    "0003": enrich_0003,
    "0004": enrich_0004,
    "0005": enrich_0005,
    "0006": enrich_0006,
    "0007": enrich_0007
}

for num, func in enrich_funcs.items():
    path = Path(f"sample_data/problems/ke_3rd/{num}/{num}.semantic.json")
    if not path.exists():
        # Try different naming if any
        alt_path = Path(f"sample_data/problems/ke_3rd/{num}/ke_3rd_{num}.semantic.json")
        if alt_path.exists():
            path = alt_path
    
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        func(data)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Enriched {path}")
    else:
        print(f"File not found for {num}")
