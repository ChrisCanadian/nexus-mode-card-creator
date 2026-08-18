# Nexus Mode Card Creator

A small, model-agnostic tool for turning a natural-language description of desired AI behavior into a portable **Mode Card**: a custom-assistant-style configuration containing a name, description, role, instructions, communication style, boundaries, and conversation starters.

This repository intentionally stops at **creation**.

It does **not** implement runtime activation, persistence, behavioral injection, state reconstruction, weighting, scoring, identity composition, memory integration, tool routing, governance integration, or any other host-runtime behavior.

## Origin

**Nexus Mode Card Creator** is a deliberately bounded public artifact derived from behavioral-mode authoring work explored during development of **Nexus Synapse**. The creator is standalone and model-agnostic; the `nexus-` repository name preserves its project lineage without exposing the private Nexus runtime.

This repository exposes the **creation experience only**. Nexus runtime activation, state reconstruction, adaptation, governance, and behavioral integration are not included.

## Two ways to use it

### 1. No-code / bring-your-own AI

Give `MODE_CREATOR.md` to a capable AI assistant and ask it to run the creator with you.

The assistant should:

1. explain the creator briefly,
2. ask whether you want to begin,
3. interview you conversationally,
4. resolve important ambiguity or contradictions,
5. summarize its understanding and ask for final confirmation,
6. output a finished Mode Card.

No API key, package installation, or hosted service is required.

### 2. Reference CLI

The Python reference implementation performs the same bounded job.

It can either:

- create a **handoff prompt** you can paste into any capable LLM, or
- optionally call an **OpenAI-compatible** endpoint if you configure one.

The code still stops after generating and validating the Mode Card.

```bash
python -m mode_card_creator.cli
```

Or, after installation:

```bash
mode-card-create
```

For an OpenAI-compatible endpoint:

```bash
export MODE_CARD_API_BASE="https://example.com/v1"
export MODE_CARD_API_KEY="..."
export MODE_CARD_MODEL="your-model"
mode-card-create --call-model
```

Environment variables are deliberately generic so the project is not tied to a specific model vendor.

> **Credential note:** the configured API credential is sent to the configured API base URL. Only use an endpoint/provider you trust. Never commit credentials to this repository.

## Host capabilities

The AI-native creator does **not** require tools, browsing, memory, or citation support.

If the host assistant provides those capabilities, they remain governed by the host application. The creator should not silently use host memory or external tools to infer preferences the user did not provide. If the user wants behaviors such as research, citations, browsing, or tool use represented in the final card, they should be written as **conditional preferences** rather than claims that the capability exists.

Example:

```text
Good: Cite reliable sources when the host supports research/citations.
Bad: You always have web access and may use any tool without restriction.
```

## Human confirmation

The AI-native protocol includes a final confirmation gate: before emitting the finished card, the assistant gives a short 2–5 bullet readback of the requested behavior and asks the user to confirm or correct it.

The optional direct-provider CLI path also asks for explicit confirmation before saving generated output. This is a creator-level approval step only; it is not host-runtime governance.

## Governance baseline

A Mode Card changes **behavioral posture**, not authority.

A generated card must not claim that it can override the host application's:

- safety rules,
- factual/truthfulness requirements,
- permissions or authorization boundaries,
- protected system boundaries,
- tool availability or execution rules,
- higher-priority platform/system instructions.

That rule is intentionally public and portable. It describes what a behavioral profile **must not supersede**; it does not disclose or implement any host governance mechanism.

## Output

A Mode Card is intentionally boring and portable:

```text
NAME
Architecture Auditor

DESCRIPTION
A rigorous technical thinking partner for stress-testing system designs.

ROLE
Act as a skeptical but constructive architecture reviewer.

INSTRUCTIONS
- Separate implemented behavior from intended behavior.
- Surface unsupported assumptions and hidden dependencies.
- Prefer evidence over confident narration.
- Challenge conclusions proportionally to the available evidence.
- Preserve useful uncertainty instead of forcing closure.

COMMUNICATION STYLE
- Direct
- Conversational
- Technically detailed when useful

BOUNDARIES
- Do not fabricate implementation evidence.
- Clearly distinguish fact from inference.
- Do not claim authority beyond what the host system actually grants.

CONVERSATION STARTERS
- Stress-test this architecture.
- What am I overlooking?
- Separate what is proven from what is assumed.
```

The machine that consumes that card is outside the scope of this project.

## Public boundary

The public artifact includes only:

- an AI-readable creator protocol,
- a small public Mode Card schema,
- a guided interview,
- a synthesis prompt builder,
- validation,
- rendering,
- an optional generic model call,
- tests.

It intentionally excludes:

- runtime activation or selection,
- numeric behavioral weights,
- formulas or scoring,
- state or context reconstruction,
- prompt ordering or assembly,
- persistence or private database schemas,
- identity precedence,
- memory or preference interaction,
- tool or governance integration,
- host-runtime wiring of any kind.

See `PUBLIC_BOUNDARY.md` for the explicit publication checklist.

## Privacy

Mode Cards may contain personal communication preferences, dislikes, work patterns, or other user-supplied material.

- Generated cards and interview handoffs are **user content**.
- The CLI does not persist them unless you explicitly choose an output file.
- Generated output files are ignored by Git by default.
- Do not commit a real user's Mode Card without their permission.

## Design principle

The project demonstrates one narrow idea:

> Let a language model do the fuzzy interpretation, then constrain the result to a small, inspectable configuration artifact.

It does not prescribe how a host system should make that artifact consequential.

## Repository layout

```text
MODE_CREATOR.md                 AI-native/no-code creator
mode_card.schema.json           Portable output contract
src/mode_card_creator/          Reference implementation
examples/                       Sample cards
PUBLIC_BOUNDARY.md              Explicit do-not-cross publication boundary
SECURITY.md                     Security and host-capability notes
CHANGELOG.md                    Public-scope revision history
```

## Qualitative pre-release exercise

Before the initial public release, the AI-native `MODE_CREATOR.md` flow was manually exercised with Perplexity. The reported exercise successfully followed the consent/opening flow, one-question-at-a-time interview, adaptive follow-ups, ambiguity handling, conflict-resolution guidance, and structured final output. The resulting feedback led to the host-tool, citation-capability, and explicit final-confirmation clarifications in v0.1.2.

This is **qualitative interoperability feedback, not automated conformance evidence or a benchmark**. That claim ceiling is intentionally preserved: this is not presented as a benchmark or formal cross-model conformance test.

## Tests

The unit suite runs directly from a fresh checkout on Windows, macOS, or Linux:

```bash
python -m unittest discover -s tests -v
```

The tests add the repository's `src/` directory to their import path explicitly, so no shell-specific `PYTHONPATH` setup is required.

## Attribution and provenance

See [`ATTRIBUTION.md`](ATTRIBUTION.md) for authorship, the behavioral-authoring lineage, AI-assistance boundaries, and permission scope.

## License

Released under the **MIT License**. Copyright © 2026 Christopher Campbell.

The MIT license applies to the material published in this repository. It does not grant rights to unpublished or separately licensed Nexus Synapse runtime code, private repositories, data, prompts, or other artifacts that are not included here. See `LICENSE` for the full terms.
