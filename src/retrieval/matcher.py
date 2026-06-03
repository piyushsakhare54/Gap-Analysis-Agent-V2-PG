from __future__ import annotations

from src.retrieval.embeddings import EmbeddingProvider
from src.retrieval.vector_index import VectorIndex
from src.schemas import Requirement, RequirementMatchSet, RetrievalMatch, Solution


def match_requirements_to_solutions(
    requirements: list[Requirement],
    solutions: list[Solution],
    embedding_provider: EmbeddingProvider,
    top_k: int = 5,
    min_score: float = 0.15,
) -> list[RequirementMatchSet]:
    solution_texts = [_solution_text(solution) for solution in solutions]
    solution_vectors = embedding_provider.embed_texts(solution_texts) if solutions else []
    index = VectorIndex()
    index.add(solutions, solution_vectors)

    match_sets: list[RequirementMatchSet] = []
    for requirement in requirements:
        query_vector = embedding_provider.embed_texts([_requirement_text(requirement)])[0]
        hits = [(solution, score) for solution, score in index.search(query_vector, top_k) if score >= min_score]
        matches = [
            RetrievalMatch(
                requirement_id=requirement.requirement_id,
                solution_id=solution.solution_id,
                score=score,
                reason=f"Cosine similarity {score:.3f}",
            )
            for solution, score in hits
        ]
        match_sets.append(
            RequirementMatchSet(
                requirement=requirement,
                matches=matches,
                candidate_solutions=[solution for solution, _ in hits],
            )
        )
    return match_sets


def _requirement_text(requirement: Requirement) -> str:
    return " ".join([requirement.statement, *requirement.constraints, *requirement.notes])


def _solution_text(solution: Solution) -> str:
    return " ".join([solution.what, *solution.scope_limits, *solution.tech_stack, *solution.deferred])

