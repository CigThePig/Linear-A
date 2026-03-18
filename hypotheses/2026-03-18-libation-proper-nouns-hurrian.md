# Hypothesis: Ritual Register Analysis, Proper Noun Isolation, and Hurrian Morphology Testing

**Date:** 2026-03-18
**Strategy category:** Libation Table Analysis / Proper Noun Isolation / Hurrian Testing
**Language tested (if applicable):** Hurrian (primary), Minoan Proper Nouns (cross-reference)
**Builds on / differs from:** `2026-03-18-admin-formula-bootstrapping.md` — that attempt focused on administrative tablets (nodules, accounting sequences). This attempt pivots to (1) the ritual register (stone vessels, metal objects), (2) formal site-specificity scoring to isolate proper nouns, and (3) systematic Hurrian morpheme inventory testing, which was only preliminary in Attempt #2.

---

## Hypothesis Statement

**H1 (Ritual Register):** `JA-SA-SA-RA-ME` is a cross-site liturgical formula (divine name or ritual invocation) appearing predominantly in stone vessel/ritual object contexts, and tokens appearing in the same structural slot across multiple sites represent structurally equivalent vocabulary — providing a "within-script bilingual" window for lexical identification.

**H2 (Proper Nouns):** Sign sequences with high site-specificity scores (≥0.8, occurring at ≥3 occurrences) are proper noun candidates. A subset of these will be phonologically compatible with Minoan/Aegean place names preserved in Greek tradition (Amnisos, Phaistos, Zakros, etc.).

**H3 (Hurrian Morphology):** If Linear A is related to Hurrian (or belongs to the same language family), then Linear A's suffix distribution should partially mirror Hurrian's case/voice morpheme inventory. The mapping -NA↔Hurrian locative-na, -TE↔dative, -JA↔intransitive marker should be testable against contextual co-occurrence data.

**Falsification conditions:**
- H1 fails if JA-SA-SA-RA-ME appears equally in administrative contexts vs. ritual contexts
- H2 fails if high-specificity tokens show no phonological resemblance to known Aegean toponyms and occur randomly across support types
- H3 fails if suffix co-occurrence patterns are incompatible with Hurrian case functions (e.g., -NA words appear in deficit/accounting contexts rather than locative contexts)

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full
- [x] All files in `hypotheses/` enumerated and read: `2026-03-18-admin-formula-bootstrapping.md`, `TEMPLATE.md`
- [x] This hypothesis differs from prior attempts because: Attempt #2 was entirely administrative-register focused and did not compute site-specificity scores. Hurrian comparison in Attempt #2 was a 5-datapoint note, not a systematic test. Libation table analysis was listed as open follow-up work in Attempt #2 but not executed.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Additional files: `corpus/linear_a_rag_chunks.jsonl` (grouped inscription contexts)
- Existing analysis: `analysis/outputs/suffix_paradigm_results_2026-03-18.json` (reused for Hurrian test)
- Inscriptions analyzed: All 1721 for proper noun isolation; ritual-support subset for H1; full corpus for H3
- External references: Hurrian case morpheme inventory (Speiser 1941, Wegner 2007); Minoan/Aegean toponym list from Greek tradition

### Analysis Steps

1. **Ritual register filtering**: Extract all inscriptions with support type matching stone vessel, metal object, architecture, libation table
2. **JA-SA-SA-RA-ME context mapping**: Find all occurrences across the full corpus; record support type, site, and ±3 token context window
3. **Structural equivalence mapping**: Group tokens appearing in the same structural position (pre-formula, post-formula) across ≥2 sites
4. **I-PI-NA-MA SI-RU-TE context mapping**: Same analysis for the second confirmed ritual bigram
5. **Site-specificity scoring**: For every multi-syllable sequence with ≥3 occurrences, compute specificity = max_site_count / total_count; threshold 0.80
6. **Proper noun cross-reference**: Compare high-specificity tokens against Aegean toponym list using simplified consonant skeleton matching
7. **VIR-adjacent flagging**: Identify site-specific tokens appearing adjacent to VIR logogram (likely personal names)
8. **Hurrian morpheme inventory mapping**: For each Hurrian case/voice suffix, find Linear A suffix candidates; score on phonological similarity (0–2), contextual compatibility (0–2), frequency plausibility (0–1)
9. **-NA locative test**: Check if -NA words co-occur with location-type contexts (preposition-like position, not accounting/KU-RO terminal)
10. **-TE dative test**: Check if -TE words appear in "to/for" argument positions
11. **-JA intransitive test**: Validate against the zero KI-RO co-occurrence finding from Attempt #2

