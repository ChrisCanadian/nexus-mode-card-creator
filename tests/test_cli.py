import json
from pathlib import Path
import tempfile
import unittest
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mode_card_creator.card import ModeCard
from mode_card_creator.cli import confirm_generated_card, main


ANSWERS = [
    "Stress-test architecture",
    "A skeptical reviewer",
    "It catches assumptions",
    "Actively stress-test",
    "Direct and technical",
    "Evidence-first",
    "Separate fact from intent",
    "Do not flatter",
    "Do not fabricate evidence",
    "Stress-test this; what am I missing; what is assumed",
]

VALID_MODEL_OUTPUT = json.dumps({
    "name": "Architecture Auditor",
    "description": "Stress-tests architecture.",
    "role": "Act as a skeptical reviewer.",
    "instructions": ["One", "Two", "Three", "Four", "Five"],
    "communication_style": ["Direct"],
    "boundaries": ["Do not fabricate evidence."],
    "conversation_starters": ["Test this.", "What is weak?", "What is assumed?"],
})


class CliTests(unittest.TestCase):
    def test_default_handoff_path_writes_prompt_without_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "handoff.md"
            with patch("builtins.input", side_effect=ANSWERS):
                rc = main(["--handoff-output", str(output)])
            self.assertEqual(rc, 0)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Mode Card Creator", text)
            self.assertIn("HOST-AUTHORITY BASELINE", text)

    def test_call_model_does_not_save_without_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_output = Path(tmp) / "mode_card.json"
            md_output = Path(tmp) / "mode_card.md"
            with patch("builtins.input", side_effect=ANSWERS + [""]), \
                 patch("mode_card_creator.cli.call_openai_compatible", return_value=VALID_MODEL_OUTPUT):
                rc = main(["--call-model", "--json-output", str(json_output), "--markdown-output", str(md_output)])
            self.assertEqual(rc, 3)
            self.assertFalse(json_output.exists())
            self.assertFalse(md_output.exists())

    def test_call_model_saves_after_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_output = Path(tmp) / "mode_card.json"
            md_output = Path(tmp) / "mode_card.md"
            with patch("builtins.input", side_effect=ANSWERS + ["yes"]), \
                 patch("mode_card_creator.cli.call_openai_compatible", return_value=VALID_MODEL_OUTPUT):
                rc = main(["--call-model", "--json-output", str(json_output), "--markdown-output", str(md_output)])
            self.assertEqual(rc, 0)
            self.assertTrue(json_output.exists())
            self.assertTrue(md_output.exists())


class ConfirmationTests(unittest.TestCase):
    def _card(self):
        return ModeCard.from_dict({
            "name": "Architecture Auditor",
            "description": "Stress-tests architecture.",
            "role": "Act as a skeptical reviewer.",
            "instructions": ["One", "Two", "Three", "Four", "Five"],
            "communication_style": ["Direct"],
            "boundaries": ["Do not fabricate evidence."],
            "conversation_starters": ["Test this.", "What is weak?", "What is assumed?"],
        })

    def test_confirmation_accepts_yes(self):
        output = []
        self.assertTrue(confirm_generated_card(self._card(), input_fn=lambda _: "yes", output_fn=output.append))
        self.assertTrue(any("Generated Mode Card draft" in line for line in output))

    def test_confirmation_rejects_default_no(self):
        self.assertFalse(confirm_generated_card(self._card(), input_fn=lambda _: "", output_fn=lambda _: None))


if __name__ == "__main__":
    unittest.main()
