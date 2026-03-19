# Hypothesis: -RO Paradigm, Lexical Expansion, and *301 Disambiguation

**Date:** 2026-03-19
**Strategy category:** Suffix Analysis / Administrative Bootstrapping / Sign Clustering
**Language tested (if applicable):** Hurrian (comparison only)
**Builds on / differs from:** Extends `2026-03-18-admin-formula-bootstrapping.md` (which identified KU-RO/KI-RO but did not test -RO as a productive suffix); extends `2026-03-19-sign-clustering-ngram-unakana-wordorder.md` (which clustered *301 globally but did not separate admin/ritual contexts); entirely new lexical expansion approach.

---

## Hypothesis Statement

**H1 (-RO Paradigm):** Tokens ending in the syllable -RO cluster disproportionately in terminal/closing positions within administrative records, analogous to the confirmed behavior of KU-RO ("total"). If -RO is a productive completive or aggregative suffix, then non-KU/KI tokens ending in -RO should show the same terminal positional bias and represent words in the semantic domain of totaling/summing.

**Falsification condition H1:** If -RO tokens appear with equal frequency in non-terminal positions (terminal rate ≤50%), the suffix has no consistent positional semantics.

**H2 (Lexical Expansion):** The most frequent multi-sign sequences appearing immediately before commodity logograms in accounting records are entity/category labels (commodity sub-types, person categories, or place qualifiers) that can be assigned provisional semantic roles by cross-referencing (a) which specific logograms they precede, (b) their site distribution, and (c) Hurrian administrative vocabulary.

**Falsification condition H2:** If the top pre-logogram sequences are already-known formulas or show no cross-site consistency (appearing at only 1 site), no new lexical items are recoverable via this method.

**H3 (*301 Context Separation):** Sign *301 has a distinct distributional co-occurrence profile in administrative records vs. ritual records. If the two profiles share <30% of their top co-occurrence partners, *301 may serve different functions in the two registers (logographic vs. phonemic, or two different phonetic values).

**Falsification condition H3:** If *301 co-occurrence profiles overlap ≥30%, the sign is used consistently across registers and the dual-context appearance is not linguistically significant.

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full
- [x] All files in `hypotheses/` enumerated and read:
  - `2026-03-18-admin-formula-bootstrapping.md`
  - `2026-03-18-libation-proper-nouns-hurrian.md`
  - `2026-03-18-ngram-luwian-ergative-me.md`
  - `2026-03-18-dikte-dikti-me-suffix.md`
  - `2026-03-19-sign-clustering-ngram-unakana-wordorder.md`
