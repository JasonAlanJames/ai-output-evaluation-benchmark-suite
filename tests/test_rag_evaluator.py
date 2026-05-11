from app.evaluators.rag_evaluator import evaluate_rag_answer
from app.schemas import RAGEvaluationRequest


def test_rag_evaluator_passes_grounded_answer():
    request = RAGEvaluationRequest(
        question="What is the refund policy?",
        expected_answer_contains=["30 days", "receipt"],
        retrieved_context="Customers may request a refund within 30 days with a receipt.",
        model_answer="Customers may request a refund within 30 days if they have a receipt.",
        sources=["refund-policy.pdf"],
    )

    result = evaluate_rag_answer(request)

    assert result.passed is True
    assert result.score >= 80
    assert result.category == "rag"


def test_rag_evaluator_flags_missing_sources():
    request = RAGEvaluationRequest(
        question="What is the refund policy?",
        expected_answer_contains=["30 days", "receipt"],
        retrieved_context="Customers may request a refund within 30 days with a receipt.",
        model_answer="Customers may request a refund within 30 days.",
        sources=[],
    )

    result = evaluate_rag_answer(request)

    assert result.passed is False
    assert result.score < 80