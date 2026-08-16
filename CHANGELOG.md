# Changelog

## v0.1.2 — 2026-08-15

Qualitative feedback from a manual Perplexity exercise of the AI-native protocol was incorporated without expanding the public runtime boundary.

### Changed

- clarified that tools, browsing, memory, and citations are optional host capabilities, not creator requirements,
- prohibited silent use of host memory/tools to infer unsupplied user preferences,
- required host-dependent behaviors to be expressed conditionally in generated cards,
- added a 2–5 bullet final readback and user-confirmation gate to `MODE_CREATOR.md`,
- added a save-confirmation gate to the optional direct-provider CLI path,
- documented the Perplexity exercise as qualitative feedback rather than benchmark/conformance evidence,
- expanded publication review checks for the new boundaries.

### Unchanged

The public Mode Card schema remains intentionally minimal. No version, tags, author notes, runtime activation, persistence, behavioral math, SSR/state reconstruction, tool wiring, governance wiring, or host-runtime consumption logic was added.

### Publication preparation

- Repository lineage finalized as `ChrisCanadian/nexus-mode-card-creator`.
- MIT License approved and added for the public repository.
- README now clarifies that the repository license does not extend to unpublished/private Nexus Synapse material.
- Unit-test discovery was made cross-platform so a fresh checkout can run the documented test command without shell-specific `PYTHONPATH` configuration.
