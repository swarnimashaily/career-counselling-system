"""Core evaluation logic for the career counselling system."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from .questionnaire import Option, Questionnaire


@dataclass(frozen=True)
class TraitProfile:
    """Aggregated trait scores for a learner."""

    scores: Dict[str, float]

    def top_traits(self, limit: int = 3) -> List[Tuple[str, float]]:
        """Return the dominant traits sorted by score."""

        return sorted(self.scores.items(), key=lambda item: item[1], reverse=True)[:limit]


@dataclass(frozen=True)
class Recommendation:
    """Represents a recommended career direction."""

    title: str
    summary: str
    strengths_alignment: List[str]
    starter_projects: List[str]
    learning_resources: List[str]


@dataclass(frozen=True)
class Evaluation:
    """Full evaluation for a learner."""

    learner_name: str
    headline: str
    traits: TraitProfile
    recommendations: Sequence[Recommendation]
    reflection_questions: Sequence[str]


class CareerCounsellor:
    """Evaluates questionnaire responses and produces guidance."""

    def __init__(self, questionnaire: Questionnaire | None = None) -> None:
        self.questionnaire = questionnaire or Questionnaire()
        self._career_library = _build_career_library()

    def evaluate(self, *, learner_name: str, responses: Dict[str, str]) -> Evaluation:
        """Evaluate a set of questionnaire responses."""

        self.questionnaire.validate(responses)
        traits = self._aggregate_traits(responses)
        ranked_paths = self._rank_paths(traits)
        recommendations = [self._create_recommendation(path) for path in ranked_paths[:3]]

        headline = self._compose_headline(learner_name, traits, recommendations)
        reflection_questions = _reflection_prompts(recommendations)

        return Evaluation(
            learner_name=learner_name,
            headline=headline,
            traits=TraitProfile(scores=traits),
            recommendations=recommendations,
            reflection_questions=reflection_questions,
        )

    def _aggregate_traits(self, responses: Dict[str, str]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        for question in self.questionnaire.questions():
            option = _option_by_id(question.options, responses[question.id])
            for trait, weight in option.weight.items():
                scores[trait] = scores.get(trait, 0.0) + weight
        return scores

    def _rank_paths(self, traits: Dict[str, float]) -> List["CareerPath"]:
        ranked = sorted(
            self._career_library,
            key=lambda path: path.match_score(traits),
            reverse=True,
        )
        return ranked

    def _create_recommendation(self, path: "CareerPath") -> Recommendation:
        return Recommendation(
            title=path.title,
            summary=path.description,
            strengths_alignment=path.strengths_alignment,
            starter_projects=path.starter_projects,
            learning_resources=path.learning_resources,
        )

    def _compose_headline(
        self, learner_name: str, traits: Dict[str, float], recommendations: Sequence[Recommendation]
    ) -> str:
        top_trait, top_score = max(traits.items(), key=lambda item: item[1])
        lead_recommendation = recommendations[0].title if recommendations else "new paths"
        return (
            f"{learner_name}, your top trait is {top_trait} ({top_score:.1f}) and "
            f"you're well suited for {lead_recommendation}."
        )


def _option_by_id(options: Sequence[Option], option_id: str) -> Option:
    for option in options:
        if option.id == option_id:
            return option
    raise ValueError(f"No option with id '{option_id}'")


@dataclass(frozen=True)
class CareerPath:
    title: str
    traits: Dict[str, float]
    description: str
    strengths_alignment: List[str]
    starter_projects: List[str]
    learning_resources: List[str]

    def match_score(self, trait_scores: Dict[str, float]) -> float:
        return sum(trait_scores.get(trait, 0.0) * weight for trait, weight in self.traits.items())


def _build_career_library() -> List[CareerPath]:
    return [
        CareerPath(
            title="Data & AI Explorer",
            traits={"analytical": 0.8, "technical": 0.7},
            description=(
                "You enjoy uncovering patterns and using technology to make sense of complex problems. "
                "Roles like data analyst, machine learning engineer, or AI ethicist can let you blend "
                "curiosity with impact."
            ),
            strengths_alignment=[
                "You naturally spot trends and question the status quo.",
                "You enjoy independent deep work and thoughtful experimentation.",
                "You like transforming messy information into useful insights.",
            ],
            starter_projects=[
                "Analyze open datasets (climate, education) and publish a short insight report.",
                "Build a simple machine learning model that solves a real-world student problem.",
                "Join a hackathon focused on ethical AI or social good.",
            ],
            learning_resources=[
                "Intro to Data Science with Python (Coursera)",
                "Kaggle Learn: Intro to Machine Learning",
                "AI Ethics case studies from the Montreal AI Ethics Institute",
            ],
        ),
        CareerPath(
            title="Digital Storyteller",
            traits={"creative": 0.9, "communication": 0.7},
            description=(
                "You bring ideas to life through words, visuals, or interactive media. "
                "Careers in content strategy, UX writing, or multimedia journalism help you build "
                "narratives that inspire action."
            ),
            strengths_alignment=[
                "You connect with audiences and translate complex topics into engaging stories.",
                "You experiment with formats—from podcasts to design mockups—to find the right voice.",
                "You notice the emotions behind people's experiences and reflect them back.",
            ],
            starter_projects=[
                "Launch a storytelling newsletter exploring student journeys in various fields.",
                "Prototype a multimedia portfolio site highlighting causes you care about.",
                "Volunteer with a local nonprofit to amplify their mission through social media.",
            ],
            learning_resources=[
                "Google UX Writing Fundamentals",
                "Storytelling for Influence (IDEO U)",
                "Build a Personal Brand on Social Media (LinkedIn Learning)",
            ],
        ),
        CareerPath(
            title="Community Impact Navigator",
            traits={"social": 0.8, "communication": 0.6},
            description=(
                "You thrive when empowering others and building supportive spaces. "
                "Roles in community management, education, or talent development let you guide "
                "people toward growth."
            ),
            strengths_alignment=[
                "You facilitate discussions that help peers discover their strengths.",
                "You design inclusive experiences where everyone feels seen.",
                "You excel at translating feedback into programs that drive impact.",
            ],
            starter_projects=[
                "Start a peer mentoring circle focused on goal setting and accountability.",
                "Design a workshop to help classmates explore future career paths.",
                "Coordinate a service project that addresses a local need.",
            ],
            learning_resources=[
                "Coaching Skills for Leaders (edX)",
                "Community Management Fundamentals (CMX)",
                "Designing Learning Experiences (IDEO U)",
            ],
        ),
        CareerPath(
            title="Product Innovator",
            traits={"technical": 0.7, "practical": 0.6},
            description=(
                "You enjoy turning ideas into tangible solutions and iterating quickly. "
                "Product management, innovation strategy, or entrepreneurship paths help you "
                "launch meaningful products."
            ),
            strengths_alignment=[
                "You balance big-picture vision with pragmatic experimentation.",
                "You love mapping user needs and crafting solutions that evolve with feedback.",
                "You are energized by dynamic environments and collaborative building.",
            ],
            starter_projects=[
                "Design a lean canvas for a product addressing a student life challenge.",
                "Join a product sprint or startup weekend to practice rapid prototyping.",
                "Build a low-code MVP and test it with potential users.",
            ],
            learning_resources=[
                "Product Strategy by Reforge",
                "Lean Startup principles (Eric Ries)",
                "Figma Community for prototyping inspiration",
            ],
        ),
        CareerPath(
            title="Sustainable Builder",
            traits={"practical": 0.8, "creative": 0.5},
            description=(
                "You like working with your hands and seeing real-world change. "
                "Careers in sustainable engineering, urban planning, or environmental design "
                "combine tangible impact with creativity."
            ),
            strengths_alignment=[
                "You think in systems and care about long-term impact on people and planet.",
                "You enjoy learning by doing and iterating on physical or spatial prototypes.",
                "You balance functionality with aesthetics when solving problems.",
            ],
            starter_projects=[
                "Prototype a sustainable product or service for your campus.",
                "Volunteer with an urban garden or green building initiative.",
                "Document how local infrastructure could become more climate resilient.",
            ],
            learning_resources=[
                "Introduction to Sustainable Design (Coursera)",
                "Open Source Ecology projects",
                "Sustainable Cities MOOC (edX)",
            ],
        ),
    ]


def _reflection_prompts(recommendations: Sequence[Recommendation]) -> Sequence[str]:
    prompts = [
        "What parts of the recommended roles excite you the most and why?",
        "How do these paths align with the impact you want to have on others?",
        "What is one experiment you could run this month to learn more?",
    ]
    if recommendations:
        prompts.append(
            f"Who could you reach out to for an informational chat about {recommendations[0].title}?"
        )
    return prompts
