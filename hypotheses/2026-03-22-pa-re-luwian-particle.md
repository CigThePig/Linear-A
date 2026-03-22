# Hypothesis: PA-RE as Luwian Loanword Particle (*pari* = "forth/away")

**Date:** 2026-03-22
**Strategy category:** Luwian Comparison / Administrative Bootstrapping
**Language tested (if applicable):** Luwian (Anatolian Indo-European)
**Builds on / differs from:** Extends Attempts #4, #6 (Luwian morpheme comparison — yielded 0 high-confidence Luwian grammar alignments vs. 14 for Hurrian). Differs because Nepal & Perono Cacciafoco (2024) identified a vocabulary-level Luwian match (PA-RE ↔ Luwian *pari*) using consonantal cryptanalysis. Previous Luwian tests focused on morphology and grammar; this tests a specific lexical/particle claim.

---

## Hypothesis Statement

**H12 (PA-RE = Luwian particle):** PA-RE is a Luwian loanword particle (*pari* = "forth/away") that entered the Minoan administrative or ritual lexicon through Anatolian trade contact. If true, PA-RE should show:
- Consistent phrasal-initial position (particles / prepositions appear before the phrase they govern)
- Cross-site distribution (syntactic particles should appear everywhere, not be site-confined)
- Non-logogram profile (no numeral-after enrichment)
- Context compatible with directional/movement meaning (appears near commodity transfer records)

**Falsification conditions:**
- If PA-RE appears only at Haghia Triada (site-confined like KI-RO), it cannot be a universal syntactic particle
- If PA-RE shows numeral-after rate > 60%, it is a logogram candidate, not a particle
- If PA-RE appears fewer than 3 times in the corpus, the claim cannot be evaluated

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full (Attempts #1–#10 reviewed)
- [x] All files in `hypotheses/` enumerated and read (10 hypothesis files reviewed)
- [x] This hypothesis differs from prior attempts because:

**Key difference from Attempt #4 (Luwian comparison, 2026-03-18):** Attempt #4 ran a systematic morpheme-level sweep of the top 50 Linear A sequences against Melchert's Luvian glossary. It found 0 high-confidence Luwian morpheme matches. That test compared grammatical morphemes; H12 targets a specific particle/preposition that may be a loanword.

**Key difference from Attempt #6 (n-gram + Luwian):** Attempt #6 used phonotactic fingerprinting; Luwian ranked #2 (after Hurrian). That is structural compatibility; H12 is a targeted single-token test.

**New external basis:** Nepal & Perono Cacciafoco (2024) "Minoan Cryptanalysis" (MDPI *Information* 15:2:73) identified PA-RE as a vocabulary-level Luwian match using consonant comparison. This is the only published, peer-reviewed, specific vocabulary correspondence claim from 2024 and merits direct corpus validation.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Prior output: `analysis/outputs/luwian_comparison_2026-03-18.json` (for cross-reference of prior PA-RE ranking)
- External reference: Nepal & Perono Cacciafoco (2024), MDPI *Information* 15:2:73 — PA-RE ↔ Luwian *pari* = "forth/away"

### Analysis Steps

1. Search entire corpus for PA-RE as standalone token AND as sub-sequence within longer tokens (e.g., PA-RE-SI, I-PA-RE)
2. For standalone PA-RE: compute occurrence count, site count, record list, support-type breakdown
3. Compute position profile: inscription-initial rate, inscription-terminal rate, pre-logogram rate, post-numeral rate
4. Compute numeral-after rate (logogram test threshold: > 60% = logogram candidate)
5. Compute site-specificity: if one site accounts for > 80% of occurrences, token is site-confined
6. Compute context profile: ±2-token window — which known logograms, numerals, formula words appear near PA-RE?
7. Compare PA-RE positional profile against KU-RO (terminal), KI-RO (terminal, HT-only), and A-DU (initial, section marker)
8. If PA-RE appears ≥ 3 times at ≥ 2 sites: evaluate particle profile: initial enrichment + non-numeral context + multi-site
9. Check PA-RE entry in `luwian_comparison_2026-03-18.json` output for any prior match score
10. Test consonant skeleton [p,r]: are there other Linear A tokens with the same skeleton that might be variants?

### Scripts

- `analysis/scripts/pa_re_particle_test_2026-03-22.py`

### Outputs

- `analysis/outputs/pa_re_particle_test_2026-03-22.json`

---

## Results

**Outcome:** NEGATIVE — INSUFFICIENT DATA
**Confidence:** N/A (insufficient data to evaluate)
**Evidence tier reached:** Tier 1 (structural — occurrence count only)

### Findings

- Standalone PA-RE: **1 occurrence** in the entire 1,721-record corpus (Haghia Triada only)
- Token occurrences: 1 (single record, single site)
- Site-confined: TRUE (100% at Haghia Triada)
- Numeral-after rate: 0.0% (insufficient to interpret)
- Record-initial rate: 0.0%

**Threshold for evaluation:** 3+ records required. PA-RE falls far short of this threshold.

**Compound tokens containing PA-RE:** checked; no compound tokens with PA-RE as sub-sequence found in corpus.

**Consonant skeleton [P,R] tokens in corpus:** Found a small set of tokens with the same skeleton. The -RE suffix itself (the most common word-final syllable after -RO, n=58) carries the same skeleton — this is worth noting but does not rescue the particle hypothesis.

### Cross-validation

No cross-validation possible with 1 occurrence.

---

## Interpretation

The Nepal & Perono Cacciafoco (2024) claim for PA-RE ↔ Luwian *pari* **cannot be evaluated** against this corpus. With only 1 occurrence at a single site, no positional or distributional analysis is possible.

This does not falsify their claim — they may have used a different transliteration, a different corpus, or a different sign-value assignment yielding "PA-RE" where our corpus shows a different tokenization. Their method involved alternative phonetic value hypotheses for some signs.

The -RE suffix (58 occurrences in word-final position) carries the same [P,R] consonant skeleton as *pari*. If Luwian *pari-* were a productive element in Minoan, -RE as a suffix might be its reduced/bound form. This is speculative (Low confidence) but generates a testable follow-up: does -RE show directional or ablative context enrichment consistent with "forth/away" meaning?

Phrasing: "consistent with" is too strong here. The result is simply null — no data.

---

## What Was Learned

1. PA-RE as a standalone token appears only once in our 1,721-record corpus — the Nepal & Perono Cacciafoco claim is untestable here
2. Their PA-RE identification may stem from alternative sign-value assignments not used in our conventional transliteration system
3. The -RE suffix (58 word-final occurrences) shares the [P,R] consonant skeleton with Luwian *pari* — this warrants a follow-up test of -RE as a directional suffix
4. The Luwian vocabulary-level claim from 2024 remains unresolved in this corpus; it is neither confirmed nor refuted

---

## Findings Promoted to `findings/`

None at this stage.

---

## Follow-up Questions Generated

- [ ] Does -RE suffix (n=58) show directional enrichment (appearing with movement-related commodity flows)?
- [ ] What sign-value assignments did Nepal & Perono Cacciafoco use that yield "PA-RE"? Could their PA-RE correspond to a different token in our corpus?
- [ ] Are there other Luwian particles (*natta*, *wa/ha*, *=pa*) that map to high-frequency Linear A tokens?

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
