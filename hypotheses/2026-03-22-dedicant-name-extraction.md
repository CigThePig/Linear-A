# Hypothesis: Dedicant Name Extraction from Ritual Formula Slot-2 (VSO Subject Position)

**Date:** 2026-03-22
**Strategy category:** Proper Noun Isolation / Libation Table Analysis
**Language tested (if applicable):** N/A (proper noun extraction)
**Builds on / differs from:** Directly extends Attempt #11 (VSO reanalysis). Also builds on Attempt #9 (JA-DI-KI-TU = Diktynna divine name candidate) and Attempt #3 (proper noun isolation via -TI suffix). Differs from Attempt #9 in that JA-DI-KI-TU was tested as a DIVINE name (object/addressee); under VSO, slot-2 is the SUBJECT — potentially the human dedicant. This test resolves whether slot-2 is a fixed divine name or a variable personal name.

---

## Hypothesis Statement

**H14 (Dedicant Name in Slot-2):** In stone vessel inscriptions following the VSO model established by Davis (2026), the token immediately following the verbal phrase (A-TA-I-*301-WA-JA) is the SUBJECT — the human dedicant making the offering. If true:
- Multiple distinct tokens should fill slot-2 (each inscription has a different dedicant)
- Slot-2 tokens should show high site-specificity (personal names are local)
- Slot-2 tokens should match personal name signatures: 2–4 syllables, name-suffix (-TI, -TA, -SI)
- Some slot-2 tokens may match Bronze Age Aegean personal names (preserved in Linear B or Greek)

Alternatively, if slot-2 contains fixed elements (divine names/addressees), the VSO model places them as the dedicated-to entity, and the dedicant may be anonymous or implicit.

