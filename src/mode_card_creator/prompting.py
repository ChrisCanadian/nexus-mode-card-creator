from __future__ import annotations

from .interview import InterviewAnswer


GOVERNANCE_BASELINE = """HOST-AUTHORITY BASELINE
The Mode Card is a behavioral profile, not an authority grant. Do not encode instructions that claim to override the host application's safety rules, truthfulness/factuality requirements, permissions, protected boundaries, tool controls, or higher-priority platform/system instructions. Preserve stylistic intent without inventing authority."""

HOST_CAPABILITY_BASELINE = """HOST-CAPABILITY BASELINE
Do not assume the host has browsing, citations, memory, tools, or any other optional capability. If the user's desired behavior depends on a host capability, phrase it conditionally (for example: 'cite reliable sources when the host supports research/citations'). Do not infer user preferences from tools or memory that are not represented in the interview."""


def build_synthesis_prompt(answers: list[InterviewAnswer]) -> str:
    answer_block = "\n".join(f"- {a.label}: {a.value}" for a in answers)
    return f"""You are converting a user interview into a portable Mode Card.

{GOVERNANCE_BASELINE}

{HOST_CAPABILITY_BASELINE}

Interview:
{answer_block}

Return ONLY valid JSON with exactly these keys:
name, description, role, instructions, communication_style, boundaries, conversation_starters

Contract:
- name: non-empty string, max 80 characters
- description: non-empty string, max 500 characters
- role: non-empty string, max 500 characters
- instructions: 5-12 non-empty behavioral instruction strings
- communication_style: 1-12 non-empty strings
- boundaries: 1-12 non-empty strings
- conversation_starters: 3-6 non-empty realistic prompt strings
- no extra fields
- do not invent model weights, memory controls, runtime activation, tool permissions, database identifiers, or host-runtime implementation details
- do not claim the Mode Card grants authority over host safety, truth, permissions, tools, or protected boundaries
- host-dependent behaviors such as browsing, citations, memory, or tool use must be written conditionally unless the interview explicitly establishes the target host capability

Resolve minor ambiguity conservatively from the interview. If a material ambiguity cannot be resolved from the answers, phrase the card so it does not invent a preference.
"""
