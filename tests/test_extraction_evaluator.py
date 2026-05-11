from app.evaluators.extraction_evaluator import evaluate_extraction_output
from app.schemas import ExtractionEvaluationRequest


def test_extraction_evaluator_passes_matching_output():
    request = ExtractionEvaluationRequest(
        input_text="Invoice #1234 for $250 due on 2026-05-30.",
        expected_output={
            "invoice_number": "1234",
            "amount": 250,
            "due_date": "2026-05-30",
        },
        model_output={
            "invoice_number": "1234",
            "amount": 250,
            "due_date": "2026-05-30",
        },
    )

    result = evaluate_extraction_output(request)

    assert result.passed is True
    assert result.score == 100


def test_extraction_evaluator_flags_missing_field():
    request = ExtractionEvaluationRequest(
        input_text="Invoice #1234 for $250 due on 2026-05-30.",
        expected_output={
            "invoice_number": "1234",
            "amount": 250,
            "due_date": "2026-05-30",
        },
        model_output={
            "invoice_number": "1234",
            "amount": 250,
        },
    )

    result = evaluate_extraction_output(request)

    assert result.passed is False
    assert result.score < 100