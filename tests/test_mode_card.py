import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mode_card_creator.card import CONSTRAINTS, PUBLIC_FIELDS, ModeCard, ValidationError, parse_mode_card_json
from mode_card_creator.interview import InterviewAnswer
from mode_card_creator.prompting import build_synthesis_prompt


def valid_payload():
    return {
        "name": "Architecture Auditor",
        "description": "Stress-tests technical architecture.",
        "role": "Act as a skeptical but constructive reviewer.",
        "instructions": [
            "Separate implementation from intent.",
            "Surface assumptions.",
            "Prefer evidence.",
            "Preserve uncertainty.",
            "Challenge conclusions proportionally."
        ],
        "communication_style": ["Direct", "Conversational"],
        "boundaries": ["Do not fabricate evidence."],
        "conversation_starters": ["Stress-test this.", "What am I missing?", "What is only assumed?"]
    }


class ModeCardTests(unittest.TestCase):
    def test_valid_round_trip(self):
        card = ModeCard.from_dict(valid_payload())
        self.assertEqual(ModeCard.from_dict(json.loads(card.to_json())), card)

    def test_rejects_unknown_fields(self):
        data = valid_payload()
        data["activation_weight"] = 0.9
        with self.assertRaises(ValidationError):
            ModeCard.from_dict(data)

    def test_rejects_missing_fields(self):
        data = valid_payload()
        del data["role"]
        with self.assertRaises(ValidationError):
            ModeCard.from_dict(data)

    def test_rejects_too_few_instructions(self):
        data = valid_payload()
        data["instructions"] = ["One", "Two", "Three", "Four"]
        with self.assertRaises(ValidationError):
            ModeCard.from_dict(data)

    def test_rejects_wrong_conversation_starter_count(self):
        data = valid_payload()
        data["conversation_starters"] = ["Only one"]
        with self.assertRaises(ValidationError):
            ModeCard.from_dict(data)

    def test_parse_fenced_json(self):
        text = "```json\n" + json.dumps(valid_payload()) + "\n```"
        self.assertEqual(parse_mode_card_json(text).name, "Architecture Auditor")

    def test_rejects_non_json_model_output(self):
        with self.assertRaises(ValidationError):
            parse_mode_card_json("Here is your mode card: great job!")

    def test_rendering(self):
        card = ModeCard.from_dict(valid_payload())
        self.assertIn("## Boundaries", card.to_markdown())
        self.assertIn('"conversation_starters"', card.to_json())

    def test_synthesis_prompt_contains_governance_and_public_contract(self):
        answers = [InterviewAnswer("purpose", "Audit architecture")]
        prompt = build_synthesis_prompt(answers)
        self.assertIn("behavioral profile, not an authority grant", prompt)
        self.assertIn("Do not assume the host has browsing, citations, memory, tools", prompt)
        self.assertIn("written conditionally", prompt)
        self.assertIn("5-12", prompt)
        self.assertIn("3-6", prompt)
        self.assertNotIn("UserModes", prompt)
        self.assertNotIn("SSR", prompt)

    def test_json_schema_parity_with_python_validator(self):
        schema = json.loads((ROOT / "mode_card.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(tuple(schema["required"]), PUBLIC_FIELDS)
        self.assertFalse(schema["additionalProperties"])
        self.assertNotIn("$id", schema)

        props = schema["properties"]
        self.assertEqual(props["instructions"]["minItems"], CONSTRAINTS["instructions"]["min_items"])
        self.assertEqual(props["instructions"]["maxItems"], CONSTRAINTS["instructions"]["max_items"])
        self.assertEqual(props["conversation_starters"]["minItems"], CONSTRAINTS["conversation_starters"]["min_items"])
        self.assertEqual(props["conversation_starters"]["maxItems"], CONSTRAINTS["conversation_starters"]["max_items"])
        self.assertEqual(props["boundaries"]["minItems"], CONSTRAINTS["boundaries"]["min_items"])
        self.assertEqual(props["boundaries"]["maxItems"], CONSTRAINTS["boundaries"]["max_items"])

        for field in ("name", "description", "role"):
            self.assertEqual(props[field]["maxLength"], CONSTRAINTS[field]["max_length"])

    def test_example_validates(self):
        data = json.loads((ROOT / "examples" / "architecture_auditor.json").read_text(encoding="utf-8"))
        card = ModeCard.from_dict(data)
        self.assertEqual(card.name, "Architecture Auditor")


if __name__ == "__main__":
    unittest.main()