**Falsification conditions:**
- If slot-2 has only 1–2 distinct tokens across all inscriptions, it is a fixed formula element (divine name/title), not a personal name slot
- If slot-2 tokens are identical to slot-3+ tokens (JA-SA-SA-RA-ME etc.), the VSO slot assignment is incorrect
- If slot-2 tokens have cross-site frequency > 0.5 (appearing broadly), they are likely fixed liturgical elements

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full (Attempts #1–#10 reviewed)
- [x] All files in `hypotheses/` enumerated and read (10 hypothesis files reviewed)
- [x] This hypothesis differs from prior attempts because:

**Key difference from Attempt #9 (divine name matching):** Attempt #9 tested JA-DI-KI-TU against divine name rosters (Hurrian, Minoan-Greek, etc.) and found a plausible match to Diktynna. H14 tests whether JA-DI-KI-TU and other slot-2 tokens are personal names of dedicants rather than divine names. These are functionally different: a divine name would appear across many inscriptions; a dedicant name would appear in only 1–3 inscriptions.

**Key difference from Attempt #3 (proper noun isolation):** Attempt #3 used site-specificity scoring globally across all inscriptions. H14 uses positional constraint (slot-2 only) to narrow the candidate set to a specific structural position, then applies personal name criteria.

**New external basis:** Davis (2026), chapter in Salgarella & Petrakis *The Wor(l)ds of Linear A* — VSO word order established from libation formula analysis; second element = subject (dedicant name or divine addressee).

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Prior output: `analysis/outputs/vso_ritual_reanalysis_2026-03-22.json` (slot-2 token list from Attempt #11)
- Prior output: `analysis/outputs/divine_name_match_2026-03-21.json` (consonant-skeleton LCS scores for reuse)
- External reference: Davis (2026) for VSO slot model; Linear B Knossos personal name lists (Ventris & Chadwick 1953)

### Analysis Steps

1. Load slot-2 token list from `vso_ritual_reanalysis_2026-03-22.json` (from Attempt #11)
2. For each distinct slot-2 token:
   a. Count occurrences (total corpus, not just slot-2)
   b. Compute site-specificity: max_site_count / total_count
   c. Extract final syllable (suffix analysis)
   d. Count number of syllables in token
   e. Check if token appears anywhere else in corpus outside ritual stone vessel context
3. Classify slot-2 tokens:
   - **Variable/personal name profile:** ≤ 3 total occurrences, site-specificity > 0.7, 2–4 syllables
   - **Fixed/divine name profile:** ≥ 4 occurrences, site-specificity < 0.5, appears across multiple inscriptions
4. For the top 5 candidates by personal-name profile score:
   Run LCS consonant-skeleton matching (reusing algorithm from `divine_name_match_2026-03-21.py`) against:
   - Known Linear B Knossos non-Greek (Minoan) personal names: e.g., consonant skeletons from Ventris & Chadwick's "pre-Greek" name list
   - Known Bronze Age Aegean theophoric names: Minos [M,N], Ariadne [R,D,N], Rhadamanthos [R,D,M,T]
   - Known Hurrian personal name patterns (e-vuri/Ewri, Tešup-compounds)
5. Specifically re-test JA-DI-KI-TU: count its total occurrences and site distribution to determine fixed vs. variable profile
6. Compute complementarity between slot-2 tokens: does any inscription contain two different slot-2 candidates? (Should not, if each is a unique dedicant)

### Scripts

- `analysis/scripts/dedicant_name_extraction_2026-03-22.py`

### Outputs

- `analysis/outputs/dedicant_name_extraction_2026-03-22.json`

---

## Results

**Outcome:** PARTIAL SUCCESS — two genuine personal name candidates found; VSO slot-2 structure clarified
**Confidence:** High (structural finding), Low (specific name identifications)
**Evidence tier reached:** Tier 3 (formulaic slot structure), Tier 4 (personal name candidates)

### Findings

**Slot-2 token distribution (11 inscriptions with A-TA-I-*301-WA-JA):**

| Token | Slot-2 Count | Total Corpus Occ | Site Specificity | Profile |
|-------|-------------|-----------------|-----------------|---------|
| `𐄁` | 9 | 233 | 0.444 | AMBIGUOUS (section divider) |
| **TU-RU-SA** | **1** | **1** | **1.0** | **PERSONAL NAME (high confidence)** |
| **SE-KA-NA-SI** | **1** | **1** | **1.0** | **PERSONAL NAME (high confidence)** |

**JA-DI-KI-TU in slot-2:** NOT OBSERVED — JA-DI-KI-TU appears in slot-3+ position across inscriptions, consistent with it being a divine object/addressee (Diktynna), not the subject.

**Overall slot-2 classification:** AMBIGUOUS — the dominant slot-2 element (`𐄁`) is the scribal section divider identified in Attempt #10, not a lexical item. In 2 of 11 inscriptions where this divider is absent at slot-2, genuine personal-name-profile tokens appear.

**TU-RU-SA (personal name candidate, Low confidence):**
- Consonant skeleton: [T, R, S]
- Best LCS match: Teshup-compound (Hurrian) — score=0.667, LCS=2
  - Teshup is the Hurrian storm god; compound names like "X-Teshup" are attested
  - [T,R,S] vs. [T,S,P]: overlap at T and S — weak but suggestive
- Second match: Tupkish (Hurrian name) — score=0.500, LCS=2
- Unique in corpus (1 occurrence); consistent with individual dedicant's name

**SE-KA-NA-SI (personal name candidate, Low confidence):**
- Consonant skeleton: [S, K, N, S]
- Best LCS match: Knossos toponym skeleton [K, N, S] — score=0.75, LCS=3
  - This match may be coincidental — Knossos is a place name, not a personal name
- Hurrian Shaushka [S, S, K] — score=0.500, LCS=2
  - Shaushka is the Hurrian goddess of love/war; consistent with a ritual context
- Unique in corpus (1 occurrence); personal name profile

### Cross-validation

- Only 11 inscriptions contain the ritual header; TU-RU-SA and SE-KA-NA-SI each appear once
- Single-occurrence personal names cannot be cross-validated across sites by definition
- The section-divider finding (`𐄁` in 9/11 slot-2 positions) is confirmed against all 11 inscriptions

---

## Interpretation

The slot-2 picture is substantially clarified: the scribal section divider `𐄁` occupies slot-2 in 9/11 inscriptions as punctuation separating the verbal phrase from content. In 2 exceptional inscriptions, the divider is absent and unique personal-name-profile tokens (TU-RU-SA, SE-KA-NA-SI) fill slot-2 directly.

This is **consistent with** the VSO dedicant-name hypothesis for a subset of inscriptions, while the majority of inscriptions suppress the dedicant name (using only the section marker before the divine/ritual content).

JA-DI-KI-TU's absence from slot-2 is informative: it suggests Diktynna is an object/addressee (slot-3+), not the subject. This is compatible with a reading where the ritual verb ("I offer") → section divider → Diktynna (divine name as object) → ritual attributes.

The Hurrian phonological matches for TU-RU-SA (Teshup-compound profile) are suggestive but Low confidence; a single LCS match does not constitute identification.

Phrasing: All interpretations are "consistent with" the data — no decipherment claimed.

---

## What Was Learned

1. `𐄁` dominates slot-2 (9/11 inscriptions) as a structural separator, not a lexical dedicant element
2. TU-RU-SA and SE-KA-NA-SI are the first genuine personal name candidates from the ritual formula — unique, site-specific, corpus-hapax tokens
3. JA-DI-KI-TU is NOT in slot-2; it occupies slot-3+ (divine addressee / object position), consistent with Diktynna as the deity being addressed
4. The slot-2 evidence is insufficient for strong personal-name claims (2 tokens is too small) but the structural finding about `𐄁` as punctuation is confirmed
5. Personal names in Minoan ritual inscriptions appear to be rare or omitted — possibly the dedicant's name was implicit (known at the cult site)

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/formulaic_sequences.md`: Slot-2 characterization; TU-RU-SA and SE-KA-NA-SI as Low-confidence personal name candidates; JA-DI-KI-TU confirmed as slot-3+ element (divine addressee)

---

## Follow-up Questions Generated

- [ ] Which sites do the TU-RU-SA and SE-KA-NA-SI inscriptions come from? Are they cult-center sites?
- [ ] Is SE-KA-NA-SI related to SE-KA-NA (a sub-sequence)? Does SE-KA appear elsewhere?
- [ ] Can the 2 non-divider inscriptions be dated or attributed to specific contexts that explain the name presence?

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
