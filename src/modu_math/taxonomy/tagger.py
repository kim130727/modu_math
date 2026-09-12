from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import get_taxonomy_registry

RULE_VERSION = "1.0.0"


@dataclass
class TaggingResult:
    problem_id: str
    concepts: list[str]
    skills: list[str]
    rule_version: str = RULE_VERSION
    source: str = "rule_based"
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "concepts": self.concepts,
            "skills": self.skills,
            "rule_version": self.rule_version,
            "source": self.source,
            "confidence": round(self.confidence, 2),
            "evidence": self.evidence,
        }


class ProblemAutoTagger:
    """Explainable rule-based tagger extracting taxonomy concepts and skills."""

    def __init__(self) -> None:
        self.registry = get_taxonomy_registry()

    def tag(
        self,
        *,
        problem_id: str,
        problem_type: str = "",
        semantic_data: dict[str, Any] | None = None,
        solvable_data: dict[str, Any] | None = None,
        grade: int | None = None,
        language: str = "ko",
    ) -> TaggingResult:
        semantic = semantic_data or {}
        solvable = solvable_data or {}
        metadata = semantic.get("metadata", {}) if isinstance(semantic.get("metadata"), dict) else {}

        unit = str(metadata.get("unit") or metadata.get("unitTopic") or "").strip()
        domain = str(metadata.get("domain") or semantic.get("domain") or "").strip()
        method = str(solvable.get("method") or "").strip()
        plan = str(solvable.get("plan") or "")
        title = str(metadata.get("title") or "")
        ptype = str(problem_type or semantic.get("problem_type") or "").strip()

        # Combine text for holistic matching
        haystack = f"{ptype} {unit} {domain} {method} {plan} {title} {problem_id}".casefold()

        concepts: list[str] = []
        skills: list[str] = []
        evidence: list[str] = []
        confidence = 0.70

        # --- Rule 1: Multiplication and Place Value ---
        if (
            "multiplication" in haystack
            or "곱셈" in haystack
            or "place_value" in haystack
            or method == "place_value_matching"
        ):
            concepts.append("arithmetic.multiplication")
            evidence.append("곱셈 관련 키워드 및 단원 감지")
            if "place_value" in haystack or "자릿값" in haystack or method == "place_value_matching":
                concepts.append("arithmetic.multiplication.place_value")
                skills.append("skill.place_value_matching")
                skills.append("skill.calculate")
                evidence.append("자릿값 계산 및 대응 감지")
                confidence = 0.95
            else:
                skills.append("skill.calculate")
                confidence = 0.90

        # --- Rule 2: Addition and Subtraction ---
        elif (
            "addition" in haystack
            or "subtraction" in haystack
            or "덧셈" in haystack
            or "뺄셈" in haystack
            or "add_parts" in method
        ):
            concepts.append("arithmetic.addition_subtraction")
            evidence.append("덧셈과 뺄셈 단원/유형 감지")
            skills.append("skill.calculate")
            if "ordering" in haystack or "순서" in haystack or "크기" in haystack:
                concepts.append("arithmetic.addition_subtraction.ordering")
                skills.append("skill.read_word_problem")
                evidence.append("계산 결과 정렬 및 비교 조건 감지")
                confidence = 0.95
            else:
                confidence = 0.90

        # --- Rule 3: Division ---
        elif "division" in haystack or "나눗셈" in haystack or "divide" in method:
            concepts.append("arithmetic.division")
            evidence.append("나눗셈 단원/유형 감지")
            skills.append("skill.calculate")
            if "model" in haystack or "수 모형" in haystack or "수모형" in haystack:
                concepts.append("arithmetic.division.model")
                evidence.append("수 모형 나눗셈 모델 감지")
                confidence = 0.95
            else:
                confidence = 0.90

        # --- Rule 4: Fractions and Decimals ---
        elif "fraction" in haystack or "분수" in haystack or "소수" in haystack:
            concepts.append("arithmetic.fractions")
            evidence.append("분수 단원/유형 감지")
            if "분류" in haystack or "판단" in haystack or "ladder" in haystack or "참" in haystack:
                concepts.append("arithmetic.fractions.classification")
                skills.append("skill.verify_fraction")
                evidence.append("분수 개념 참/거짓 및 분류 판단 감지")
                confidence = 0.95
            else:
                concepts.append("arithmetic.fractions.concept")
                skills.append("skill.read_word_problem")
                skills.append("skill.verify_fraction")
                evidence.append("분수 표현 및 의미 파악 감지")
                confidence = 0.90

        # --- Rule 5: Geometry - Segments ---
        elif "segment" in haystack or "선분" in haystack:
            concepts.append("geometry.plane_figures")
            concepts.append("geometry.plane_figures.segments")
            skills.append("skill.compare_lengths")
            evidence.append("선분의 길이 비교 감지")
            confidence = 0.95

        # --- Rule 6: Geometry - Circle ---
        elif "circle" in haystack or "원" in unit or "원" in title or "띠 종이" in haystack:
            concepts.append("geometry.circle")
            evidence.append("원 단원/유형 감지")
            if "sequence" in haystack or "순서" in haystack:
                concepts.append("geometry.circle.drawing")
                skills.append("skill.draw_figure")
                evidence.append("원 그리기 작도 순서 감지")
                confidence = 0.95
            elif "반지름" in haystack or "지름" in haystack or "크게" in haystack or "구멍" in haystack:
                concepts.append("geometry.circle.radius")
                skills.append("skill.draw_figure")
                skills.append("skill.compare_lengths")
                evidence.append("반지름과 원의 크기 관계 감지")
                confidence = 0.95
            else:
                skills.append("skill.draw_figure")
                confidence = 0.85

        # --- Rule 7: Measurement - Capacity & Weight ---
        elif "들이" in haystack or "무게" in haystack or "capacity" in haystack:
            concepts.append("measurement.capacity_weight")
            evidence.append("들이와 무게 단원/유형 감지")
            if "높이" in haystack or "병" in haystack and "설명" in haystack:
                concepts.append("measurement.capacity_weight.height_comparison")
                skills.append("skill.compare_capacity")
                skills.append("skill.review_answer")
                evidence.append("높이와 들이의 비교 조건 판단 감지")
                confidence = 0.95
            else:
                concepts.append("measurement.capacity_weight.comparison")
                skills.append("skill.compare_capacity")
                evidence.append("들이의 직접/간접 비교 감지")
                confidence = 0.95

        # Default fallback if no specific rule matched
        if not concepts:
            if "수와 연산" in haystack or "arithmetic" in haystack:
                concepts.append("arithmetic")
                skills.append("skill.calculate")
                evidence.append("기본 수와 연산 영역 감지")
                confidence = 0.60
            elif "도형" in haystack or "geometry" in haystack:
                concepts.append("geometry")
                skills.append("skill.compare_lengths")
                evidence.append("기본 도형 영역 감지")
                confidence = 0.60
            elif "측정" in haystack or "measurement" in haystack:
                concepts.append("measurement")
                skills.append("skill.compare_capacity")
                evidence.append("기본 측정 영역 감지")
                confidence = 0.60
            else:
                concepts.append("arithmetic")
                skills.append("skill.read_word_problem")
                evidence.append("기본 영역 폴백 적용")
                confidence = 0.50

        # Validate that all generated tags exist in the registry
        valid_concepts = [c for c in dict.fromkeys(concepts) if self.registry.contains(c)]
        valid_skills = [s for s in dict.fromkeys(skills) if self.registry.contains(s)]

        # If for some reason a concept tag isn't in registry, fallback to root
        if not valid_concepts:
            valid_concepts = ["arithmetic"]
        if not valid_skills:
            valid_skills = ["skill.read_word_problem"]

        return TaggingResult(
            problem_id=problem_id,
            concepts=valid_concepts,
            skills=valid_skills,
            rule_version=RULE_VERSION,
            source="rule_based",
            confidence=confidence,
            evidence=evidence,
        )
