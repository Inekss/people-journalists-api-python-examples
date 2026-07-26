"""Run People and Journalists resolve-then-filter examples."""

from __future__ import annotations

import json
import sys

from perigon_examples import PerigonClient, ResolveJournalistExample, ResolvePersonExample
from perigon_examples.errors import PerigonError


def main() -> int:
    try:
        with PerigonClient() as client:
            person = ResolvePersonExample(client).run()
            journalist = ResolveJournalistExample(client).run()
    except PerigonError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("=== Resolve person -> Articles (personWikidataId) ===")
    print(json.dumps(person, indent=2, ensure_ascii=False))
    print()
    print("=== Resolve journalist -> Articles (journalistId) ===")
    print(json.dumps(journalist, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