### Scripts

- `analysis/scripts/libation_table_analysis_2026-03-18.py`
- `analysis/scripts/proper_noun_isolation_2026-03-18.py`
- `analysis/scripts/hurrian_morphology_2026-03-18.py`
- `analysis/scripts/summary_report_2026-03-18b.py`

### Outputs

- `analysis/outputs/libation_analysis_2026-03-18.json`
- `analysis/outputs/proper_noun_candidates_2026-03-18.json`
- `analysis/outputs/hurrian_morphology_2026-03-18.json`
- `analysis/outputs/summary_report_2026-03-18b.md`

---

## Results

**Outcome:** PARTIAL SUCCESS
**Confidence:** Medium (H1 ritual register), Low-Medium (H2 proper nouns), Medium (H3 Hurrian morphology)
**Evidence tier reached:** Tier 3 (Formulaic) for ritual analysis; Tier 4 (Lexical) for proper noun candidates; Tier 5 (Grammatical) for Hurrian morphology

### Findings

**H1 — Ritual Register (SUPPORTED):**
- JA-SA-SA-RA-ME confirmed at 5 sites (Iouktas, Palaikastro, Platanos, Psykhro, Troullos) on stone vessels (6/7) and metal objects (1/7) — zero administrative occurrences. Tier 3, Medium confidence.
- 10 tokens identified as 100% ritual-exclusive (≥3 occurrences), including:
  - `A-TA-I-*301-WA-JA` (11 occurrences, 3 sites) — the most frequent ritual formula
  - `SI-RU-TE` (7 occ), `I-PI-NA-MA` (6 occ), `U-NA-KA-NA-SI` (4 occ), `DU-RE-ZA-SE` (3 occ)
- Multi-site post-anchor companion: `U-NA-KA-NA-SI` follows JA-SA-SA-RA-ME at both Iouktas and Palaikastro
- Three bigrams confirmed at ≥2 cult sites: `I-PI-NA-MA SI-RU-TE` (4 sites), `JA-SA-SA-RA-ME U-NA-KA-NA-SI` (2 sites), `U-NA-KA-NA-SI I-PI-NA-MA` (2 sites) — suggestive of a four-unit liturgical sequence
- Ritual-enriched suffixes: -MU (17.56x), -SE (3.75x), -TE (3.04x), -ME (3.01x)

**H2 — Proper Nouns (PARTIAL, mostly LOW confidence):**
- 61 multi-syllable tokens analyzed (≥3 occurrences); 42 above 0.80 specificity threshold
- 4 toponym matches by consonant skeleton:
  - `KU-NI-SU` (KNS) ~ Knossos (Linear B *ko-no-so*) — Low confidence; HT-only
  - `DA-KA` (DK) ~ Dikte — Low confidence; HT-only
  - `MI-NU-TE` (MNT) ~ Amnisos or Minoai — Low confidence
  - `I-RA₂` (R) ~ multiple possibilities — inconclusive
- No VIR-adjacent site-specific tokens identified with high specificity in this run
- Single-site limitation: most high-specificity candidates are HT-only, reducing confidence

**H3 — Hurrian Morphology (MIXED RESULTS):**
- 14 high-confidence alignments (score ≥ 4.0); 42 medium-confidence (3.0–3.9)
- Strong alignments: -TE ↔ directive (score=5), -NA ↔ locative (score=5), -TI ↔ directive (score=5), -NE ↔ plural_nom (score=4.5)
- **-JA intransitive test: CONFIRMED** — zero KI-RO across 17 sites + 59% word-initial position = compatible with absolutive/intransitive marker (Medium-High confidence, Tier 5)
- **-RE participle test: COMPATIBLE** — 19.0% KU-RO rate, highest of all suffixes (Medium confidence)
- **-NA locative test: PARTIALLY FAILED** — 33% terminal-number use is too high for a pure locative; function may be ambiguous or dual
- **-TE directive test: WEAKLY SUPPORTED** — 20 sites (most widespread), 3.04x ritual enrichment consistent with dative/directive (Low-Medium)

