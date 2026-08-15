from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InterviewAnswer:
    label: str
    value: str


QUESTIONS: tuple[tuple[str, str], ...] = (
    ("purpose", "What do you want this mode to be especially useful for?"),
    ("role", "What kind of collaborator or specialist should it act like?"),
    ("success", "What would make you say, 'Yes, that is exactly how I wanted it to behave'?"),
    ("challenge", "How much should it challenge you: supportive, neutral, skeptical, or actively stress-testing?"),
    ("style", "How should it communicate: direct/gentle, concise/detailed, conversational/formal, technical/plain-language?"),
    ("reasoning", "What reasoning posture should it prefer: evidence-first, exploratory, adversarial review, Socratic, generative, or something else?"),
    ("reliable", "What should it reliably do every time this mode is used?"),
    ("avoid", "What behaviors make an assistant less useful or annoy you?"),
    ("boundaries", "What should this mode avoid, refuse to pretend, or clearly label as uncertain?"),
    ("starters", "Give me a few realistic prompts you would use with this mode."),
)


def conduct_terminal_interview(input_fn=None, output_fn=None) -> list[InterviewAnswer]:
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print
    answers: list[InterviewAnswer] = []
    output_fn("Mode Card Creator — answer naturally. You can be brief or detailed.\n")
    for label, question in QUESTIONS:
        while True:
            value = input_fn(f"{question}\n> ").strip()
            if value:
                answers.append(InterviewAnswer(label=label, value=value))
                break
            output_fn("Please give at least a short answer.")
    return answers
