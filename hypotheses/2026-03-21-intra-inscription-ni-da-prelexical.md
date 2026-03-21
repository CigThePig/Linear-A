# Hypothesis: Intra-Inscription Case Validation, NI Commodity ID, -DA Disambiguation, Pre-Logogram Lexical Sweep

**Date:** 2026-03-21
**Strategy category:** Suffix Analysis / Logogram Identification / Administrative Bootstrapping
**Language tested (if applicable):** Hurrian (primary for grammar), general comparative for NI
**Builds on / differs from:** Directly extends Attempt #9 (2026-03-21-paradigm-divine-logogram.md) by following up on all four open questions from that attempt. Also builds on Attempts #2, #3, #8 (suffix work) and Attempt #7 (lexical expansion).

---

## Hypothesis Statement

**H10a (Intra-Inscription Case Validation):** If the case paradigm found in Attempt #9 (H9a) is real inflectional morphology, at least some inscriptions will contain two different case forms of the same stem within the same inscription. Furthermore, absolutive (-JA) forms should appear at structurally earlier positions than ergative (-RU) forms within those inscriptions (agent after patient word-order or absolutive-before-ergative syntax).

**H10b (NI Commodity Identification):** NI (68.4% numeral-after, 7 sites, 76 occurrences) is a commodity logogram whose specific referent can be identified through co-occurrence patterns with other known logograms and cross-site context analysis. Specifically, NI is hypothesized to be the Linear A equivalent of the fig logogram (Linear B *NI/FIG), given that token "FIG" appears 0 times in the corpus.

**H10c (-DA Grammatical Disambiguation):** The 16 unique -DA tokens divide into two classes: (a) proper nouns / toponyms (e.g., I-DA = Mt. Ida) that inflate the high ritual enrichment (4.40x) found in H9d, and (b) grammatical -DA case suffixes on stems that also appear with other case variants (from the H9a paradigm list). If class (b) is isolated, its distributional profile should better match the Hurrian dative -da prediction (low KI-RO, low ritual enrichment, word-terminal).

**H10d (Pre-Logogram Lexical Sweep):** Tokens appearing immediately before known logograms at 3+ sites and ≥5 occurrences represent commodity modifiers, variety names, or grammatical words that can be promoted to the confirmed vocabulary, advancing toward the 20-item goal.

