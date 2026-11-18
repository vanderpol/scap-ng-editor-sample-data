# SCAP-NG language features vs OVAL Self-Assertion — 2026-11-18

**Scope:** native 0.4.1 authoring/evaluation features that cannot be qualified *solely* from original OVAL Test/Definition content. An existing OVAL analogue does not test native wire shape, editor save semantics, policy integration, or Result provenance. Positive files below are **authored test candidates**, not RI PASS receipts.

| Feature / normative locus | Covered by OVAL original? | New native fixture(s) | Remaining acceptance |
|---|---|---|---|
| Ordered Evaluate `if / then / else_if / else` — `expression.schema.json` | No native equivalent | `assessments/conditional-ordered.assessment.yaml`; mutation vectors | Branch-only execution, no skipped collection, UNKNOWN/ERROR guard, nested branches, Result trace |
| Optional organizational Input presence `input_provided` and provided-empty distinction | No | `assessments/optional-input-presence.assessment.yaml` (exact canonical example); `semantic-negative/unguarded-optional-input.assessment.yaml` | Invocation bindings, absence/empty/wrong type; editor guard dominance |
| Explicit `not_applicable` vs `not_evaluated` authored leaves | Source OVAL status analogue only, not this authoring grammar | `assessments/conditional-not-applicable.assessment.yaml` | Ensure canonical six-state Assessment/Rule translation and no fabricated compliance |
| Manual Assessment response choices and evidence guidance | No: OVAL Self-Assertion is automated | `assessments/manual-review.assessment.yaml` | Editor manual UI and normalized human outcome; RI must not auto-execute |
| Cross-Assessment dependencies and conditional reuse | OVAL Definitions reference other Definitions but not NG's Assessment package contract | `assessments/referenced-baseline.assessment.yaml`, `assessments/conditional-dependency.assessment.yaml` | Package resolution, version pins, cycles, reuse by target/snapshot/authority |
| Shared Object scoping, refactor and identity | OVAL Objects exist; NG authored scope/new one-line selector form differs | `assessments/shared-object-reuse.assessment.yaml`; `semantic-negative/dangling-shared-object.assessment.yaml` | Reference rename/update, validation, source identity, single acquisition and separated contexts |
| Require nested `one` vs `xor`, independent Item/field cardinality | OVAL analogue; no full native schema validation from OVAL-only runs | `assessments/require-one-versus-xor.assessment.yaml` | Nested TRUE/FALSE/UNKNOWN/ERROR, typed field/value cardinality, SQLite parity |
| Native Set/Filter include/exclude and nested operands | OVAL analogue; NG syntax has no named State registry | `assessments/set-filter-difference.assessment.yaml` | Supplied Items and complete/denied population, nested set, identity/dedup, pushdown parity |
| Benchmark/Group/Rule source-local and inherited applicability | OVAL Test content has no XCCDF policy inheritance | `policy/benchmark-applicability-profiles.benchmark.yaml`, `policy/*.rule.yaml`, `policy/applicability-catalog.yaml`, `applicability/inheritance-vector.json` | Build verified package, execute condition Assessments, ancestor AND / same-level OR and profile-disabled separate |
| Independent native Profile `disabled_rules` vs XCCDF Profile extends | No | Two Profiles in policy Benchmark | Profile selection and omitted/not_applicable/not_evaluated distinction |
| Rule Assessment choice and manual/automated mode | No Benchmark/Rule layer in OVAL corpus | Two Rules in `policy/`; `manual-review` | Alternate choices, input binding and manual scheduling in package |
| Explicit reporting `reported_elements`, session/Rule/Assessment provenance, scan IDs and human explanations | OVAL output contract differs | All automated Assessment samples specify `reported_elements: all` | **Not yet a full Result-wire fixture**; RI #149 must add separate canonical Result success/held vectors |
| Variable scope, aliases, functions (`count`, `time_difference`, etc.) | **Yes** OVAL source Test content supplies an independent oracle for many functions | Native tests here use `variable.value` for platform neutrality | Continue pinned OVAL Self-Assertion and current RI variable conformance, don't duplicate bulk corpus |
| Proposed collection-expansion `foreach` | Not an OVAL 5.12.3 language feature; native `foreach_binding` exists only as schema `$defs` scaffolding | `negative/unapproved-foreach.assessment.yaml` | **Normative owner decision required:** [scap-ng #76](https://github.com/vanderpol/scap-ng/issues/76); design positive examples only AFTER approved grammar; no RI-only DSL |
| YAML editor preservation, dropdown/enums, branch ordering, undo/redo, hidden defaults | No | All `assessments/`, intentional negatives, legacy `fixtures/source-preservation/` | Extension Host and native YAML/graphical regression in [scap-ng-vscode #61](https://github.com/vanderpol/scap-ng-vscode/issues/61) |

## Truth and qualification levels

1. **Authored** — the new document exists with separate analytical expectation; not a runtime result.
2. **Schema-valid** — the exact frozen 0.4.1 checkout validates the document. Required before merging PR.
3. **Core-executable** — RI executes its common engine against typed synthetic evidence, yielding independently compared expected outcomes and decisive reasons.
4. **Package/external-scope** — loader, dependency reuse, Benchmark applicability/Profile and canonical Results pass integration tests with declared security scope.
5. **Editor-preserved** — graphical and YAML round-trip, no-op bytes, Undo/Redo and deliberate invalid diagnostics tested.
6. **Host/source-equivalent** — requires an authentic source witness/host authority; **not claimed by these synthetic fixtures**.

Historical 0.4.0 files remain in `fixtures/current-v04/`, explicitly not part of current schema admissions. No original Self-Assertion expected outcomes were edited.

## Next independent test content

RI should add compact canonical Result documents for session/Rule/Assessment status and evidence provenance once it establishes a correct schema-conformant writer. The editor should add generated controls for all approved conditional branches, manual responses and policy layers, while protecting malformed authoring text. A current-schema `foreach` positive fixture is intentionally **blocked**, not omitted by accident.
