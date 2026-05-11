from typing import List


def calculate_score(total_checks: int, passed_checks: int) -> float:
    if total_checks == 0:
        return 0.0

    return round((passed_checks / total_checks) * 100, 2)


def passed_threshold(score: float, threshold: float = 80.0) -> bool:
    return score >= threshold


def contains_required_terms(text: str, required_terms: List[str]) -> List[str]:
    lower_text = text.lower()

    return [
        term for term in required_terms
        if term.lower() in lower_text
    ]


def missing_required_terms(text: str, required_terms: List[str]) -> List[str]:
    lower_text = text.lower()

    return [
        term for term in required_terms
        if term.lower() not in lower_text
    ]