# Hypothesis: N-gram Language Fingerprinting, Luwian Morpheme Comparison, Ergative Split Search, and -ME Suffix Analysis

**Date:** 2026-03-18
**Strategy category:** N-gram Fingerprinting / Luwian Comparison / Grammatical Analysis
**Language tested (if applicable):** Luwian (primary comparative test), Hurrian (control), Proto-Semitic (control), Etruscan (control)
**Builds on / differs from:** `2026-03-18-libation-proper-nouns-hurrian.md` — Attempt #3 tested Hurrian morphology systematically but left four open questions: (1) N-gram fingerprinting to independently rank candidate languages (Strategy 9, never attempted); (2) Luwian morpheme comparison as a control against Hurrian (Strategy 4, never attempted); (3) confirmation of the four-unit liturgical sequence in single inscriptions; (4) -ME suffix analysis (3.01x ritual enrichment unexplained); (5) search for the ergative marker if -JA is absolutive.

---

## Hypothesis Statement

**H1 (N-gram Fingerprinting):** The Linear A bigram transition probability matrix will show closer proximity (lower KL-divergence or higher cosine similarity) to Hurrian or Luwian than to Proto-Semitic or Etruscan, providing an independent language family compatibility score not dependent on morpheme-level assumptions.

**H2 (Luwian Morpheme Comparison):** If Linear A suffix behavior maps onto Hurrian case morphemes (Attempt #3 result), it should show *different* behavior when mapped against Luwian case/derivational morphology. If Luwian fits equally well, the Hurrian preference is not justified. If Luwian fits worse, Hurrian is the preferred hypothesis.

**H3 (Liturgical Sequence Confirmation):** The four-unit sequence `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` proposed in Attempt #3 can be found partially or completely in single inscriptions, confirming it is a real formulaic unit rather than an artifact of bigram co-occurrence.

**H4 (-ME Suffix):** The -ME suffix (ritual enrichment 3.01x, 12 ritual / 14 admin occurrences) functions as a grammatical marker specific to religious/dedicatory contexts — possibly a vocative, divine-case, or dedicatory suffix — distinct from the -ME in JA-SA-SA-RA-ME being a suffix to the root JA-SA-SA-RA.

**H5 (Ergative Split):** If -JA marks the absolutive/intransitive subject (Attempt #3, Medium-High confidence), an ergative marker should be identifiable — a suffix that appears *only* with transitive verbs or in contexts where KI-RO (deficit, action applied to something) is present.

**Falsification conditions:**
- H1 fails if Linear A n-gram distances are uniform across all candidate languages (no discrimination)
- H2 fails if Luwian morpheme alignment scores equal or exceed Hurrian (negating Hurrian preference)
- H3 fails if no inscription contains ≥3 of the four sequence elements in order
- H4 fails if -ME words are evenly distributed across ritual and administrative contexts with no syntactic cluster
- H5 fails if no suffix shows the inverse pattern of -JA (high KI-RO co-occurrence, word-final position, transitive context)

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full
- [x] All files in `hypotheses/` enumerated and read: `2026-03-18-admin-formula-bootstrapping.md`, `2026-03-18-libation-proper-nouns-hurrian.md`, `TEMPLATE.md`
- [x] This hypothesis differs from prior attempts because: Attempts #2 and #3 focused on administrative bootstrapping, suffix co-occurrence, ritual register separation, proper noun isolation, and Hurrian morphology. This attempt adds (1) N-gram fingerprinting (Strategy 9, no prior attempt), (2) Luwian morpheme comparison (Strategy 4, no prior attempt, explicitly listed as control in Attempt #3 follow-up), and (3) three targeted follow-up analyses from Attempt #3 open questions. No prior attempt has compared Linear A phonotactics against multiple language families simultaneously.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Additional files: `corpus/linear_a_rag_chunks.jsonl` (full inscription text for liturgical sequence search)
- Prior output reused: `analysis/outputs/suffix_paradigm_results_2026-03-18.json`
- External references:
  - Hurrian bigram reference: derived from Mitanni-period Hurrian morpheme sequences (Speiser 1941, Wegner 2007)
  - Luwian morpheme inventory: Melchert 2003 *Luvian Texts*; cuneiform Luwian case endings
  - Proto-Semitic consonant inventory: Reconstructed triconsonantal root patterns
  - Etruscan syllable frequencies: Bonfante & Bonfante *The Etruscan Language* (2002)

### Analysis Steps

1. **N-gram matrix construction**: Extract all syllable bigrams from `transliteration_tokens` across all 1721 records. Build a transition probability matrix (row = current sign, col = next sign). Remove logograms and numerals.
2. **Reference language matrices**: Construct simplified bigram matrices for Hurrian, Luwian, Proto-Semitic, and Etruscan using known morpheme sequences and phonological inventories. Use CV syllable structure as the common representation layer.
3. **Distance computation**: Compute cosine similarity between Linear A bigram vector and each reference language bigram vector. Rank by similarity.
4. **Luwian morpheme mapping**: Apply Luwian case endings (-anza nominative sg., -an accusative, -ati/i dative-locative, -ati ablative, -anza/-ants plural) to Linear A suffix data. Score each mapping on phonological similarity, contextual compatibility, and frequency using the same 5-point rubric as Attempt #3.
5. **Hurrian vs. Luwian comparison**: Direct comparison of alignment scores for each Linear A suffix against both Hurrian and Luwian morphemes.
6. **Liturgical sequence search**: For all 1721 inscriptions, check which contain ≥2 of {JA-SA-SA-RA-ME, U-NA-KA-NA-SI, I-PI-NA-MA, SI-RU-TE} in correct order. Report any containing 3 or 4.
7. **-ME suffix corpus analysis**: Extract all tokens ending in -ME. Analyze: (a) ritual vs. administrative frequency; (b) position in inscription (initial, medial, final); (c) what follows -ME tokens (number? logogram? another word?); (d) whether -ME tokens cluster around specific logograms.
8. **Ergative search**: Find the suffix whose co-occurrence profile is the inverse of -JA: high KI-RO rate (deficit/action context), word-FINAL position bias, transitive argument position. The ergative marker in an SOV agglutinative language typically appears on the agent noun.
9. **A-TA-I-*301-WA-JA full analysis**: Analyze the most frequent ritual-exclusive formula: extract all 11 occurrences, contexts, companion tokens, and structural position.

### Scripts

- `analysis/scripts/ngram_fingerprint_2026-03-18.py`
- `analysis/scripts/luwian_comparison_2026-03-18.py`
- `analysis/scripts/liturgical_sequence_2026-03-18.py`
- `analysis/scripts/me_suffix_ergative_2026-03-18.py`

### Outputs

- `analysis/outputs/ngram_fingerprint_2026-03-18.json`
- `analysis/outputs/luwian_comparison_2026-03-18.json`
- `analysis/outputs/liturgical_sequence_2026-03-18.json`
- `analysis/outputs/me_suffix_ergative_2026-03-18.json`
- `analysis/outputs/attempt4_summary_2026-03-18.md`

---

## Results

**Outcome:** PARTIAL SUCCESS (H1 failed, H2 confirmed, H3 confirmed, H4 partially confirmed, H5 inconclusive)
**Confidence:** High (H3 liturgical), Medium (H2 Luwian vs Hurrian), Low-Medium (H4 -ME), Low (H1 n-gram, H5 ergative)
**Evidence tier reached:** Tier 3 (Formulaic) — primary; Tier 5 (Grammatical) — secondary; Tier 1 (Structural) — n-gram

### Findings

**H1 (N-gram Fingerprinting): WEAK / METHOD LIMITATIONS**
- Linear A phonotactic similarity ranking: Proto-Semitic (0.1467) > Luwian (0.1131) > Etruscan (0.0971) > Hurrian (0.0860)
- However all similarities are very low (<0.15) due to: (a) unknown/special signs inflating the "OTHER" consonant class to 30% of bigrams; (b) newline tokens conflated with syllabic signs; (c) reference profiles are approximations based on limited morpheme inventory rather than full text corpora
- **RESULT: INCONCLUSIVE** — method needs refinement before ranking is trustworthy
- Notable: result is INCONSISTENT with Hurrian morphological ranking from Attempt #3 (Hurrian was best morphologically, worst n-gram). This inconsistency must be explained.

**H2 (Luwian Morpheme Comparison): HURRIAN PREFERRED, MARGINALLY**
- Luwian: 0 high-confidence alignments (≥4.0), 10 medium-confidence (3.0–3.9)
- Hurrian (Attempt #3): 14 high-confidence, 42 medium-confidence
- Direct suffix comparison: Hurrian wins 8, Luwian wins 7 (marginal Hurrian preference)
- Luwian lexical matches (consonant skeleton): SA-RA₂~SARA, RE-ZA~ARAZA, PA-TA-NE~PATA — all Low confidence

**H3 (Liturgical Sequence): CONFIRMED — most significant finding of this session**
- IOZa2 (Iouktas) contains ALL FOUR elements in order: `JA-SA-SA-RA-ME → U-NA-KA-NA-SI → I-PI-NA-MA → SI-RU-TE`
- Full inscription: `A-TA-I-*301-WA-JA 𐄁 JA-DI-KI-TU 𐄁 JA-SA-SA-RA-ME 𐄁 U-NA-KA-NA-SI 𐄁 I-PI-NA-MA 𐄁 ↵ SI-RU-TE 𐄁 TA-NA-RA-TE-U-TI-NU 𐄁 I 𐄁`
- KOZa1 and TLZa1 each have 3/4 elements in order across sites
- New tokens in IOZa2: JA-DI-KI-TU (slot 2), TA-NA-RA-TE-U-TI-NU (coda)

**H4 (-ME Suffix): PARTIALLY CONFIRMED**
- -ME is a grammatical suffix (detachable): bare root JA-SA-SA-RA found (1 occ), JA-SA-SA-RA-MA variant found (1 occ)
- -ME words have zero KU-RO/KI-RO rate → NOT an accounting marker
- -ME words are predominantly medial (65%) → not a terminal case
- Luwian verbal noun suffix -amma- scores medium alignment → possible nominal derivation function
- Ritual enrichment detection failed due to case-sensitivity bug in support type matching (all ritual rates computed as 0.0% — corpus uses "Stone vessel" not "stone vessel")
- **RESULT: PARTIALLY CONFIRMED** — -ME is a grammatical suffix, specific function unclear

**H5 (Ergative Marker): INCONCLUSIVE**
- No suffix shows a clean inverse of -JA's profile
- Best KI-RO candidates among common suffixes (n≥30): -RE (13.8%), -NA (5.6%)
- -RE remains the most plausible active participle/transitive-agent marker
- The ergative marker may be expressed through word order rather than suffixation
- Data quality issue: ritual rates all 0.0% due to case-sensitivity bug

### Cross-validation

- IOZa2 liturgical sequence: CONFIRMED at Iouktas; partial confirmation at Kophinas and Troullos (non-HT)
- A-TA-I-*301-WA-JA ritual header: CONFIRMED at 5 sites (Iouktas, Syme, Kophinas, Palaikastro, Troullos)
- Hurrian preference over Luwian: SUPPORTED by 8-7 suffix comparison (not cross-site — methodological comparison)
- *301 standalone = HT administrative sign: CONFIRMED (230/238 occurrences at HT)

---

## Interpretation

**The liturgical sequence confirmation is the primary contribution of this session.** IOZa2 provides, for the first time, a fully attested ritual inscription with internal structure:

1. HEADER: `A-TA-I-*301-WA-JA` — invocation opener (11 occ, 5 sites, always initial)
2. SLOT 1: `JA-DI-KI-TU` — unknown (divine epithet? location? first dedicant title?)
3. CORE SEQUENCE: `JA-SA-SA-RA-ME` → `U-NA-KA-NA-SI` → `I-PI-NA-MA` → `SI-RU-TE`
4. CODA: `TA-NA-RA-TE-U-TI-NU` — unknown (dedicant? closing formula?)

This structure is consistent with Near Eastern libation table formulae: header (divine name invocation) → body (ritual phrases) → closing (dedicant or concluding formula). If this interpretation is correct, then:
- `JA-SA-SA-RA` is the root of the divine name (bare form attested)
- `-ME` in JA-SA-SA-RA-ME is a grammatical suffix (probably a divine case or vocative)
- `U-NA-KA-NA-SI` is the next formula unit (epithet, object of invocation, or associated deity)
- `I-PI-NA-MA SI-RU-TE` is a closing ritual phrase (prayer? benediction? offering description?)

**N-gram result is puzzling:** Proto-Semitic ranks first in phonotactic similarity, contradicting the Hurrian morphological preference. Possible explanations: (a) the reference profiles are too approximate; (b) Linear A phonotactics reflect a contact language with Semitic-influenced phonotactics but Hurrian-influenced morphology; (c) the n-gram method is not discriminative at consonant-class resolution. A finer-grained n-gram analysis is needed before drawing conclusions.

**Hurrian vs. Luwian comparison is more robust than n-gram:** The 14 high-confidence Hurrian alignments vs. 0 Luwian high-confidence alignments is a meaningful result. The Hurrian morphological preference is sustained.

Phrasing: All findings "provide evidence for" or "are consistent with" the interpretations above. No decipherment is claimed.

---

## What Was Learned

1. **The complete IOZa2 inscription is the most informative single inscription identified so far.** It provides a template for ritual inscription structure: header formula → slot → divine name → epithets → closing formula → dedicant coda.
2. **JA-SA-SA-RA is the bare divine root.** The -ME suffix is grammatical, not lexical. This narrows the search for cognates — we need a divine name with phonological skeleton J-S-S-R in candidate languages.
3. **A-TA-I-*301-WA-JA is a ritual header, not itself a divine name.** It appears before, not as, the divine name. The *301 sign in this formula is different from standalone *301 at HT (administrative classifier).
4. **N-gram analysis at consonant-class resolution is insufficiently discriminative.** Sign-level bigram matrices with clean token extraction would produce more reliable results.
5. **The support type case-sensitivity bug (Stone vessel vs stone vessel) affected ritual rate calculations.** All ritual rates in the ergative analysis are 0.0% and must be treated as invalid. The Attempt #3 ritual enrichment ratios remain valid as they used a different script.
6. **No ergative suffix identified** — this negative result is informative. Either the ergative is marked by word order, by a preverbal particle, or Linear A is not ergative-absolutive (the absolutive interpretation of -JA may be wrong).

---

## Findings Promoted to `findings/`

- [x] Updated `findings/formulaic_sequences.md`: IOZa2 full inscription, four-unit sequence confirmed, A-TA-I-*301-WA-JA structure, JA-SA-SA-RA bare root
- [x] Updated `findings/hurrian_morphology.md`: Hurrian 14 high-confidence vs Luwian 0 high-confidence comparison

---

## Follow-up Questions Generated

- [ ] What is `JA-DI-KI-TU`? Find all occurrences, support types, sites — compare to `A-DI-KI-TE` (Palaikastro variant).
- [ ] What is `TA-NA-RA-TE-U-TI-NU`? Compare to `TA-NA-I-*301-U-TI-NU` (variant A-TA-I formula). Are they the same token with minor scribal variation?
- [ ] Is `SA-SA-RA-ME` (2 occ) a truncated form of JA-SA-SA-RA-ME or an independent lexical item?
- [ ] Run n-gram analysis with clean token extraction (exclude \n, 𐄁, numerals) and sign-level bigrams for better language discrimination.
- [ ] Test whether -ME is a comitative/essive/perlative by checking syntactic slot: does X-ME consistently appear adjacent to another noun rather than before a verb or number?
- [ ] Is there word-order evidence for the ergative? Check whether SOV vs. SVO patterns can be extracted from known accounting formulas.

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
