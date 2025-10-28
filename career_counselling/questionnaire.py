"""Questionnaire definitions for the career counselling engine."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class Option:
    """Represents a multiple-choice option."""

    id: str
    label: str
    weight: Dict[str, float]


@dataclass(frozen=True)
class Question:
    """Represents a questionnaire item."""

    id: str
    prompt: str
    options: Sequence[Option]


class Questionnaire:
    """Provides access to the counselling questionnaire."""

    _questions: Sequence[Question]

    def __init__(self) -> None:
        self._questions = _build_questions()

    def questions(self) -> Sequence[Question]:
        """Return the questions in order."""

        return self._questions

    def question_ids(self) -> List[str]:
        """Return the stable question identifiers."""

        return [question.id for question in self._questions]

    def validate(self, responses: Dict[str, str]) -> None:
        """Validate that the provided responses are complete and valid."""

        missing = [qid for qid in self.question_ids() if qid not in responses]
        if missing:
            raise ValueError(f"Missing responses for: {', '.join(missing)}")

        for question in self._questions:
            if responses[question.id] not in {option.id for option in question.options}:
                raise ValueError(
                    f"Invalid option '{responses[question.id]}' for question '{question.id}'."
                )


def _build_questions() -> Sequence[Question]:
    """Create the base questionnaire."""

    return [
        Question(
            id="strength",
            prompt="Which statement best describes your current strengths?",
            options=[
                Option(
                    id="analytical",
                    label="I enjoy solving complex problems and working with data.",
                    weight={"analytical": 1.0, "technical": 0.5},
                ),
                Option(
                    id="creative",
                    label="I like creating content, telling stories, or designing experiences.",
                    weight={"creative": 1.0, "communication": 0.5},
                ),
                Option(
                    id="supportive",
                    label="I thrive when helping others grow and collaborating on teams.",
                    weight={"social": 1.0, "communication": 0.5},
                ),
                Option(
                    id="practical",
                    label="I prefer hands-on work where I can see tangible results quickly.",
                    weight={"practical": 1.0, "technical": 0.5},
                ),
            ],
        ),
        Question(
            id="values",
            prompt="What motivates you most in a future career?",
            options=[
                Option(
                    id="impact",
                    label="Making a positive impact on society and individuals.",
                    weight={"social": 0.8, "creative": 0.4},
                ),
                Option(
                    id="innovation",
                    label="Inventing new solutions or working with cutting-edge technology.",
                    weight={"technical": 0.8, "analytical": 0.6},
                ),
                Option(
                    id="security",
                    label="Having stability, clear expectations, and predictable routines.",
                    weight={"practical": 0.9},
                ),
                Option(
                    id="expression",
                    label="Having the freedom to express myself and explore ideas.",
                    weight={"creative": 0.8, "communication": 0.4},
                ),
            ],
        ),
        Question(
            id="environment",
            prompt="What environment do you picture yourself thriving in?",
            options=[
                Option(
                    id="team",
                    label="Collaborating in cross-functional teams with lots of communication.",
                    weight={"social": 0.9, "communication": 0.7},
                ),
                Option(
                    id="independent",
                    label="Working independently where I can focus deeply for long periods.",
                    weight={"analytical": 0.7, "technical": 0.6},
                ),
                Option(
                    id="dynamic",
                    label="Fast-paced spaces where priorities can change often.",
                    weight={"technical": 0.5, "practical": 0.6},
                ),
                Option(
                    id="studio",
                    label="Creative studios or workshops where I build and experiment.",
                    weight={"creative": 0.7, "practical": 0.6},
                ),
            ],
        ),
        Question(
            id="learning",
            prompt="How do you prefer to learn new skills?",
            options=[
                Option(
                    id="courses",
                    label="Structured courses with clear milestones and feedback.",
                    weight={"analytical": 0.6, "practical": 0.4},
                ),
                Option(
                    id="projects",
                    label="Working on personal projects that let me explore on my own.",
                    weight={"creative": 0.5, "technical": 0.6},
                ),
                Option(
                    id="people",
                    label="Learning through conversations, mentorship, or coaching others.",
                    weight={"social": 0.7, "communication": 0.6},
                ),
                Option(
                    id="hands-on",
                    label="Trying things out physically and iterating quickly.",
                    weight={"practical": 0.7, "technical": 0.4},
                ),
            ],
        ),
    ]
