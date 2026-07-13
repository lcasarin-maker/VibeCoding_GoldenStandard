"""gs_query: CLI + servidor MCP de busqueda lexica sobre el catalogo GS
(GS-03/GS-MCP-001). Sin embeddings, sin red."""

from gs_query.search import search

__all__ = ["search"]
