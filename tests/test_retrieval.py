from src.retrieval import EmbeddingProvider, match_requirements_to_solutions
from src.schemas import Requirement, Solution


def requirement(text: str) -> Requirement:
    return Requirement(
        requirement_id="REQ-0001",
        statement=text,
        source_transcript="biz",
        source_quote=text,
        source_line_range=(1, 1),
    )


def solution(identifier: str, text: str) -> Solution:
    return Solution(
        solution_id=identifier,
        what=text,
        source_transcript="eng",
        source_quote=text,
        source_line_range=(1, 1),
    )


def test_obvious_hashing_match_is_retrieved() -> None:
    provider = EmbeddingProvider(provider="hashing")
    matches = match_requirements_to_solutions(
        [requirement("passwordless login for enterprise users")],
        [
            solution("SOL-1", "email magic link passwordless login implementation"),
            solution("SOL-2", "monthly CSV billing export"),
        ],
        provider,
        top_k=1,
        min_score=0.1,
    )
    assert matches[0].candidate_solutions[0].solution_id == "SOL-1"


def test_top_k_and_min_score_respected() -> None:
    provider = EmbeddingProvider(provider="hashing")
    matches = match_requirements_to_solutions(
        [requirement("audit logs retention")],
        [
            solution("SOL-1", "audit logs retention policy"),
            solution("SOL-2", "audit log storage"),
            solution("SOL-3", "unrelated dashboard rendering"),
        ],
        provider,
        top_k=2,
        min_score=0.2,
    )
    assert len(matches[0].candidate_solutions) <= 2
    assert all(match.score >= 0.2 for match in matches[0].matches)


def test_unrelated_item_filtered_by_score() -> None:
    provider = EmbeddingProvider(provider="hashing")
    matches = match_requirements_to_solutions(
        [requirement("passwordless login")],
        [solution("SOL-1", "warehouse forklifts maintenance")],
        provider,
        top_k=1,
        min_score=0.5,
    )
    assert matches[0].candidate_solutions == []

