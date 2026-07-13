from dataclasses import dataclass


@dataclass
class GraphSummary:

    entity_count: int
    edge_count: int
    relation_counts: dict[str, int]

    top_relations: list[tuple[str, int]]