"""FastAPI application exposing the career counselling engine."""
from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from career_counselling import CareerCounsellor, Questionnaire
from career_counselling.genai import compose_full_report

app = FastAPI(title="Career Counselling GenAI Platform", version="1.0.0")

questionnaire = Questionnaire()
counsellor = CareerCounsellor(questionnaire)


class OptionModel(BaseModel):
    id: str = Field(..., description="Option identifier")
    label: str = Field(..., description="User-facing label")


class QuestionModel(BaseModel):
    id: str
    prompt: str
    options: List[OptionModel]


class EvaluationRequest(BaseModel):
    learner_name: str = Field(..., description="Name to personalize guidance")
    responses: Dict[str, str] = Field(..., description="Mapping of question id to option id")


class RecommendationModel(BaseModel):
    title: str
    summary: str
    strengths_alignment: List[str]
    starter_projects: List[str]
    learning_resources: List[str]


class EvaluationResponse(BaseModel):
    headline: str
    trait_scores: Dict[str, float]
    recommendations: List[RecommendationModel]
    reflection_questions: List[str]
    narrative_report: str


@app.get("/questionnaire", response_model=List[QuestionModel])
def get_questionnaire() -> List[QuestionModel]:
    """Return the questionnaire definitions."""

    return [
        QuestionModel(
            id=question.id,
            prompt=question.prompt,
            options=[OptionModel(id=option.id, label=option.label) for option in question.options],
        )
        for question in questionnaire.questions()
    ]


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    """Evaluate questionnaire responses for a learner."""

    try:
        evaluation = counsellor.evaluate(
            learner_name=request.learner_name,
            responses=request.responses,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EvaluationResponse(
        headline=evaluation.headline,
        trait_scores=evaluation.traits.scores,
        recommendations=[
            RecommendationModel(
                title=item.title,
                summary=item.summary,
                strengths_alignment=item.strengths_alignment,
                starter_projects=item.starter_projects,
                learning_resources=item.learning_resources,
            )
            for item in evaluation.recommendations
        ],
        reflection_questions=list(evaluation.reflection_questions),
        narrative_report=compose_full_report(evaluation),
    )
