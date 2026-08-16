from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .card import ValidationError, parse_mode_card_json
from .interview import conduct_terminal_interview
from .prompting import build_synthesis_prompt
from .provider import ProviderError, call_openai_compatible


def confirm_generated_card(card, input_fn=None, output_fn=None) -> bool:
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print

    output_fn("\nGenerated Mode Card draft:")
    output_fn(f"- Name: {card.name}")
    output_fn(f"- Role: {card.role}")
    output_fn(f"- Instructions: {len(card.instructions)}")
    output_fn(f"- Boundaries: {len(card.boundaries)}")
    response = input_fn("Save this Mode Card? [y/N] ").strip().lower()
    return response in {"y", "yes"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a portable AI behavioral Mode Card.")
    parser.add_argument("--call-model", action="store_true", help="Call a configured OpenAI-compatible endpoint and render the returned card.")
    parser.add_argument("--handoff-output", default="mode_card_handoff.md", help="Output file for the no-provider handoff prompt.")
    parser.add_argument("--json-output", default="mode_card.json", help="JSON output path when --call-model is used.")
    parser.add_argument("--markdown-output", default="mode_card.md", help="Markdown output path when --call-model is used.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    answers = conduct_terminal_interview()
    prompt = build_synthesis_prompt(answers)

    if not args.call_model:
        path = Path(args.handoff_output)
        path.write_text("# Mode Card Creator — LLM Handoff\n\n" + prompt, encoding="utf-8")
        print(f"Created {path}")
        return 0

    try:
        raw = call_openai_compatible(prompt)
        card = parse_mode_card_json(raw)
    except (ProviderError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not confirm_generated_card(card):
        print("Mode Card was not saved. Re-run the creator and adjust your answers if you want to revise it.")
        return 3

    Path(args.json_output).write_text(card.to_json() + "\n", encoding="utf-8")
    Path(args.markdown_output).write_text(card.to_markdown(), encoding="utf-8")
    print(f"Created {args.json_output} and {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
