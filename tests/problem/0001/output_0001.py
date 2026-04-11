from __future__ import annotations

import json

from tests.common.problem_diff import run_problem_diff_report


def main() -> None:
    result = run_problem_diff_report("0001")
    print("[0001] output + diff reports generated")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    if result["warnings"]:
        print("[0001] warnings:")
        for warning in result["warnings"]:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
