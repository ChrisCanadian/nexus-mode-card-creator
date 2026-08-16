# Public Boundary

This repository is intentionally a **creator only**.

The publication boundary is the finished Mode Card.

```text
user idea
   ↓
guided creator
   ↓
validated Mode Card
   ↓
STOP
```

## Allowed in the public repository

- natural-language interview questions,
- adaptive interview guidance,
- public Mode Card fields,
- prompt generation for the creator itself,
- schema/shape validation,
- Markdown/JSON rendering,
- optional generic model invocation,
- examples,
- tests for the creator,
- **public, host-agnostic boundary language stating that a behavioral profile does not override higher-authority safety, truth, permissions, or protected boundaries.**

That final item is a statement about the limits of the **card**, not an implementation of governance.

## Explicitly excluded

Do not add any of the following to this repository:

- host-runtime mode activation,
- automatic mode detection,
- mode selection logic,
- database schemas used by a private runtime,
- user or identity join keys,
- numeric trait/gauge weights,
- formulas, thresholds, interpolation, scoring, or pressure math,
- precedence or conflict-resolution logic between private runtime state layers,
- state reconstruction,
- prompt assembly order,
- context selection,
- memory retrieval or learned-preference interaction,
- canonical identity composition,
- tool availability or execution logic,
- governance or advisory-system integration,
- production configuration,
- private behavioral profiles,
- private prompts,
- internal runtime diagrams that reveal how a host consumes the card.

## Review rule

If a proposed file or feature answers this question:

> “How does the private host runtime make a Mode Card consequential?”

it does not belong in this repository.

If it answers only:

> “How can a person create a useful portable Mode Card?”

it is probably in scope.

## Governance wording rule

It is safe to say:

> “A Mode Card must not claim to override the host system's safety, truthfulness, permissions, protected boundaries, tool controls, or higher-priority instructions.”

It is **not** safe, within this repository's intended boundary, to explain how a specific host implements those controls, how precedence is calculated, how permissions are stored, or how a mode is composed into a live runtime.

## Sanitization is not enough

Renaming private tables, fields, classes, formulas, or prompt sections is not sufficient if the resulting artifact still teaches the private runtime method.

The safe abstraction is **creation**, not a generalized copy of runtime consumption.
