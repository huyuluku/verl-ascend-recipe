"""Create a hash-bound D2 report; never fit on the validation JSONL.

Run externally after fitting a candidate, then atomically publish --output.
The caller is responsible for recording forecasts before observing responses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4

from .length_scheduler.d2_quality import make_validation_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--rows", required=True, help="Held-out pre-rollout predictions and completed lengths, JSONL")
    parser.add_argument("--trained-through-epoch", type=int, required=True)
    parser.add_argument("--validation-epoch", type=int, required=True)
    parser.add_argument("--risk-weight", type=float, default=0.5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(args.rows).read_bytes()
    report = make_validation_report(
        [json.loads(line) for line in source.splitlines() if line.strip()],
        checkpoint=args.checkpoint,
        trained_through_epoch=args.trained_through_epoch,
        validation_epoch=args.validation_epoch,
        risk_weight=args.risk_weight,
    )
    report["validation_rows_sha256"] = hashlib.sha256(source).hexdigest()
    destination = Path(args.output)
    temporary = destination.with_name(f"{destination.name}.tmp-{uuid4().hex}")
    temporary.write_text(json.dumps(report, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, destination)


if __name__ == "__main__":
    main()
