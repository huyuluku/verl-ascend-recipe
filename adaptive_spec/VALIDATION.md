# Validation

## Public candidate validation (2026-10-19)

The recipe's executable source, tests and configuration are unchanged from
private-source commit `6ef655072dedb79d26bcb4782ad29eebcbe96518`.
The new branch starts at upstream `26590228c049126644e82389da67b30b416ddfae`.
Only this validation note, the recipe index and unit-test discovery are added
around that extracted recipe.

Local Windows checks used Python 3.12.14 and the upstream-pinned Ruff 0.14.10:

- `PYTHONPATH=adaptive_spec python -m pytest tests/ adaptive_spec/tests/ -q --tb=short`:
  **398 passed** (331 upstream + 67 recipe), no skips.
- `python -m ruff check .`: passed.
- `python -m ruff format --check .`: passed, 189 files formatted.
- Python 3.10 syntax parsing: passed; this is not a Python 3.10 runtime execution.
- `python -m build --outdir ../validation/dist adaptive_spec`: wheel and sdist built.
- The built wheel was installed into a fresh isolated environment with `--no-index --no-deps`.
  Disabled-plugin import and both plugin entry-point loads passed without importing
  torch, Ray, vLLM or vLLM-Ascend.

The first local build used `--no-isolation` in a pre-existing test environment
without setuptools and failed before building. The normal isolated build above
installed its declared build backend and passed; no source fix was needed.

No new framework, training, device-generation or performance run was performed
for this public candidate. Full verl/Ray execution, optional Elastic device
integration, quality checks and matched package throughput remain pending.
This submission is a Draft for author and maintainer review.

## Historical provenance (2026-10-09)

The following checks were recorded for the private delivery at commit
`6ef655072dedb79d26bcb4782ad29eebcbe96518`, extracted from community base
`1028677a58172f26714640d2ce994eac4f20744a`. They are not new device
measurements of this public PR. Raw receipts remain outside the package.

## CPU and packaging validation

Local checks used Python 3.12.14 and Ruff 0.14.10:

- 331 upstream tests and 67 recipe tests passed (398 total).
- Six additional, out-of-repository historical-oracle tests passed: 32,000 stabilization
  steps and 7,680 posterior/scoring queries. The aggregate is 404 tests. These compare
  normal-lifecycle components, not an entire historical runner replay.
- Ruff lint/format checks and Python 3.10 syntax parsing passed.
- Wheel and sdist builds passed. A separate wheel installation exercised the documented
  context-builder, plan-only and replay commands, then loaded the generated map into the
  actual controller and made an Engine decision.
- Replay records are CPU fixtures, explicitly marked as non-device measurements; their
  emitted runtime is disabled. They are not performance evidence.

Public verl contracts were inspected at the REQUIRED_VERL pin. Acquire/release methods
were exercised with a CPU protocol simulator, not a real Ray actor. The private CI runs
all 67 recipe tests on Python 3.10 and 3.12; check the workflow for the commit being reviewed.

## Bounded device validation

Offline collection completed on a source-verified Ascend 0.23 environment with Qwen3.5-9B,
TP2, K5/K7, two states (B1/L256 and B2/L512), one repeat and 64-token continuations.
Both depths completed all states (six responses total). Every state/depth retained more
than the required two clean decode steps. The collector generated a directly loadable
phase map and matching enabled runtime configuration. Plan-only was also exercised on
that environment. The backend was vLLM 0.23.0 and vLLM-Ascend
0.23.0rc2.dev1+g5ed283a6c.d20260719, with exact supported runner fingerprints.

The generated map was then used for a bounded native vLLM online-plugin test: two sibling
responses, 32 tokens each, eager async scheduling, TP2 and startup MTP capacity K7.
This is a short integration check, not a complete verl/Ray rollout, quality evaluation,
representative calibration grid or throughput comparison. Read-only worker RPC on the final wheel confirmed the adapter was installed on
both TP workers, physical/drafted K was 5, each controller made 12 decisions and
recorded 18 evidence blocks. The trusted callable RPC permission was limited to
this isolated validation process; production configuration does not enable it.
Receipts and raw logs are retained outside the distributed package.

Collection used the calibration-r3 wheel. The final wheel differs in the collector only
by streaming file hashing/JSONL reading; the observer and device probe code are unchanged.
Final CLI/artifact tests exercise those I/O changes. Failed environment/script setup
attempts and their logs remain in private local/server validation directories; they are
not counted as passed device experiments and are not shipped.

## Evidence limits

Full supported-stack verl/Ray execution, optional Elastic device integration and matched
package throughput measurements remain pending. Existing CPU router regressions do not
establish end-to-end device performance. Historical gains came from a customized
rollout-only experiment stack without actor weight updates; some historical runs used
K11, which this package excludes. Do not attribute those gains to the extracted recipe.