### Cross-validation

- JA-SA-SA-RA-ME ritual exclusivity: CONFIRMED across 5 geographically diverse sites (non-HT: Palaikastro, Platanos, Psykhro, Troullos)
- I-PI-NA-MA SI-RU-TE: CONFIRMED at 4 cult sites including 3 non-HT (Kophinas, Troullos, Vrysinas)
- -JA zero KI-RO: CONFIRMED at 17 sites (Attempt #2 + this attempt)
- Toponym candidates: NOT CROSS-VALIDATED — all at Haghia Triada only

---

## Interpretation

**Ritual register finding is the strongest outcome of this session.** The identification of 10 ritual-exclusive tokens, the confirmation of JA-SA-SA-RA-ME at 5 sites, and the discovery of a possible four-unit liturgical sequence (`JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE`) represent meaningful progress toward Tier 3–4. These formulas are consistent with a religious invocation structure (divine name + epithet + verb phrase + dedicatory term), which is structurally common in contemporary Near Eastern ritual texts (Hurrian-Mitanni, Hittite, Ugaritic).

**-JA as absolutive marker is now the best-supported single grammatical claim.** Zero KI-RO co-occurrence across 17 sites, dominant word-initial position, low accounting co-occurrence, and ritual enrichment all point to -JA marking the absolutive or intransitive nominal. This is compatible with Hurrian but also with other agglutinative ergative-absolutive languages.

**Hurrian morphological compatibility is real but not definitive.** The aligned matrix shows plausible mappings for 6 of 14 Linear A suffixes. The -NA locative partial failure is an important negative result — it constrains how we interpret the Hurrian connection. The test results support calling Linear A "compatible with Hurrian morphology" but do not constitute evidence of genetic relatedness.

**Proper noun isolation produced suggestive but low-confidence results.** KU-NI-SU as a possible "Knossos" reference is the most interesting candidate, but its HT-only distribution means it cannot be elevated above Low confidence without further evidence.

Phrasing: All of the above "is consistent with", "suggests", or "provides evidence for" — none constitutes confirmed decipherment.

---

## What Was Learned

1. The ritual register is structurally distinct from the administrative register — 10 tokens are categorically exclusive to it. This means ritual and administrative records should be analyzed as separate registers with different vocabulary.
2. The four-unit liturgical sequence hypothesis is the most promising new thread: a combined analysis of `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` could yield the first multi-word Minoan "phrase" with testable internal structure.
3. -JA as absolutive marker is now robust enough to use as a working assumption in future analyses.
4. Site-specificity scoring alone, without contextual/grammatical slot analysis, produces too many candidates with insufficient discrimination. Future proper noun analysis needs to combine specificity scores with grammatical position data.
5. The -NA locative hypothesis is the first clear partial failure from Attempt #3 — this is important negative evidence that -NA is NOT a simple locative.

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/formulaic_sequences.md`: Ritual-exclusive token inventory (10 tokens), possible four-unit liturgical sequence, ritual-enriched suffixes, updated suffix grammatical role table with Hurrian parallels
- [x] Created `findings/proper_noun_candidates.md`: KU-NI-SU, DA-KA, MI-NU-TE toponym hypotheses with methodology notes
- [x] Created `findings/hurrian_morphology.md`: Full alignment matrix results, 4 individual hypothesis test results, Hurrian morpheme reference table

---

## Follow-up Questions Generated

- [ ] Can the four-unit liturgical sequence `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` be found complete in a single inscription?
- [ ] What is sign `*301`? It appears in `A-TA-I-*301-WA-JA` (11 ritual occ) and as a standalone opening token (232 records). Paleographic identification is a priority.
- [ ] Does KU-NI-SU appear at Knossos-site records, or in grammatical positions suggesting "destination to Knossos"?
- [ ] Run Strategy 9 (N-gram fingerprinting): can bigram transition probabilities distinguish Hurrian from Luwian better than the suffix alignment method?
- [ ] What does -ME mark in JA-SA-SA-RA-ME? If it's a grammatical suffix (e.g., vocative, genitive, divine case), what is the root JA-SA-SA-RA?
- [ ] Is there evidence for an ergative/absolutive split in Linear A? If -JA is absolutive, the ergative marker should also be identifiable.

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
