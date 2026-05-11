from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    passed: bool
    score: float = Field(ge=0, le=100)
    category: str
    findings: List[str]
    recommendations: List[str]


class RAGEvaluationRequest(BaseModel):
    question: str
    expected_answer_contains: List[str]
    retrieved_context: str
    model_answer: str
    sources: List[str]


class ExtractionEvaluationRequest(BaseModel):
    input_text: str
    expected_output: Dict[str, Any]
    model_output: Dict[str, Any]
    required_fields: Optional[List[str]] = None


class AgentEvaluationRequest(BaseModel):
    user_request: str
    expected_action: str
    expected_requires_approval: bool
    agent_output: Dict[str, Any]


class BatchEvaluationRequest(BaseModel):
    rag_cases: List[RAGEvaluationRequest] = []
    extraction_cases: List[ExtractionEvaluationRequest] = []
    agent_cases: List[AgentEvaluationRequest] = []


class BatchEvaluationResult(BaseModel):
    total_cases: int
    passed_cases: int
    failed_cases: int
    average_score: float
    results: List[EvaluationResult]