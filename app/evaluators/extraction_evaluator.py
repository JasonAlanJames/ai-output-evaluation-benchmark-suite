from typing import Any

from app.schemas import EvaluationResult, ExtractionEvaluationRequest
from app.scoring.scoring_rules import calculate_score, passed_threshold


def _values_match(expected: Any, actual: Any) -> bool:
    if isinstance(expected, str) and isinstance(actual, str):
        return expected.strip().lower() == actual.strip().lower()

    return expected == actual


def evaluate_extraction_output(request: ExtractionEvaluationRequest) -> EvaluationResult:
    findings = []
    recommendations = []

    required_fields = request.required_fields or list(request.expected_output.keys())

    total_checks = len(required_fields) + len(request.expected_output) + 1
    passed_checks = 0

    if isinstance(request.model_output, dict):
        passed_checks += 1
        findings.append("Model output is valid JSON/dictionary structure.")
    else:
        findings.append("Model output is not a valid dictionary structure.")
        recommendations.append("Enforce structured JSON output with a schema.")

    for field in required_fields:
        if field in request.model_output:
            passed_checks += 1
            findings.append(f"Required field present: {field}.")
        else:
            findings.append(f"Required field missing: {field}.")
            recommendations.append(f"Ensure extraction prompt requires the '{field}' field.")

    for key, expected_value in request.expected_output.items():
        actual_value = request.model_output.get(key)

        if _values_match(expected_value, actual_value):
            passed_checks += 1
            findings.append(f"Field '{key}' matched expected value.")
        else:
            findings.append(
                f"Field '{key}' mismatch. Expected '{expected_value}', got '{actual_value}'."
            )
            recommendations.append(f"Improve extraction accuracy for field '{key}'.")

    score = calculate_score(total_checks, passed_checks)

    return EvaluationResult(
        passed=passed_threshold(score),
        score=score,
        category="structured_extraction",
        findings=findings,
        recommendations=recommendations,
    )