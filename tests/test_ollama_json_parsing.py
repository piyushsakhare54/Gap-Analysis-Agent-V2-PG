from src.agents.ollama_client import OllamaJSONClient, _try_local_json_repair


def test_local_json_repair_adds_missing_array_comma() -> None:
    malformed = '{"requirements": [{"statement": "one"} {"statement": "two"}]}'
    parsed = _try_local_json_repair(malformed)
    assert parsed is not None
    assert len(parsed["requirements"]) == 2


def test_local_json_repair_removes_trailing_commas() -> None:
    malformed = '{"requirements": [{"statement": "one",},],}'
    parsed = _try_local_json_repair(malformed)
    assert parsed == {"requirements": [{"statement": "one"}]}


def test_local_json_repair_closes_truncated_object_array() -> None:
    truncated = '{"requirements": [{"statement": "one"}, {"statement": "two"},'
    parsed = _try_local_json_repair(truncated)
    assert parsed == {"requirements": [{"statement": "one"}, {"statement": "two"}]}


def test_local_json_repair_salvages_valid_array_items_before_malformed_item() -> None:
    malformed = (
        '{"solutions": ['
        '{"what": "one", "notes": []},'
        '{"what": "two", "notes": []},'
        '{"what": "broken" "notes": []}'
        "]}"
    )
    parsed = _try_local_json_repair(malformed)
    assert parsed == {"solutions": [{"what": "one", "notes": []}, {"what": "two", "notes": []}]}


def test_generate_json_retries_on_value_error() -> None:
    class DummyClient:
        def _chat(self, model: str, system: str, user: str) -> str:
            if "malformed JSON" in user:
                return '{"requirements": [{"statement": "fixed", "source_quote": "fixed", "line_start": 1, "line_end": 1, "confidence": 0.9, "constraints": [], "notes": []}]}'
            return 'this is not json at all'

    client = DummyClient()  # type: ignore[arg-type]
    parsed = OllamaJSONClient.generate_json(client, model="test", system="sys", user="usr")
    assert parsed == {
        "requirements": [
            {
                "statement": "fixed",
                "source_quote": "fixed",
                "line_start": 1,
                "line_end": 1,
                "confidence": 0.9,
                "constraints": [],
                "notes": [],
            }
        ]
    }
