from __future__ import annotations

import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OllamaJSONClient:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        temperature: float = 0,
        timeout_seconds: int = 900,
        think: bool = False,
        num_predict: int = 2048,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        self.think = think
        self.num_predict = num_predict

    def generate_json(self, model: str, system: str, user: str) -> dict[str, Any]:
        content = self._chat(model, system, user)
        try:
            return _parse_json_object(content)
        except (json.JSONDecodeError, ValueError):
            repaired = _try_local_json_repair(content)
            if repaired is not None:
                return repaired
            repair_prompt = (
                "Fix this malformed JSON and return only one valid JSON object. "
                "Do not add explanations, markdown, or extra keys. Keep the same schema and data.\n\n"
                f"{content}"
            )
            repaired_content = self._chat(
                model=model,
                system="You repair malformed JSON. Return only valid compact JSON.",
                user=repair_prompt,
            )
            return _parse_json_object(repaired_content)

    def _chat(self, model: str, system: str, user: str) -> str:
        payload = {
            "model": model,
            "stream": False,
            "think": self.think,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {"temperature": self.temperature, "num_predict": self.num_predict},
            "format": "json",
        }
        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            detail = _extract_error_detail(body) or exc.reason
            raise RuntimeError(
                f"Ollama request failed for model '{model}' with HTTP {exc.code}: {detail}. "
                f"Check `ollama list` and pull the configured model if needed."
            ) from exc
        except URLError as exc:
            raise RuntimeError(
                f"Could not reach Ollama at {self.base_url}. Start Ollama and pull the configured model."
            ) from exc

        message = raw.get("message", {})
        if isinstance(message, dict):
            content = message.get("content")
            if content:
                return str(content)
        response = raw.get("response")
        if response:
            return str(response)
        thinking = message.get("thinking") if isinstance(message, dict) else None
        if thinking:
            raise RuntimeError(
                "Ollama returned thinking output but no JSON content. "
                "Set run.ollama_think: false or update Ollama if the model ignores `think: false`."
            )
        return ""


def _parse_json_object(content: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    cleaned = _strip_code_fence(cleaned)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        extracted = _extract_balanced_json_object(cleaned)
        if extracted is None:
            raise ValueError(f"LLM did not return a JSON object: {content[:500]}")
        parsed = json.loads(extracted)
    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")
    return parsed


def _try_local_json_repair(content: str) -> dict[str, Any] | None:
    cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    cleaned = _strip_code_fence(cleaned)
    extracted = _extract_balanced_json_object(cleaned) or cleaned
    array_repair = _repair_top_level_object_array(extracted)
    if array_repair is not None:
        return array_repair
    candidates = [
        extracted,
        re.sub(r",\s*([}\]])", r"\1", extracted),
        re.sub(r"}\s*{", "},{", extracted),
    ]
    candidates.append(re.sub(r",\s*([}\]])", r"\1", candidates[-1]))
    completed = _complete_truncated_json(extracted)
    if completed is not None:
        candidates.extend(
            [
                completed,
                re.sub(r",\s*([}\]])", r"\1", completed),
            ]
        )
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _repair_top_level_object_array(content: str) -> dict[str, Any] | None:
    match = re.search(r'^\s*\{\s*"(?P<key>[^"]+)"\s*:\s*\[', content)
    if match is None:
        return None
    key = match.group("key")
    index = match.end()
    items: list[dict[str, Any]] = []
    while index < len(content):
        next_start = content.find("{", index)
        if next_start == -1:
            break
        raw_item = _extract_balanced_json_object(content[next_start:])
        if raw_item is None:
            break
        normalized = re.sub(r",\s*([}\]])", r"\1", raw_item)
        try:
            parsed = json.loads(normalized)
        except json.JSONDecodeError:
            break
        if isinstance(parsed, dict):
            items.append(parsed)
        index = next_start + len(raw_item)
    if not items:
        return None
    return {key: items}


def _complete_truncated_json(content: str) -> str | None:
    stack: list[str] = []
    in_string = False
    escape = False
    for char in content:
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            stack.append("}")
        elif char == "[":
            stack.append("]")
        elif char in ("}", "]"):
            if not stack or stack[-1] != char:
                return None
            stack.pop()
    if in_string or not stack:
        return None
    completed = re.sub(r",\s*$", "", content.strip())
    return completed + "".join(reversed(stack))


def _strip_code_fence(content: str) -> str:
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", content, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else content


def _extract_balanced_json_object(content: str) -> str | None:
    start = content.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(content)):
        char = content[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return content[start : index + 1]
    return None


def _extract_error_detail(body: str) -> str | None:
    if not body:
        return None
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return body[:500]
    if isinstance(parsed, dict):
        error = parsed.get("error")
        if error:
            return str(error)
    return body[:500]
