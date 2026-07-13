#!/usr/bin/env python3
"""Servidor MCP (stdio) de gs_query, mismo patron que
cerberus_mcp_server.py: FastMCP con un tool que expone la busqueda lexica
sobre el catalogo GS. Sin red, sin embeddings (GS-03/GS-MCP-001)."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from gs_query.search import search

mcp = FastMCP(
    "gs_query",
    instructions=(
        "Busca en el catalogo Golden Standard (vices, principios, tokenomics, "
        "vectores adversariales) por termino lexico. Sin red, sin embeddings."
    ),
)


@mcp.tool(description="Busca reglas del catalogo GS por termino, con filtro opcional de dominio/severidad.")
def gs_query(query: str, domain: str = "", severity: str = "", max_results: int = 5) -> list[dict]:
    return search(
        query,
        domain=domain or None,
        severity=severity or None,
        max_results=max_results,
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
