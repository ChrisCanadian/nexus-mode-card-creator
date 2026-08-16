# Security Notes

Mode Card Creator is intentionally small and has no persistent server component.

## Credentials

The optional provider path reads:

- `MODE_CARD_API_BASE`
- `MODE_CARD_API_KEY`
- `MODE_CARD_MODEL`

The API key is sent as a Bearer credential to the configured API base URL. Use only a provider/endpoint you trust. Never commit real credentials.

## User content

Generated Mode Cards and interview handoffs may contain personal or work-related preferences. Treat them as user content. Generated default output names are excluded by `.gitignore`.

## Host capabilities

The AI-native protocol does not require or grant browsing, citations, memory, or tool access. If a host assistant provides those capabilities, the host application's own permissions and policies remain authoritative. The creator should not silently use host memory/tools to infer user preferences that were not supplied in the interview.

## Scope

This project does not grant permissions, execute host tools, mutate host state, or implement host governance. A Mode Card is configuration text only.
