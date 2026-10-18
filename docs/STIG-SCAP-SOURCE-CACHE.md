# Official STIG + SCAP source cache for near-instant Rule retrieval

**2026-10-18 · Design / pilot contract · [issue #2](https://github.com/vanderpol/scap-ng-editor-sample-data/issues/2).** Not a claim that a complete live source cache or automated publisher refresh currently exists.

## Product goal

**A user types one STIG Rule identifier; the authoring editor retrieves one small, already indexed Rule packet from public GitHub.** Neither the agent nor the editor downloads or unzips publisher STIG/SCAP packages, parses huge XML streams, resolves OVAL graphs or traverses thousands of files **during routine authoring**.

Target **cache lookup + relevant source packet delivery under 2 seconds** on reasonably connected clients (measured separately in ChatGPT/VS Code), with no fixed promise for AI generation. The agent must show a usable draft/view before deep related-content research. Serve ordinary Rule text + OVAL entry graph from predictable GitHub.com text/JSON file paths, with no GitHub Actions artifact or external binary host needed on the request path.

## Two distinct official source families, one lookup

| Input | Source | Parse and precompute | Author-facing view |
| --- | --- | --- | --- |
| **Manual STIG XCCDF ZIP** | Verified, publisher-issued DISA Cyber Exchange artifact from `cyber.mil` | Benchmark/Group/Rule hierarchy, `SV-...r..._rule`, `V-...`, `CCI-...`, title, severity, discussion, check text, fix text, check-content refs, STIG ID, revision/version | Official *manual requirement and check* |
| **SCAP benchmark (data stream ZIP/XML + component OVAL)** | **Separate** verified publisher-issued SCAP content ZIP from `cyber.mil` when available | SCAP datastream and component index; Rule ↔ check-content-ref ↔ OVAL Definition ↔ Tests ↔ Objects ↔ States ↔ Variables (plus OVAL local/global components, Sets, Filters, function dependencies); selectors/identities; source components and per-reference provenance | Exact automated source graph/OVAL logic, not an AI recreation |
| **Reviewed SCAP-NG derived content** | Separate, version-pinned project sources | Existing Assessment + shared assessment/collection graph, selected grammar profile | Reuse/modernize NG authoring, not an official source claim |

**Never merge manual-STIG and SCAP Rule records solely by title/CCI/SV prefix.** Their publications and release cycles may differ. Preserve each origin/version independently; show `manual version X` and `SCAP stream version Y`. Record an exact Rule ID and crosswalk with confidence/provenance; unmatched or conflicting pairs are **review required** rather than forced.

## Read path (precomputed, versioned)

```text
source-cache/
  README.md
  manifest.json                # last verified release pointers; tiny
  lookups/
    by-rule-id/<safe-id>.json   # immutable-ish locator record for a Rule version/benchmark
    by-vuln-id/<safe-id>.json   # alternate keys, no guessing
  releases/
    <publisher-release>/<benchmark-id>/<revision>/
      source.json              # official ZIP names/sha256, issue/retrieval data, component hashes
      rules/<safe-id>.json     # compact Rule packet with manual + available SCAP source refs
      oval/<definition-id>.json # resolved source graph and normalized pointer map
      original/               # optional extracted *unaltered* text components; see file sizes
```

These are **illustrative target paths**, not files already generated. Prefer a manifest lookup or one predictable path followed by **one small Rule packet**. Canonical IDs must be encoded safely and include benchmark identity/revision; `SV-...` is not globally unique across releases. Keep old snapshots available; update `manifest.json` atomically *after* full validation to prevent inconsistent lookups.

A Rule packet should include `record_type`, `benchmark_id`, `rule_id`, `vuln_id`, `publication_version`, `publisher=DISA`, `source_kind=manual-xccdf|scap-datastream`, `artifact_sha256`, original exact source path / element identifier, parser version, **source evidence availability**, and links to both checked raw component and optimized per-Rule data. Include a compact `status`: `official-verified`, `project-derived`, `unverified-upload`, `missing`, `source-version-mismatch`; a project cache by itself never changes publisher identity.

## Controlled refresh pipeline (not per user request)

1. A **maintainer-controlled** scheduled release check or manual trigger discovers publisher notices at **cyber.mil**; do not fall back to STIGViewer.com or treat it as official.
2. Download each official ZIP **once per changed publisher release**. Verify allowed official URL/redirect host and TLS, source identity, hashes, file size/extraction limits and XML hardening; retain original SHA-256, original bytes in a permitted artifact store and reproducible extraction metadata. Avoid unsafe `extractall` and unbounded entity expansion.
3. Normalize XCCDF and SCAP datastream/OVAL into **separate linked source records**, preserve original XPath/element IDs/markup and all OVAL dependency edges. Direct lookup must not have to recursively compute the graph.
4. Validate: unique identities per benchmark/revision, reference closure, OVAL cyclic/unknown dependencies reported explicitly, nested Groups, Rule alias mapping, changed/removed Rule differential report, original-versus-extracted provenance and limits.
5. Publish immutable content paths and a short index/manifest on **GitHub.com** only **after** review/green gates. The agent receives `cache_generation_sha` and source-packet hash. Keep previous generations and benchmark releases readable.
6. Scheduled checks alone are not actual background progress in this chat. GitHub Actions automation and public-source legal/redistribution assessment must be implemented, reviewed and enabled separately. Consider repository/LFS/release size constraints and public GitHub API rate limiting.

## Important boundaries

- **Read source from this verified cache by default.** If the requested official manual/SCAP release isn't present, label `NOT IN VERIFIED CACHE`. User can upload an official ZIP or the maintainer can prepare a refresh; no silent third-party mirror substitution.
- **Official publisher remains DISA**; cache is a pinned verified copy. The project SCAP-NG authoring examples and derived optimized Assessment files are not a second publisher.
- **Do not discard original OVAL structure as meaningless complexity.** An optimized JSON dependency closure may be more convenient for AI, but preserve exact source graph IDs, cardinality, function expansion, XML namespace, check binding and component provenance for review/lossless source alignment.
- **Do not confuse parsed graph availability with result semantics.** AI proposes content; deterministic syntax tooling diagnoses structure; tested scanner evaluator alone reports Assessment outcomes.
- **Offline support:** the same immutable cache-generation pack must be exportable/importable to air-gapped VS Code users with no network or cloud model required.
- **No work for the user's AI quota per lookup** beyond a tiny indexed text retrieval. The goal is to make first render and basic edit operations ordinary deterministic I/O, not ChatGPT Work research.

## Acceptance pilot

- Preprocessing program supports both classes with explicit capability coverage, plus strict ZIP/XML rejection tests.
- One verified **real manual XCCDF** publisher ZIP and one **real SCAP stream** publisher ZIP are imported; original counts/text/refs independently checked. Do not say these have been ingested until files and hashes are recorded.
- Direct per-rule lookups verified on simple Linux and complex Windows cases; exact requested Rule identifiers mapped to correct stream/revision.
- Benchmark measured for *cache-hit lookup and rule display* separately from AI prose generation, on GitHub.com and an offline local pack. Aim at <2s for cache-hit delivery; report percentile/conditions and cache-miss experience transparently.
- Test version mismatches, missing OVAL references, external component paths, ZIP bombs, duplicate IDs, malformed XML, source version mismatch and unreleased publication.
- Production cache home remains to be decided. `vanderpol/scap-content` is **private** and unsuitable as the only source for a public anonymous agent; this repo is a useful pilot, but a **dedicated verified-source public repository** is preferable once the parser/refresh contract is established.

Related [public trust policy](https://github.com/vanderpol/scap-ng/blob/main/docs/public-authoring/AUTHORITATIVE-STIG-SOURCES.md), [editor fast-first #8](https://github.com/vanderpol/scap-ng-editor/issues/8), and [Board demo #6](https://github.com/vanderpol/scap-ng-editor/issues/6).