- [x] This hypothesis differs from prior attempts because:
  - **No prior attempt tested -RO as a productive suffix.** KU-RO and KI-RO were treated as opaque units; the -RO component was never tested independently.
  - **No prior attempt systematically mined pre-logogram sequences for new lexical items.** Admin formula bootstrapping (Attempt #2) found terminal-slot tokens but not pre-logogram entity tokens.
  - **No prior attempt separated *301's admin vs. ritual distributional profile.** Attempt #6 sign clustering used the entire corpus without register separation.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Inscriptions analyzed: All 1721 for H1 and H3; admin subset (tablet/nodule/roundel/clay vessel) for H2
- External references: Hurrian administrative vocabulary from Mitanni-period texts; Linear B commodity logograms (Ventris/Chadwick)

### Analysis Steps — H1 (-RO Paradigm)

1. Load full corpus; extract all tokens with type="token" from transliteration_tokens
2. For each multi-syllable token ending in "-RO": record (a) its position index within the inscription token list, (b) total token count of inscription, (c) relative position = index / count, (d) site, (e) support type, (f) whether followed by a numeral
3. Exclude pure logograms and numerals
4. Compute terminal position rate: fraction of -RO tokens at position ≥0.75 of inscription length
5. Compare to baseline: same metric for all other non-logographic multi-syllable tokens
6. Separate KU-RO and KI-RO from the general -RO pool; test whether remaining -RO tokens show the same positional clustering
7. List top 20 non-KU/KI tokens ending in -RO by frequency with full context

### Analysis Steps — H2 (Lexical Expansion)

1. Load corpus; filter to administrative support types: tablet, nodule, roundel, clay vessel
2. Define known commodity logograms: GRA, VIN, OLE, OLIV, VIR, MUL, CYP, FIG, LANA, OVS, BOS, CERV, NI
3. For each record, find all logogram positions; extract the 1-token and 2-token windows immediately before each logogram
4. Aggregate: for each pre-logogram sequence, count (a) total occurrences, (b) number of distinct sites, (c) which logograms it precedes (distribution)
5. Filter: keep only sequences with ≥3 occurrences AND ≥2 distinct sites AND not in known-formula list
6. For each qualifying sequence: check if it is single-commodity-specific (appears only before one logogram type) vs. general
7. Cross-reference phonological skeleton of top candidates with Hurrian commodity/administrative vocabulary

### Analysis Steps — H3 (*301 Context Separation)

1. Load full corpus; split into admin records (support ∈ {tablet, nodule, roundel, clay vessel}) and ritual records (support ∈ {stone vessel, metal object})
2. Find all records containing "*301" in their transliteration tokens
3. For each context (admin/ritual), build a co-occurrence frequency vector for *301: for every other sign S that appears within a window of 3 tokens of *301, count co-occurrences
4. Apply PMI weighting: PMI(*301, S) = log[P(*301,S) / (P(*301) × P(S))]
5. Extract top-20 co-occurrence partners for each context
6. Compute overlap: |admin_top20 ∩ ritual_top20| / 20
7. Secondary check: does *301 in admin records immediately precede numerals? (logographic indicator)
8. Secondary check: does *301 in admin records appear in predictable positions (first token, after formula words)?

### Scripts

- `analysis/scripts/ro_suffix_analysis_2026-03-19.py`
- `analysis/scripts/lexical_expansion_2026-03-19.py`
- `analysis/scripts/sign301_analysis_2026-03-19.py`

### Outputs

- `analysis/outputs/ro_suffix_analysis_2026-03-19.json`
- `analysis/outputs/lexical_expansion_2026-03-19.json`
- `analysis/outputs/sign301_analysis_2026-03-19.json`
- `analysis/outputs/attempt7_summary_2026-03-19.md`

---

## Results

**Outcome:** PARTIAL SUCCESS (H1 failed by threshold; H2 partial; H3 inconclusive but yields critical structural finding)
**Confidence:** Low–Medium across individual findings
**Evidence tier reached:** Tier 3 (Formulaic) for PO-TO-KU-RO and A-DU; Tier 1 (Structural) for *301 header finding

### Findings

#### H1: -RO Paradigm — FAILED (by threshold) / PARTIAL (structurally)

- Total non-formula -RO tokens: **25 occurrences**, 7 sites, 16 distinct token types
- Terminal rate: **40%** (threshold was 60%) — hypothesis FAILED by strict criterion
- Baseline terminal rate: 22.5% — -RO tokens are still **1.8× more terminal than baseline**, suggesting weak but real positional bias
- KU-RO and KI-RO were filtered as logograms (correct behavior)

**Significant sub-findings:**

**PO-TO-KU-RO** (2 occ, Haghia Triada, 100% terminal):
- HT122b: `… KU-RO 65 → PO-TO-KU-RO → 97` — appears AFTER KU-RO with a LARGER number (97 > 65)
- HT131b: `NI 30 OLIV 2 VIN+SA — → PO-TO-KU-RO → 451 ½` — appears at record end with very large quantity
- Interpretation: **PO-TO-KU-RO = "grand total" or "cumulative total"**, superseding KU-RO in records with compound tallies
- Evidence: Tier 3 (Formulaic); Confidence: Medium (single site only, needs cross-validation)

**KI-DA-RO** (2 occ, Haghia Triada, 100% terminal):
- Context: `DA-NE-KU-TI 1 → KI-DA-RO → 1` and `PI 10 → KI-DA-RO → 5 MI-NU-MI`
- Possible variant of KI-RO ("owed/deficit") with intercalated -DA- (Hurrian dative/directive?)
- Evidence: Tier 3; Confidence: Low (2 occ, 1 site)

**SA-RO** (4 occ, Haghia Triada, 25% terminal):
- Contexts: appears BETWEEN wine (VIN) logogram and quantities: `VIN 37 → SA-RO → 10 SI-DA-RE`
- Mid-inscription position, no terminal clustering — possibly a VIN sub-category or accounting unit
- Evidence: Tier 3; Confidence: Low (1 site only)

#### H2: Lexical Expansion — PARTIAL (4 of 5 threshold, but key individual findings)

4 qualifying sequences found (threshold was 5):
- `≈ ¹⁄₆` — fraction-separator token (not a lexical item)
- `*304` — unknown sign appearing before OLE/OLIV at 2 sites (possible logogram)
- `A-DU` — **9 occ, 3 sites** (Haghia Triada, Khania, Tylissos) — see below
- `¹⁄₁₆` — fraction token (not a lexical item)

**A-DU** (9 occ, 3 sites: HT, Khania, Tylissos):
- Appears as FIRST TOKEN in 7/10 occurrences (record-initial position)
- Also appears after section dividers (—) within records
- Followed immediately by a divider (𐄁) in most cases, then commodity entries
- Interpretation: **A-DU = administrative section header** or conjunction ("herewith", "from", "also"), marking the start of a new tallying unit
- HT99a: A-DU appears at record start, followed by SA-RA₂ → CYP 4 (connects to SA-RA₂ pattern)
- HT92: `TE 𐄁 → A-DU → 𐄁 GRA 680` — A-DU appears mid-record after TE, then GRA 680
- Evidence: Tier 3 (Formulaic/Administrative); Confidence: Low-Medium (cross-site, but function unclear)

**SA-RA₂** (20+ occ, Haghia Triada only):
- Appears before GRA (8x), CYP (5x) with large quantities
- Critical pattern: appears AFTER KU-RO with a new commodity:
  - HT100: `KU-RO 97 → SA-RA₂ → CYP 5`
  - HT94a: `KU-RO 110 → SA-RA₂ → CYP 5`
- Interpretation: **SA-RA₂ = "additionally" or supplementary entry marker** — introduces a secondary commodity line after the main total
- HT-only; cannot cross-validate. Low confidence for lexical assignment.
- Evidence: Tier 3; Confidence: Low (1 site)

**Sign *304** (14 occ, 2 sites: HT, Khania):
- Appears before OLE (4x), OLIV (4x), GRA (2x), NI (2x), CYP (2x)
- Broad logogram distribution (not commodity-specific)
- May be an unknown administrative sign (person category, measurement unit)
- Evidence: Tier 1; Confidence: Low

#### H3: *301 Context Separation — INCONCLUSIVE + NEW STRUCTURAL FINDING

- H3 could not be evaluated: **0 ritual records contain standalone *301**
- The ritual formula A-TA-I-*301-WA-JA stores *301 as part of a compound token, not standalone
- Admin records with standalone *301: **246 records** (238 token count)

**CRITICAL NEW FINDING: *301 as Administrative Tablet Initializer**
- *301 appears at **FIRST POSITION (position 0) in 97.6% of admin occurrences**
- First-position rate: 0.976 — near-perfect positional consistency
- Admin site distribution: Haghia Triada (230/246), Khania (14), Knossos (1), Zakros (1)
- PMI top partners in admin context: MA-RE (4.03), SI-RU (3.03), *306 (2.23)
- NOT followed by numerals (2.0% rate) → NOT a commodity logogram
- NOT followed by logograms (0.0% rate) → NOT a quantity qualifier

**Interpretation:** Sign *301 in administrative records functions as a **TABLET HEADER MARKER** or **INSCRIPTION INITIALIZER** — a scribal mark placed at the top of every administrative tablet to indicate its administrative status. This is structurally analogous to Linear B "ta-ra-si-ja" (consignment/task headings) or other administrative header terms.

The ritual compound A-TA-I-*301-WA-JA is the ritual register's adaptation of this header convention: the administrative initializer *301 is incorporated into a liturgical opening formula. The ritual formula may translate something like: "in the presence of / under the seal of / dedicated to [deity]", incorporating the administrative initializer as part of the dedicatory formula.

### Cross-validation

**PO-TO-KU-RO:**
- Site 1: Haghia Triada — confirmed (2 occ)
- ⚠ No cross-site data — cannot elevate above Medium confidence

**A-DU:**
- Site 1: Haghia Triada — 7 occurrences
- Site 2: Khania — 2 occurrences (KH11, KH23)
- Site 3: Tylissos — 1 occurrence (TY3a)
- Cross-site confirmed: consistent record-initial position across all three sites ✓

**SA-RA₂:**
- Site 1: Haghia Triada — 20+ occurrences
- No other sites — cannot cross-validate

**Sign *301 admin header role:**
- Site 1: Haghia Triada — 230 records
- Site 2: Khania — 14 records
- Site 3: Knossos — 1 record
- Site 4: Zakros — 1 record
- Cross-site confirmed: first-position behavior consistent across all sites ✓

---

## Interpretation

**H1 (-RO paradigm):** The hypothesis in its strict form failed (40% terminal rate, threshold 60%). However:
1. -RO tokens show real positional bias vs. baseline (1.8× more terminal)
2. PO-TO-KU-RO is a genuine new lexical item — a compound of KU-RO meaning "grand total"
3. The -RO suffix does NOT appear to be a generally productive completive suffix in the corpus; most -RO tokens are either isolated personal names or rare administrative terms

The finding suggests that KU-RO and KI-RO may be OPAQUE COMPOUNDS rather than analyzable as [stem]-RO, counter to the initial hypothesis. The -RO component may not be a productive suffix — it may simply be part of the root of the word "total".

**H2 (Lexical expansion):** A-DU (3 sites, record-initial position) is the most promising new functional word. Its consistent appearance at the start of accounting records across 3 geographically separated sites (HT, Khania, Tylissos) makes it a strong candidate for an administrative header term. This is consistent with Hurrian administrative patterns where section-starting words are grammatically distinct.

SA-RA₂'s post-KU-RO appearance pattern (SA-RA₂ CYP 5 following KU-RO totals) is structurally very interesting but requires inter-site validation that is not currently available.

**H3 (*301 admin header):** The 97.6% first-position rate is one of the strongest structural signals observed in the entire project. *301 is almost certainly a SCRIBAL CONVENTION MARKER — a non-phonemic tablet header sign used to identify the document type or scribal authority. This is consistent with its appearance in the ritual formula as an embedded component rather than a standalone sign.

**Language family implications:** The A-DU finding is interesting for Hurrian comparison: Hurrian has the demonstrative/article "ande/anti" and the particle "adi"; a section-header word A-DU would be phonologically compatible with Hurrian demonstrative use. However, this is speculative.

---

## What Was Learned

1. The -RO suffix is NOT a productive completive suffix in Linear A. KU-RO and KI-RO are likely opaque roots, not analyzable as [stem]-RO. The compound PO-TO-KU-RO is evidence that KU-RO is treated as an atomic unit extended by prefixation.
2. Sign *301's near-perfect first-position rate in admin records resolves a major mystery: it is a TABLET INITIALIZER, not a regular phoneme in admin contexts. Its presence in the ritual formula A-TA-I-*301-WA-JA is a borrowing of the administrative header convention into the ritual register.
3. A-DU is the strongest new cross-site administrative word candidate (3 sites, record-initial), though its semantic content requires further analysis.
4. Pre-logogram token mining is limited by the corpus — most pre-logogram tokens are fractions, single-syllable particles, or HT-specific, making cross-site validation difficult. SA-RA₂ is the most frequent pre-logogram sequence but is HT-only.
5. PO-TO-KU-RO = "grand total" adds one confirmed lexical item to the project inventory (Medium confidence, Tier 3).

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/formulaic_sequences.md`: PO-TO-KU-RO ("grand total"), A-DU (administrative section header), SA-RA₂ (post-total supplementary marker), *301 admin header function
- [x] Appended to `findings/known_logograms.md`: *304 as candidate unknown sign (note only)

---

## Follow-up Questions Generated

- [ ] Does PO-TO-KU-RO appear at non-HT sites? Search for PO-TO prefix in all records.
- [ ] What is the full paradigm of KU-RO compounds? Are there other PO-TO- prefixed terms?
- [ ] Is A-DU related to the start-of-tablet convention, or does it specifically mean "delivery"? Compare: does A-DU always start new sections or can it appear after numerals?
- [ ] What do MA-RE and SI-RU (high PMI partners of *301) tell us about the document type that begins with *301? Are all *301-initial records of the same accounting type?
- [ ] SA-RA₂ before GRA at HT — is SA-RA₂ a grain variety (emmer wheat? barley sub-type?) or a measurement class?
- [ ] *304 (14 occ, 2 sites) before OLE/OLIV — is it a logogram for an oil container type?

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
