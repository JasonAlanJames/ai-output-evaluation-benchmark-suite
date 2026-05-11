from app.schemas import EvaluationResult, RAGEvaluationRequest
from app.scoring.scoring_rules import (
    calculate_score,
    contains_required_terms,
    missing_required_terms,
    passed_threshold,
)


def evaluate_rag_answer(request: RAGEvaluationRequest) -> EvaluationResult:
    findings = []
    recommendations = []

    total_checks = 5
    passed_checks = 0

    matched_terms = contains_required_terms(
        request.model_answer,
        request.expected_answer_contains,
    )

    missing_terms = missing_required_terms(
        request.model_answer,
        request.expected_answer_contains,
    )

    if matched_terms:
        passed_checks += 1
        findings.append(f"Model answer included expected terms: {matched_terms}.")
    else:
        findings.append("Model answer did not include expected answer terms.")
        recommendations.append("Improve answer completeness by using retrieved context more directly.")

    if not missing_terms:
        passed_checks += 1
        findings.append("Model answer included all expected terms.")
    else:
        findings.append(f"Model answer missed expected terms: {missing_terms}.")
        recommendations.append("Review chunking, retrieval quality, or prompt instructions.")

    if request.retrieved_context.strip():
        passed_checks += 1
        findings.append("Retrieved context was provided.")
    else:
        findings.append("No retrieved context was provided.")
        recommendations.append("Ensure the RAG pipeline returns relevant context before generation.")

    if request.sources:
        passed_checks += 1
        findings.append("Sources were provided.")
    else:
        findings.append("No sources were provided.")
        recommendations.append("Include source citations to improve answer trustworthiness.")

    context_lower = request.retrieved_context.lower()
    answer_lower = request.model_answer.lower()

    grounded_terms = [
        term for term in request.expected_answer_contains
        if term.lower() in context_lower and term.lower() in answer_lower
    ]

    if grounded_terms:
        passed_checks += 1
        findings.append(f"Answer appears grounded in retrieved context for terms: {grounded_terms}.")
    else:
        findings.append("Answer grounding could not be confirmed from retrieved context.")
        recommendations.append("Add stronger source-grounding checks or citation-level validation.")

    score = calculate_score(total_checks, passed_checks)

    return EvaluationResult(
        passed=passed_threshold(score),
        score=score,
        category="rag",
        findings=findings,
        recommendations=recommendations,
    )