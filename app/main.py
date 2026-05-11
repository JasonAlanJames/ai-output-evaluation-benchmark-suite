from fastapi import FastAPI

from app.config import settings
from app.evaluators.agent_evaluator import evaluate_agent_decision
from app.evaluators.extraction_evaluator import evaluate_extraction_output
from app.evaluators.rag_evaluator import evaluate_rag_answer
from app.schemas import (
    AgentEvaluationRequest,
    BatchEvaluationRequest,
    BatchEvaluationResult,
    EvaluationResult,
    ExtractionEvaluationRequest,
    RAGEvaluationRequest,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A production-style benchmark suite for evaluating AI outputs across "
        "RAG systems, structured extraction APIs, and agentic workflows."
    ),
)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
    }


@app.post("/evaluate/rag-answer", response_model=EvaluationResult)
def evaluate_rag(request: RAGEvaluationRequest) -> EvaluationResult:
    return evaluate_rag_answer(request)


@app.post("/evaluate/json-extraction", response_model=EvaluationResult)
def evaluate_extraction(request: ExtractionEvaluationRequest) -> EvaluationResult:
    return evaluate_extraction_output(request)


@app.post("/evaluate/agent-decision", response_model=EvaluationResult)
def evaluate_agent(request: AgentEvaluationRequest) -> EvaluationResult:
    return evaluate_agent_decision(request)


@app.post("/evaluate/batch", response_model=BatchEvaluationResult)
def evaluate_batch(request: BatchEvaluationRequest) -> BatchEvaluationResult:
    results = []

    for case in request.rag_cases:
        results.append(evaluate_rag_answer(case))

    for case in request.extraction_cases:
        results.append(evaluate_extraction_output(case))

    for case in request.agent_cases:
        results.append(evaluate_agent_decision(case))

    total_cases = len(results)
    passed_cases = sum(1 for result in results if result.passed)
    failed_cases = total_cases - passed_cases
    average_score = round(
        sum(result.score for result in results) / total_cases,
        2,
    ) if total_cases else 0.0

    return BatchEvaluationResult(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        average_score=average_score,
        results=results,
    )