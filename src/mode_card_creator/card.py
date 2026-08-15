from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import re
from typing import Any

PUBLIC_FIELDS = (
    "name",
    "description",
    "role",
    "instructions",
    "communication_style",
    "boundaries",
    "conversation_starters",
)

CONSTRAINTS = {
    "name": {"min_length": 1, "max_length": 80},
    "description": {"min_length": 1, "max_length": 500},
    "role": {"min_length": 1, "max_length": 500},
    "instructions": {"min_items": 5, "max_items": 12, "item_max_length": 600},
    "communication_style": {"min_items": 1, "max_items": 12, "item_max_length": 200},
    "boundaries": {"min_items": 1, "max_items": 12, "item_max_length": 300},
    "conversation_starters": {"min_items": 3, "max_items": 6, "item_max_length": 300},
}


class ValidationError(ValueError):
    pass


def _clean_string(value: Any, field: str, *, max_length: int) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    value = value.strip()
    if not value:
        raise ValidationError(f"{field} must not be empty")
    if len(value) > max_length:
        raise ValidationError(f"{field} exceeds {max_length} characters")
    return value


def _clean_list(value: Any, field: str, *, min_items: int, max_items: int, item_max_length: int) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError(f"{field} must be a list")
    if not (min_items <= len(value) <= max_items):
        raise ValidationError(f"{field} must contain {min_items}-{max_items} items")
    cleaned: list[str] = []
    for index, item in enumerate(value):
        cleaned.append(_clean_string(item, f"{field}[{index}]", max_length=item_max_length))
    return cleaned


@dataclass(frozen=True)
class ModeCard:
    name: str
    description: str
    role: str
    instructions: list[str]
    communication_style: list[str]
    boundaries: list[str]
    conversation_starters: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModeCard":
        if not isinstance(data, dict):
            raise ValidationError("Mode Card must be a JSON object")

        keys = set(data)
        expected = set(PUBLIC_FIELDS)
        unknown = keys - expected
        missing = expected - keys
        if unknown:
            raise ValidationError(f"Unknown fields: {', '.join(sorted(unknown))}")
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(sorted(missing))}")

        return cls(
            name=_clean_string(data["name"], "name", max_length=CONSTRAINTS["name"]["max_length"]),
            description=_clean_string(data["description"], "description", max_length=CONSTRAINTS["description"]["max_length"]),
            role=_clean_string(data["role"], "role", max_length=CONSTRAINTS["role"]["max_length"]),
            instructions=_clean_list(data["instructions"], "instructions", **CONSTRAINTS["instructions"]),
            communication_style=_clean_list(data["communication_style"], "communication_style", **CONSTRAINTS["communication_style"]),
            boundaries=_clean_list(data["boundaries"], "boundaries", **CONSTRAINTS["boundaries"]),
            conversation_starters=_clean_list(data["conversation_starters"], "conversation_starters", **CONSTRAINTS["conversation_starters"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        def bullets(items: list[str]) -> str:
            return "\n".join(f"- {item}" for item in items)

        return (
            f"# {self.name}\n\n"
            f"## Description\n{self.description}\n\n"
            f"## Role\n{self.role}\n\n"
            f"## Instructions\n{bullets(self.instructions)}\n\n"
            f"## Communication Style\n{bullets(self.communication_style)}\n\n"
            f"## Boundaries\n{bullets(self.boundaries)}\n\n"
            f"## Conversation Starters\n{bullets(self.conversation_starters)}\n"
        )


def _strip_fenced_json(text: str) -> str:
    text = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    return text


def parse_mode_card_json(text: str) -> ModeCard:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError("Model output is empty")
    candidate = _strip_fenced_json(text)
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Model output is not valid JSON: {exc.msg}") from exc
    return ModeCard.from_dict(data)
