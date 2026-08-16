from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    pass


def call_openai_compatible(prompt: str, *, api_base: str | None = None, api_key: str | None = None, model: str | None = None, timeout: float = 60.0) -> str:
    base = (api_base or os.getenv("MODE_CARD_API_BASE") or "").rstrip("/")
    key = api_key or os.getenv("MODE_CARD_API_KEY") or ""
    model_name = model or os.getenv("MODE_CARD_MODEL") or ""

    if not base:
        raise ProviderError("MODE_CARD_API_BASE is required for --call-model")
    if not key:
        raise ProviderError("MODE_CARD_API_KEY is required for --call-model")
    if not model_name:
        raise ProviderError("MODE_CARD_MODEL is required for --call-model")

    payload = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Return only the requested JSON object."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{base}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        raise ProviderError(f"Provider call failed: {exc}") from exc

    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ProviderError("Provider response did not contain choices[0].message.content") from exc