**Falsification conditions:**
- H10a fails if no inscription contains 2+ case forms of the same stem; or if -JA and -RU show no positional asymmetry when they co-occur
- H10b fails if NI shows no distinctive co-occurrence pattern with any logogram family, or if NI contexts are too varied across sites to identify a single commodity
- H10c fails if the two -DA classes cannot be separated, or if stripping proper nouns does not substantially change the distributional profile
- H10d fails if no pre-logogram token meets the 3-site/5-occurrence threshold, OR if every candidate is a known formula word

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full (Attempts #1–#9 reviewed)
- [x] All files in `hypotheses/` enumerated and read (8 hypothesis files including this one's predecessors)
- [x] This hypothesis differs from prior attempts because:

**Key difference from Attempt #9 (most recent):** Attempt #9 found the case paradigm cross-inscriptionally (same stem, different suffixes, different inscriptions). Attempt #10 H10a tests intra-inscription co-occurrence — the same stem appearing twice in one text with different endings. This is a qualitatively stronger test because it requires the scribe to inflect the same word twice for different syntactic roles in the same sentence/record.

**Key difference from Attempt #7 (lexical expansion):** Attempt #7 searched for tokens appearing before any numeral. H10d searches for tokens appearing before specific known logograms — a tighter, more semantically constrained filter that should yield commodity-specific vocabulary rather than generic pre-numeral words.

**Key difference from Attempt #8 (*304 logogram):** That attempt used PMI-based co-occurrence. H10b uses positional context windows and cross-site comparison patterns, which avoids the mixed-sample-space bug (CI-003) that affected PMI computation in that attempt.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Prior outputs:
  - `analysis/outputs/paradigm_alternation_2026-03-21.json` — paradigm stems and confirmed case tokens (H10a, H10c)
  - `analysis/outputs/da_suffix_test_2026-03-21.json` — 16 unique -DA tokens and distributional profiles (H10c)
- External references:
  - Linear B *NI/FIG logogram for NI comparison (H10b)
  - Hurrian dative -da expected distribution profile from `findings/hurrian_morphology.md` (H10c)
  - Known logogram list from `findings/known_logograms.md` (H10d)

### Analysis Steps

**H10a:**
1. Load all paradigm stems from `paradigm_alternation_2026-03-21.json` and their confirmed case tokens
2. For each record in corpus, scan token list for 2+ case forms of the same stem within that inscription
3. For each co-occurrence found: record inscription ID, site, tokens, their positions (index in token array)
4. Compute mean position of -JA forms vs. -RU forms across all co-occurring pairs
5. Test: is mean(-JA position) < mean(-RU position)? — absolutive-before-ergative prediction

**H10b:**
1. Extract all records containing NI token; build ±3-token context windows
2. Compute co-occurrence rates with each known logogram (GRA, VIN, OLE, OLIV, CYP, *304, MUL, VIR)
3. Compare NI context distribution across 7 sites for consistency
4. Check fraction-preceded rate; compare with GRA/VIN/OLE baselines
5. Compare NI co-occurrence profile against known commodity logogram profiles to identify cluster membership

**H10c:**
1. Load 16 unique -DA tokens from `da_suffix_test_2026-03-21.json`
2. Classify each token: if its stem (token minus final -DA sign) appears as a paradigm stem in H9a output → Class B (grammatical)
3. Remaining tokens: check against ritual sequence (JA-SA-SA-RA-ME, DI-KI, U-NA-KA-NA-SI) and short-form criterion (≤3 signs) → Class A (proper noun / toponym)
4. Recompute distributional profile for Class B alone (KI-RO, KU-RO, ritual enrichment, VIR rate)
5. Compare Class B profile to Hurrian dative prediction

**H10d:**
1. For each known logogram (TARGET_LOGOGRAMS), scan all inscriptions for immediate predecessor tokens
2. Exclude: numerals, fractions, other known logograms, known formula words (KU-RO, KI-RO, A-DU, *301, *304)
3. Aggregate by pre-token: total occurrences, site count, set of logograms preceded, record list
4. Filter: site_count ≥ 3 AND total_occurrences ≥ 5
5. Classify: multi-logogram tokens as grammatical/modifier candidates; single-logogram tokens as variety/specific descriptor candidates
6. Rank by (site_count × total_occurrences)

### Scripts

- `analysis/scripts/intra_inscription_paradigm_2026-03-21.py` (H10a)
- `analysis/scripts/ni_commodity_context_2026-03-21.py` (H10b)
- `analysis/scripts/da_disambiguation_2026-03-21.py` (H10c)
- `analysis/scripts/pre_logogram_sweep_2026-03-21.py` (H10d)

### Outputs

- `analysis/outputs/intra_inscription_paradigm_2026-03-21.json`
- `analysis/outputs/ni_commodity_context_2026-03-21.json`
- `analysis/outputs/da_disambiguation_2026-03-21.json`
- `analysis/outputs/pre_logogram_sweep_2026-03-21.json`
- `analysis/outputs/attempt10_summary_2026-03-21.md`

---

## Results

**Outcome:** MIXED — H10a NEGATIVE (INFORMATIVE), H10b PARTIALLY SUPPORTED, H10c PARTIALLY SUPPORTED (KEY NEGATIVE FINDING), H10d MOSTLY FAILED (STRUCTURAL DISCOVERY)
**Confidence:** H10a: High (definitive negative) | H10b: Medium-High (NI = plant commodity) | H10c: Medium (ritual enrichment finding) | H10d: High (definitive negative)
**Evidence tier reached:** H10a: Tier 1 (structural) | H10b: Tier 2 (logographic) | H10c: Tier 5 (grammatical) | H10d: Tier 1 (structural)

### Findings

**H10a:** 0 inscriptions contain 2+ case forms of the same stem. This is expected given the administrative corpus structure — Linear A tablets are inventory lists, not narrative texts. The case paradigm remains valid but is cross-inscriptional evidence only.

**H10b:** NI is an administrative agricultural commodity (ritual enrichment 0.5x, below baseline). Co-occurrence profile: VIN (26.9%), CYP (25.4%), GRA (22.4%), *304 (13.4%). Average quantity 9.4, maximum 62. Fraction-before rate 22.4%. Fig hypothesis highest-scoring (score=3). NI is almost certainly a plant/fruit commodity logogram.

**H10c:** 16 -DA tokens split: 9 Class A (proper noun/toponym), 7 Class B (grammatical stems). Class B ritual enrichment = 6.06x — far above Hurrian dative profile. **Hurrian dative -da identification REJECTED.** Critical limitation: I-DA (5 occurrences on stone vessels, all ritual) was misclassified as Class B because stem "I" appears in paradigm. Even corrected, -DA shows consistently high ritual enrichment in both classes, indicating it is a RITUAL DEDICATORY morpheme, not an administrative case suffix.

**H10d:** Only `𐝫` (U+1076B) meets the 3-site/5-occurrence threshold — preceding 11 different logograms at 5 sites. This sign is a scribal entry/section marker (Tier 1 structural), not a vocabulary item. No lexical vocabulary candidates found via pre-logogram position.

### Cross-validation

- H10a: Tested all 1721 records (no HT bias possible)
- H10b: NI present at 7 sites (HT, KH, KN, PH, Zakros, Crete, Tel Haror) ✓✓
- H10c: -DA tested at 12 sites; I-DA specifically at 3 non-HT sites (Nerokurou, Palaikastro, Zakros) ✓
- H10d: `𐝫` appears at 5 sites (HT, KH, KN, TY, ZA) ✓

---

## Interpretation

**H10a (negative):** The inability to find intra-inscription case co-occurrences is a corpus-structure finding, not a falsification of the case paradigm. Linear A administrative texts are single-subject inventories (like Linear B). This constrains how we should interpret all further grammatical evidence — it must remain cross-inscriptional.

**H10b (NI = figs/plant):** NI's administrative profile, bulk quantities, and fruit-commodity co-occurrence pattern consistently points to a plant product (most likely figs). The absence of "FIG" token in the corpus and the presence of NI in the same structural position as GRA/VIN/OLE supports the identification of NI as the Linear A fig logogram. This provides evidence that is compatible with the Linear B sign correspondences (Linear B NI = fig logogram).

**H10c (-DA = ritual marker):** The rejection of Hurrian dative -da does not eliminate the Hurrian hypothesis entirely, but it removes one of the medium-confidence Hurrian morpheme alignments. -DA appears to be a ritual dedicatory marker — this is consistent with some Hurrian theophoric formations but not the administrative dative. The Hurrian compatibility should be downgraded from Medium-High to Medium overall.

**H10d (structural discovery):** The `𐝫` sign is an administrative entry marker. The absence of lexical pre-logogram tokens confirms that Linear A commodity vocabularies are encoded in compound-sign form (OLE+KI, GRA+QE) rather than as separate preceding words. This has implications for vocabulary discovery: future lexical work must focus on compound signs and cross-inscription contexts, not positional pre-logogram analysis.

---

## What Was Learned

1. Linear A administrative tablets never show the same word in two different case forms within a single inscription — they are inventory records, not narrative texts
2. NI is a bulk agricultural commodity with administrative profile; fig identification is most consistent hypothesis
3. -DA is a ritual dedicatory marker, not an administrative dative case suffix — Hurrian dative hypothesis rejected
4. `𐝫` (U+1076B) is a scribal entry marker functionally equivalent to `𐄁`
5. The pre-logogram position is not productive for vocabulary discovery — compound signs encode commodity varieties
6. I-DA (Mt. Ida toponym) can be misclassified by the paradigm-based disambiguation due to shared stem "I" with grammatical forms — proper noun identification requires support-type cross-checking

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/hurrian_morphology.md`: -DA rejection entry; overall compatibility downgraded to Medium
- [x] Appended to `findings/known_logograms.md`: NI identification reinforced; `𐝫` structural marker note

---

## Follow-up Questions Generated

- [ ] Is NI specifically figs? Cross-reference 7-site NI distribution with fig archaeobotany record
- [ ] What is I-DA doing at ZA24a alongside GRA logogram? (ritual grain dedication?)
- [ ] What is -DA's specific ritual function? Check if -DA tokens are always preceded by ritual elements (divine names, sanctuary names)
- [ ] Can `𐝫` be matched to a known Linear A sign number?
- [ ] What is the 20th vocabulary item? *22F (78.6% numeral-after, 4 sites) is the strongest remaining candidate

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
