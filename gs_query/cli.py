"""CLI de gs_query: python -m gs_query "terminos" --domain CDxx --severity alta --max 5"""

from __future__ import annotations

import argparse
import json
import sys

from gs_query.search import search


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gs_query")
    parser.add_argument("query", help="Terminos de busqueda")
    parser.add_argument("--domain", default=None, help="Filtra por dominio canonico (CDxx)")
    parser.add_argument("--severity", default=None, help="Filtra por severidad (alta/media/baja/high/medium/low)")
    parser.add_argument("--max", type=int, default=5, dest="max_results")
    args = parser.parse_args(argv)

    results = search(
        args.query, domain=args.domain, severity=args.severity, max_results=args.max_results
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
