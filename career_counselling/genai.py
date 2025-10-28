"""Lightweight generative utilities to craft narrative feedback."""
from __future__ import annotations

from textwrap import dedent

from .engine import Evaluation, Recommendation


def compose_full_report(evaluation: Evaluation) -> str:
    """Produce a narrative summary of the evaluation."""

    intro = dedent(
        f"""
        Hey {evaluation.learner_name},
        Here's a quick look at how your strengths and motivations can shape your next steps.
        {evaluation.headline}
        """
    ).strip()

    trait_lines = [
        "Top strengths: "
        + ", ".join(f"{trait} ({score:.1f})" for trait, score in evaluation.traits.top_traits())
    ]

    recommendation_sections = [
        _describe_recommendation(index + 1, recommendation)
        for index, recommendation in enumerate(evaluation.recommendations)
    ]

    reflection_section = "Reflection prompts:\n- " + "\n- ".join(evaluation.reflection_questions)

    return "\n\n".join([intro, *trait_lines, *recommendation_sections, reflection_section])


def _describe_recommendation(position: int, recommendation: Recommendation) -> str:
    strengths = "\n".join(f"    • {item}" for item in recommendation.strengths_alignment)
    projects = "\n".join(f"    • {item}" for item in recommendation.starter_projects)
    resources = "\n".join(f"    • {item}" for item in recommendation.learning_resources)

    return dedent(
        f"""
        Option {position}: {recommendation.title}
        Why it fits:
        {strengths}
        Try this next:
        {projects}
        Keep exploring with:
        {resources}
        """
    ).strip()
