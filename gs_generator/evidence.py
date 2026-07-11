"""Evidence classification used by metrics and lint without changing wiki bytes."""


def classify_source(source: str) -> str:
    """Classify a catalog source with a deterministic, falsifiable heuristic."""
    value = str(source).strip().lower()
    if not value or value.startswith("pending:") or "pending" in value:
        return "pending"
    if "internal" in value or "cited generically" in value:
        return "internal-generic"
    return "primary"


def has_primary_evidence(item: dict) -> bool:
    return any(
        isinstance(ref, dict)
        and classify_source(ref.get("source", "")) == "primary"
        for ref in item.get("evidence", []) or []
    )
