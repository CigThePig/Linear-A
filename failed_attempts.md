# Linear A Decipherment: Failed and Inconclusive Attempts

## Purpose

This file is **mandatory reading before beginning any new decipherment attempt.**

It records all approaches tried, why they failed or stalled, and what was learned. The goal is to prevent duplicate effort and accumulate negative knowledge — knowing what does NOT work is as valuable as knowing what does.

Linear A has defeated every serious decipherment attempt for 70+ years. That means this file will grow. A growing file is not failure — it is evidence that the research is being conducted rigorously.

**After every session**, prepend a new entry to the Attempt Log below, even for inconclusive results.

---

## Entry Schema (Copy This Block for Each New Attempt)

```
---

### Attempt #N — [Short Descriptive Title]

**Date:** YYYY-MM-DD
**Hypothesis file:** `hypotheses/YYYY-MM-DD-hypothesis-name.md`
**Session:** [Claude session ID or researcher name]
**Strategy:** [e.g., Language Family Testing / Suffix Analysis / Logogram Identification / Administrative Bootstrapping]
**Language tested (if applicable):** [e.g., Proto-Semitic, Luwian, Hurrian, isolate, N/A]

#### Summary of Approach
[2–4 sentences describing what was attempted and why]

#### Data Used
- Files: [list corpus files consulted]
- Inscriptions analyzed: [count or IDs]
- Methods: [e.g., bigram frequency, suffix clustering, cross-language lexeme matching]

#### Results
**Outcome:** [FAILED / INCONCLUSIVE / PARTIAL SUCCESS / SUCCESS]
**Key finding:** [One sentence]
**Confidence:** [Low / Medium / High]

#### What Was Learned
[Even failures teach something. Document it explicitly — do not leave this blank.]

#### Why a Re-attempt Needs to Differ
[Explain what would need to be different for another attempt at this angle to succeed]

#### Follow-up Questions Generated
- [ ] [Question 1]
- [ ] [Question 2]
```

---

## Attempt Log

<!-- Newest entries at the top -->

---

### Attempt #10 — Intra-Inscription Case Validation, NI Commodity ID, -DA Disambiguation, Pre-Logogram Sweep

**Date:** 2026-03-21
**Hypothesis file:** `hypotheses/2026-03-21-intra-inscription-ni-da-prelexical.md`
**Strategy:** Suffix Analysis / Logogram Identification / Administrative Bootstrapping
**Language tested (if applicable):** Hurrian (primary for grammar)

#### Summary of Approach

Four follow-up analyses on Attempt #9's open questions: (H10a) intra-inscription case validation — check whether the cross-inscriptional case paradigm (A-JA, A-RU, etc.) appears within single tablets; (H10b) NI commodity identification — determine what commodity NI represents using co-occurrence and context patterns; (H10c) -DA grammatical disambiguation — separate ritual toponyms from grammatical -DA case suffixes; (H10d) pre-logogram lexical sweep — identify recurring tokens before known logograms as vocabulary candidates.

#### Result: MIXED — Two negative (informative), one supported, one structural discovery

**H10a (NEGATIVE, INFORMATIVE):** Zero inscriptions contain 2+ case forms of the same stem. This is a corpus-structure finding: Linear A administrative tablets are single-subject inventory records (like Linear B), not narrative texts. The cross-inscriptional case paradigm evidence remains valid. Intra-inscription case validation is structurally impossible with this corpus.

**H10b (PARTIALLY SUPPORTED):** NI identified as an administrative agricultural commodity: ritual enrichment 0.5x (below baseline), 87% tablet support, co-occurrence profile dominated by VIN (26.9%), CYP (25.4%), GRA (22.4%). Average quantity 9.4, fraction-before rate 22.4%. Fig hypothesis scores highest (3 points): bulk quantities, agricultural context, absence of "FIG" token in corpus (0 occurrences). **NI = probable fig logogram or equivalent plant commodity. Confidence: High for logogram status; Medium for fig identification.**

**H10c (KEY NEGATIVE FINDING):** -DA disambiguation into proper nouns (9 tokens) vs. grammatical forms (7 tokens) revealed that BOTH classes show high ritual enrichment (Class A: 3.7x, Class B: 6.06x). The Hurrian dative -da hypothesis requires low ritual enrichment (<2.0x) — this prediction FAILS definitively. **-DA is a RITUAL DEDICATORY marker, not an administrative dative case suffix. Hurrian dative -da identification REJECTED.** Critical methodological note: I-DA (5 occurrences exclusively on stone vessels at Nerokurou, Palaikastro, Zakros) was misclassified as grammatical because stem "I" appears in the paradigm — I-DA is the Mt. Ida toponym and should be a proper noun. Even correcting this, -DA remains ritual-enriched throughout. Overall Hurrian compatibility downgraded from Medium-High to Medium.

**H10d (MOSTLY FAILED, STRUCTURAL DISCOVERY):** Only one token meets the 3-site/5-occurrence threshold for pre-logogram position: `𐝫` (Unicode U+1076B), appearing before 11 different logograms at 5 sites. This is a scribal entry/section marker (Tier 1 structural), not a vocabulary item. No new lexical vocabulary found. Pre-logogram position is not productive for vocabulary discovery because Linear A encodes commodity varieties as compound signs (OLE+KI, GRA+QE) rather than as preceding lexical tokens.

#### What Was Learned

1. Linear A administrative tablets are structurally equivalent to Linear B inventory lists — no narrative syntax within single inscriptions; all grammatical paradigm evidence must be cross-inscriptional
2. NI is a bulk agricultural commodity with administrative profile; fig identification is best current hypothesis; NI at Tel Haror suggests export commodity
3. -DA is a ritual dedicatory morpheme, not an administrative dative — definitively rejects Hurrian dative -da alignment
4. `𐝫` (U+1076B) is a scribal entry marker (like `𐄁`) — should be in exclusion lists in all future analyses
5. I-DA (Mt. Ida toponym) can be misclassified by paradigm-based disambiguation — support-type checking is required for toponym vs. case suffix distinction

#### Productive Directions Generated

- *22F remains the strongest unconfirmed logogram candidate (78.6% numeral-after, 4 sites) — should be the next vocabulary item targeted
- -DA function needs further investigation: is it always preceded by a divine name or sanctuary name? Test whether -DA tokens have ritual elements immediately before them
- The paradigmatic case evidence (17 stems with 2+ HC case variants) is the strongest Tier 5 finding to date but requires a different validation strategy than intra-inscription co-occurrence

---

### Attempt #9 — Paradigmatic Alternation, Divine Name Matching, Logogram Sweep, -DA/-NE Testing

**Date:** 2026-03-21
**Hypothesis file:** `hypotheses/2026-03-21-paradigm-divine-logogram.md`
**Session:** Claude (claude/continue-deciphering-B3uKU)
**Strategy:** Suffix Analysis / Logogram Identification / Hurrian Testing
**Language tested (if applicable):** Hurrian (morphological), Minoan-Greek (divine names), Luwian, Proto-Semitic

#### Summary of Approach

Four parallel analyses: (H9a) paradigmatic stem alternation search — finding the same root with multiple case suffixes; (H9b) phonological matching of ritual tokens against known divine name rosters; (H9c) systematic logogram sweep using numeral-after rate; (H9d) distributional profiling of -DA and -NE suffixes.

This was the first attempt to search for inflectional paradigms directly from corpus data (stem + suffix combinations) rather than testing suffixes one at a time.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records)
- Methods: Token extraction, suffix/stem decomposition, LCS consonant matching, frequency/co-occurrence profiling
- Scripts: `paradigm_alternation_2026-03-21.py`, `divine_name_match_2026-03-21.py`, `logogram_sweep_2026-03-21.py`, `da_suffix_test_2026-03-21.py`

#### Results
**Outcome:** PARTIAL SUCCESS

**Key findings:**
- H9a: 17 stems with 2+ HC case-suffix variants; stem "A" shows 5-case paradigm (A-JA, A-RU, A-NA, A-RE, A-DA) at 9 sites — strongest direct Tier 5 evidence to date
- H9b: JA-DI-KI-TU matches "Diktynna" at LCS=3, score=0.750 — first plausible divine name identification; JA-SA-SA-RA remains unidentified
- H9c: NI confirmed as new logogram candidate (7 sites, 68.4% numeral-after); *22F (4 sites, 78.6%) and *308 (3 sites, 75%) are additional candidates. Total FIG tokens in corpus = 0.
- H9d: -DA and -NE are distinct grammatical categories but neither fits Hurrian dative (-da) or plural nominative (-ne) cleanly; both INCONCLUSIVE

**Confidence:** H9a: Medium-High | H9b: Medium | H9c: Medium-High (NI) | H9d: Low

#### What Was Learned

1. The paradigmatic alternation method is productive — 17 stems confirmed with 2+ HC case variants, which proves an inflectional case system from corpus data alone
2. Linear A does not have FIG as a token; NI is the likely fig/agricultural logogram equivalent (7 sites)
3. JA-DI-KI-TU = Diktynna is phonologically plausible — supports the DI-KI = Dikte toponym hypothesis
4. -DA and -NE are active grammatical suffixes but their specific Hurrian correspondences are ambiguous; -DA's high ritual enrichment (4.40x) requires proper-noun separation before conclusions
5. The gap between Hurrian morphological predictions and Linear A corpus behavior remains: Hurrian ergative -š ≠ -RU, and -DA/-NE don't cleanly map to Hurrian dative/-ne. The Hurrian hypothesis has more support from structure than from specific morpheme correspondences

#### Why a Re-attempt Needs to Differ

For H9b: JA-SA-SA-RA divine name identification requires a different method — pure consonant LCS is insufficient for a 4-syllable token. Try a split analysis: if JA- is a prefix, test SA-SA-RA root separately against deities with s-r consonant skeleton.

For H9d: Before concluding on -DA, separate I-DA (toponym candidate for Mt. Ida) from other -DA tokens. Test whether remaining administrative -DA tokens show lower ritual enrichment and higher entity-receipt patterns.

#### Follow-up Questions Generated
- [ ] Can A-JA and A-RU appear in the same inscription with different structural roles (positional validation of case alternation)?
- [ ] Is NI specifically figs, or a different commodity? Check archaeological inventory at NI-attesting sites.
- [ ] What is the JA-SA-SA-RA root identity? Test SA-SA-RA consonants (s-r) against divine names with š-r skeleton (Ishhara, Asherah).
- [ ] Is -DA's high ritual rate driven by I-DA (Mt. Ida toponym)? Separate toponym tokens from case-marked tokens.

---

### Attempt #8 — *304 Logogram, A-DU Section Marker, Ergative Search, PO-TO Sweep

**Date:** 2026-03-20
**Hypothesis file:** `hypotheses/2026-03-20-logogram-section-ergative.md`
**Session:** Claude (claude/continue-deciphering-EmGSB)
**Strategy:** Logogram Identification / Administrative Bootstrapping / Suffix Analysis
**Language tested (if applicable):** Hurrian (ergative prediction tested)

#### Summary of Approach

Tested four sub-hypotheses identified from Attempt #7's unresolved questions: (1) sign *304 as an olive-related logogram, (2) A-DU as an administrative section header, (3) -RU as ergative case marker (inverse to absolutive -JA), and (4) cross-site presence of PO-TO-KU-RO. Used positional analysis for the logogram test, enrichment ratios for A-DU, and an "inverse-JA score" metric for the ergative search.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl`
- Inscriptions analyzed: All 1721 records
- Methods: Positional analysis (numeral-after rate), PMI computation, suffix co-occurrence profiling, inverse-JA scoring, complementarity testing

#### Results

**H8a (*304 logogram) — SUCCESS:**
- *304 numeral-after rate: 84.0% (above GRA control at 72.6%)
- PMI with OLIV: 5.009, with OLE: 4.219 — olive-product commodity confirmed (values corrected 2026-03-21 from record-level PMI recomputation; prior values 4.328/3.968 used mixed sample space — see code_issues.md CI-003)
- 5 sites: HT, Khania, Phaistos, Pyrgos, Zakros
- **14th confirmed lexical item. High confidence, Tier 2.**

**H8b (A-DU section marker) — INCONCLUSIVE:**
- Record-initial: 70.0% (marginal threshold)
- Logogram enrichment: 1.49× (below 2× threshold)
- 3 sites (HT, Khania, Tylissos); CYP dominant in post-window
- Status: Retain at Low-Medium confidence; may be CYP-specific rather than general section header

**H8c (-RU ergative marker) — SUCCESS (with caveats):**
- Inverse-JA score: 3.761; 5 sites; 83.3% complementarity with -JA (score corrected 2026-03-21; prior value 4.448 used VIR co-occurrence = 0.0 due to VIR-family matching bug — see code_issues.md CI-001)
- KI-RO co-occurrence 13.3% vs. -JA 0.0%; word-terminal 72.2% vs. -JA word-initial 67.2%
- Corrected VIR co-occurrence: -RU 13.3%, -JA 10.3% (small but real difference, consistent with ergative interpretation)
- Hurrian ergative -š prediction (-SI) ranks 18th; -SA (now properly profiled) scores 0.990, below -JA baseline — Hurrian ergative prediction definitively rejected (both SI and SA; previously only SI was tested — see code_issues.md CI-002)
- **-RU is best ergative/oblique candidate. Medium confidence, Tier 5.**

**H8d (PO-TO-KU-RO cross-site) — FAILED:**
- 0 non-HT occurrences in full corpus sweep
- **PO-TO-KU-RO downgraded from Medium to Low confidence.**
**Outcome:** PARTIAL SUCCESS
**Key finding:** *304 confirmed as olive-related logogram (14th item); -RU identified as ergative/oblique candidate with clear inverse profile to -JA
**Confidence:** High (H8a), Medium (H8c), Low-Medium (H8b), Low (H8d)

#### What Was Learned

- Sign *304 demonstrates that positional analysis can identify "unknown" logograms even without Linear B parallels. The high numeral-after rate (84%) combined with olive PMI is sufficient for High confidence identification.
- The ergative-absolutive split IS detectable: -RU and -JA have 83.3% non-overlapping records at 5 sites each. This is the strongest case system finding to date.
- The Hurrian ergative prediction (-SI/-SA from -š) failed. This is a significant challenge to the Hurrian morphological hypothesis that requires explanation.
- The inverse-JA scoring method is a new reusable tool for identifying grammatical case markers in corpus data.

#### Why a Re-attempt Needs to Differ

- **A-DU:** To confirm, need a higher-power test: specifically analyze the commodity type in each A-DU record, not just the 5-token window. Also need to check A-DU occurrences at Khania and Tylissos individually.
- **Hurrian ergative:** Needs phonological explanation for why -RU doesn't map to Hurrian -š, or needs comparison against Hurrian instrumental -ae to see if -RU fits better as instrumental.
- **PO-TO-KU-RO:** Requires physical discovery of new inscriptions at non-HT sites.

#### Follow-up Questions Generated

- [ ] What is *304 specifically? (olive paste, container, quality grade, by-product?)
- [ ] Is -TU allomorphic with -RU or a distinct case marker?
- [ ] Is -RU instrumental rather than ergative? (Corrected VIR rate is 13.3% vs. 10.3% for -JA — small difference, not diagnostic alone)
- [ ] Why does Hurrian -š not correspond to -RU? Phonological bridge needed.
- [ ] Is A-DU specifically a CYP-section marker rather than a general section header?

---

### Attempt #7 — -RO Paradigm, Lexical Expansion, *301 Disambiguation

**Date:** 2026-03-19
**Hypothesis file:** `hypotheses/2026-03-19-ro-paradigm-lexical-expansion.md`
**Session:** Claude (claude/continue-deciphering-qMqnk)
**Strategy:** Suffix Analysis / Administrative Bootstrapping / Sign Distribution
**Language tested (if applicable):** Hurrian (comparison only)

#### Summary of Approach

Three parallel hypotheses: (H1) tokens ending in -RO cluster in terminal positions like KU-RO, suggesting -RO is a productive completive suffix; (H2) frequent pre-logogram sequences in admin records are candidate new lexical items; (H3) sign *301 has distinct distributional profiles in admin vs. ritual contexts. Scripts analyzed all 1721 corpus records.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl`
- Inscriptions analyzed: All 1721 (H1, H3); 1509 admin records (H2)
- Methods: Positional analysis (relative position within inscription), pre-logogram window extraction, PMI co-occurrence matrix, admin/ritual register separation

#### Results
**Outcome:** PARTIAL SUCCESS

**H1 (-RO paradigm): FAILED** by strict threshold (40% terminal rate vs. 60% threshold). However:
- -RO tokens are 1.8× more terminal than baseline (22.5%), indicating weak real bias
- **PO-TO-KU-RO** identified as a "grand total" compound (appears AFTER KU-RO with larger numbers): HT122b `KU-RO 65 PO-TO-KU-RO 97`, HT131b `PO-TO-KU-RO 451 ½`. Medium confidence, HT-only, needs cross-site validation.
- -RO is NOT a productive suffix in the corpus — KU-RO and KI-RO are likely opaque roots, not [stem]-RO

**H2 (Lexical expansion): PARTIAL** (4 qualifying candidates, threshold 5). Key findings:
- **A-DU**: 9 occurrences, 3 sites (HT, Khania, Tylissos), record-initial or section-initial position in 7/9 occurrences. Likely an **administrative section header word**. Low-Medium confidence.
- **SA-RA₂**: 20+ occurrences at HT ONLY; appears after KU-RO introducing supplementary entries (CYP 5 appended to main total). HT-specific — cannot cross-validate. Low confidence.
- **Sign *304**: 14 occ, 2 sites, appears before OLE/OLIV — possible unknown administrative sign

**H3 (*301 context separation): INCONCLUSIVE** — 0 ritual occurrences of standalone *301 found. BUT:
- **CRITICAL STRUCTURAL FINDING:** Sign *301 appears at FIRST POSITION in **97.6% of admin occurrences** (246 records). It is an **administrative tablet initializer / scribal header mark**, not a phoneme or logogram.
- Admin site distribution: HT (230), Khania (14), Knossos (1), Zakros (1)
- PMI top partner: MA-RE (4.03), confirming *301-headed tablets involve person/transaction records

**Confidence:** Low-Medium for new lexical items; High for *301 positional function

#### What Was Learned

1. **-RO is NOT a productive suffix.** KU-RO and KI-RO are opaque roots. A future re-attempt at -RO analysis would need to apply morphological stripping rules (removing root vs. affix) rather than treating the whole token as root+suffix.
2. **Sign *301 is resolved as a tablet initializer** — one of the strongest structural findings in the project (97.6% first-position rate across 4 sites). This is a non-phonemic scribal convention, not a regular sign value. The ritual formula A-TA-I-*301-WA-JA embeds it as a phonetic component.
3. **A-DU is a new cross-site functional word** (3 sites, record-initial) — the first new administrative formula word candidate since KU-RO/KI-RO. Semantics unclear but position is consistent.
4. **PO-TO-KU-RO** extends the KU-RO formula family — "grand total" interpretation is strong from positional evidence (appears after KU-RO, with larger number). Needs cross-site validation.
5. Pre-logogram token mining is limited by HT dominance (64% of corpus) — most frequent pre-logogram sequences are HT-only.

#### Why a Re-attempt Needs to Differ

- A -RO re-attempt would need to first identify all compound tokens containing KU-RO as a root (e.g., PO-TO-KU-RO, *23M-KU-RO) and test whether PO-TO- prefix appears with other roots
- A lexical expansion re-attempt would benefit from focusing on 2nd-tier sites (Khania, Phaistos, Zakros) exclusively, removing HT dominance bias
- H3 (*301) is now resolved — no need to revisit

#### Follow-up Questions Generated
- [ ] Does PO-TO-KU-RO appear at non-HT sites? (search entire corpus for PO-TO- prefix)
- [ ] What is the full paradigm of KU-RO compounds? Are there other X-KU-RO forms?
- [ ] What does MA-RE mean? High-PMI with *301-initial records suggests it's a key admin term in the *301 document class.
- [ ] Is A-DU related to a Hurrian preposition/conjunction (*andi*, *adi*)? Or Linear B parallel?
- [ ] What does SA-RA₂ mean in the context of supplementary CYP entries at HT?
- [ ] Is *304 a logogram for a type of oil vessel or a person category sign?

---

### Attempt #6 — Computational Sign Clustering, Refined N-gram, U-NA-KA-NA-SI Analysis, Word-Order Test

**Date:** 2026-03-19
**Hypothesis file:** `hypotheses/2026-03-19-sign-clustering-ngram-unakana-wordorder.md`
**Session:** claude/continue-deciphering-kAv66
**Strategy:** Sign Clustering (Strategy 7), N-gram Fingerprinting (Strategy 9 revision), Formulaic Analysis, Grammatical Analysis
**Language tested (if applicable):** Hurrian, Luwian, Proto-Semitic, Etruscan (n-gram comparison)

#### Summary of Approach

Five analyses executed: (1) First application of Strategy 7 — computational sign clustering via PMI co-occurrence matrix + PCA + k-means on 102 active signs; (2) Refined n-gram fingerprinting at sign level (fixed Attempt #4's compound token issue and structural token conflation); (3) Deep analysis of U-NA-KA-NA-SI as an independent research target across all 1721 records; (4) Word-order analysis for the ergative hypothesis — tested whether -JA appears post-logogram and -RE appears pre-logogram in accounting inscriptions; (5) -ME comitative/essive test via neighbor token classification.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records)
- Scripts: `sign_clustering_2026-03-19.py`, `ngram_clean_2026-03-19.py`, `unakana_analysis_2026-03-19.py`, `word_order_2026-03-19.py`
- Methods: PMI co-occurrence matrix, k-means clustering (k=10), sign-level bigram comparison, token substring search, logogram-neighbor position analysis

#### Results
**Outcome:** PARTIAL SUCCESS (H1 low confidence; H2 confirmed; H3 partially confirmed; H4/H5 inconclusive)
**Key finding:** The critical Attempt #4 contradiction (Proto-Semitic #1 / Hurrian #4 in n-gram) is RESOLVED. At sign level with compound token splitting, Hurrian ranks #1 (cosine 0.027 vs. Proto-Semitic 0.014). The contradiction was a methodological artifact of treating multi-sign tokens like "U-NA-KA-NA-SI" as single opaque units instead of splitting them into individual CV signs for bigram computation.
**Confidence:** High (H2 reversal documented), Medium (H3 U-NA-KA-NA-SI), Low (H1 clustering), Inconclusive (H4/H5)

#### What Was Learned
1. **Hurrian n-gram ranking restored**: Three independent lines of evidence (n-gram phonotactics, morphological alignment, suffix comparison) all now favor Hurrian. The language family assessment is elevated from Medium to Medium-High confidence.
2. **Strategy 7 is not discriminative at this corpus size**: k-means clustering on 102 signs with ~6,500 tokens produces mostly low-purity clusters (purity 0.25–0.33). *304 and *308 cluster near nasal-initial signs (purity 1.00, Medium confidence) but most unknown signs produce Low confidence results.
3. **U-NA-KA-NA-SI is 100% ritual** (6/6 stone vessels, 4 sites); appears independently in 3/6 cases (not exclusively dependent on JA-SA-SA-RA-ME as assumed). Core sub-sequences NA-KA-NA, KA-NA-SI, U-NA-KA are also 100% ritual.
4. **Word-order analysis cannot distinguish suffix position bias** in simple accounting formulas because all syllabic tokens appear pre-logogram (post-logogram is always a numeral). A clause-internal approach is needed.
5. **-ME comitative hypothesis inconclusive**: 46% of -ME tokens appear between two syllabic tokens (suggestive of comitative) but does not reach 50% threshold. -ME function remains open.
6. **Methodological discovery**: The compound token representation in the corpus (multi-sign words stored as single hyphenated tokens) must always be split before sign-level analysis. This affects bigram computation, sign frequency, and co-occurrence matrices.

#### Negative Results (Documented)
- H1 (sign clustering): Low confidence — corpus too small for discriminative k-means at k=10; must retest with k=5–6 or higher frequency threshold
- H4 (word-order ergative): Inconclusive — accounting formula structure prevents post-logogram syllabic tokens from appearing; method does not test the hypothesis
- H5 (-ME comitative): Inconclusive — 46% comitative pattern, below 50% threshold

#### Follow-up
- Run Strategy 5 (Proto-Semitic controlled morphological comparison) to test whether the n-gram demotion of Proto-Semitic also applies to morphology
- Analyze PKZa8 ("JA-SA-U-NA-KA-NA-SI" compound) and SYZa2 ("U-NA-KA-NA-SI-OLE") in detail
- Retry clustering with k=5–6 and freq≥10 threshold
- Build Hurrian n-gram reference from actual attested word sequences, not just morpheme templates

---

### Attempt #5 — DI-KI Element Analysis, IOZa2 Coda Identification, -ME Suffix Positional Analysis

**Date:** 2026-03-18
**Hypothesis file:** `hypotheses/2026-03-18-dikte-dikti-me-suffix.md`
**Session:** claude/decipher-and-document-AKvKy
**Strategy:** Libation Table Analysis (Strategy 6) / Proper Noun Isolation (Strategy 3) / Grammatical Analysis
**Language tested (if applicable):** Minoan (internal structure), Hurrian (morphological comparison)

#### Summary of Approach

Three targeted corpus searches built on the confirmed IOZa2 liturgical sequence from Attempt #4: (1) searched all 1721 inscriptions for the DI-KI element to test whether JA-DI-KI-TU and A-DI-KI-TE are variants of a shared sacred toponym; (2) analyzed all TA-NA-* and *-U-TI-NU tokens to identify whether IOZa2's coda is a variant of IOZa6's header; (3) tested whether -ME tokens appear in early syntactic positions (vocative hypothesis).

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records)
- Inscriptions analyzed: all 1721; DI-KI found in 9 inscriptions; TA-NA-* in 10; -ME in 26
- Methods: substring token search, positional analysis (relative word position), ritual enrichment ratio, structural slot comparison

#### Results
**Outcome:** PARTIAL SUCCESS (H1 substantially supported; H2 refuted and reframed; H3 inconclusive)
**Key finding:** DI-KI element is strongly ritual-enriched (7.4x, 67% vs 9% baseline), appears in fixed "slot 1" position after ritual header at BOTH Iouktas and Palaikastro — making it an integral component of the liturgical sequence template, not an incidental token.
**Confidence:** Low-Medium (H1), Low (H2 revised), Low (H3)

#### What Was Learned
1. **DI-KI is a slot-1 liturgical element**: confirmed at 2 sites (Iouktas: JA-DI-KI-TU; Palaikastro: A-DI-KI-TE/A-DI-KI-TE-TE). The liturgical sequence template now has 7 positions: [HEADER] → [DI-KI] → [JA-SA-SA-RA-ME] → [U-NA-KA-NA-SI] → [I-PI-NA-MA] → [SI-RU-TE] → [CODA]
2. **TA-NA-I-*301-U-TI-NU is a header, not a coda**: appears inscription-initial in IOZa6; is a variant of A-TA-I-*301-WA-JA (both contain *301, both initial)
3. **-U-TI-NU is Iouktas-site-specific**: 3 occurrences, all Iouktas stone vessels; possibly a sanctuary identifier
4. **-ME positional vocative hypothesis FAILED**: -ME tokens show no early-position clustering; mean position (0.471) not different from non-ME ritual tokens (0.448)
5. **-ME ritual enrichment is 5.13x** (corrected from earlier 3.01x — previous analysis had support-type case-sensitivity bug)
6. **JA-SA-SA-RA-ME → U-NA-KA-NA-SI ordering is structurally locked**: 4/4 co-occurrences in this fixed order across 3 sites
7. Administrative DI-KI uses (DI-KI-SE at HT) appear in personal name lists — DI-KI may have been used as a toponym giving rise to personal names

#### Why a Re-attempt Needs to Differ
- **H1 (DI-KI toponym)**: Next step requires checking whether DI-KI or its phonological equivalent appears in Aegean place names, Linear B Knossos tablets, or Greek mythology references to Dikte/Dikti. Additional evidence needed to raise from Low-Medium to Medium confidence.
- **H2 (coda)**: TA-NA-RA-TE-U-TI-NU remains unexplained as a coda. Its structure (7 syllables, -U-TI-NU terminal) may indicate a dedicant name or site-specific ritual coda. Future analysis should compare it to known Minoan personal name structures.
- **H3 (-ME function)**: Positional analysis failed. Next approach: check whether -ME appears specifically with divine names (vs. non-divine names), and whether there is a semantic distinction between JA-SA-SA-RA (bare) vs JA-SA-SA-RA-ME (with -ME) contexts.

#### Follow-up Questions Generated
- [ ] Does DI-KI appear in Linear B Knossos tablets as a toponym or logogram?
- [ ] What is the grammatical function of the -TU vs -TE suffix contrast on DI-KI (Iouktas vs Palaikastro)?
- [ ] What is U-NA-KA-NA-SI? — consistently follows JA-SA-SA-RA-ME; divine epithet, companion deity, or ritual formula?
- [ ] Is -U-TI-NU a sanctuary identifier for Iouktas peak sanctuary?
- [ ] What is the function of -ME when attached to divine names? (5.13x ritual enrichment but positional analysis inconclusive)

---

### Attempt #4 — N-gram Fingerprinting, Luwian Comparison, Liturgical Sequence Confirmation, -ME Suffix, Ergative Search

**Date:** 2026-03-18
**Hypothesis file:** `hypotheses/2026-03-18-ngram-luwian-ergative-me.md`
**Session:** claude/continue-deciphering-2U6cg
**Strategy:** N-gram Fingerprinting (Strategy 9) / Luwian Comparison (Strategy 4) / Liturgical Sequence Follow-up (Strategy 6) / Grammatical Analysis
**Language tested (if applicable):** Luwian (comparative morphology), Proto-Semitic/Etruscan/Hurrian (n-gram control)

#### Summary of Approach

Five-part analysis: (1) N-gram phonotactic fingerprinting comparing Linear A bigram distributions against Hurrian, Luwian, Proto-Semitic, and Etruscan at consonant-class resolution; (2) Luwian morpheme alignment using the same 5-point rubric as the Attempt #3 Hurrian test, enabling direct comparison; (3) verification of the four-unit liturgical sequence `JA-SA-SA-RA-ME → U-NA-KA-NA-SI → I-PI-NA-MA → SI-RU-TE` in single inscriptions; (4) -ME suffix syntactic analysis and JA-SA-SA-RA root isolation; (5) ergative marker search by constructing an inverse-absolutive profile.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records), `corpus/linear_a_rag_chunks.jsonl`
- Inscriptions analyzed: all 1721
- Methods: consonant-class bigram matrices, cosine similarity, KL-divergence, Luwian morpheme scoring (5-point rubric), token membership testing, position analysis, inverse-profile ergative ranking

#### Results
**Outcome:** PARTIAL SUCCESS
**Key finding:** IOZa2 (Iouktas) contains the complete four-unit liturgical sequence in a single inscription; Hurrian retains marginal morphological preference over Luwian (8-7 suffix wins); n-gram analysis inconclusive (Proto-Semitic ranked first, inconsistent with morphological results).
**Confidence:** High (liturgical confirmation), Low-Medium (Luwian vs. Hurrian), Low (n-gram), Low-Medium (-ME as grammatical suffix)

#### What Was Learned

1. **IOZa2 (Iouktas) is now the most informative single ritual inscription identified.** It contains the complete sequence plus a header (A-TA-I-*301-WA-JA), a slot-1 token (JA-DI-KI-TU), and a coda (TA-NA-RA-TE-U-TI-NU). This provides a template for ritual inscription structure.
2. **JA-SA-SA-RA is confirmed as the bare divine root** — the bare form and a -MA variant were found, proving -ME is a grammatical suffix, not a root-integral element.
3. **Hurrian retains a marginal morphological preference over Luwian.** 14 vs. 0 high-confidence alignments is the key metric. But the n-gram result (Proto-Semitic first, Hurrian last) creates an unresolved contradiction.
4. **The n-gram fingerprinting method at consonant-class resolution is insufficiently discriminative** — newlines, unknown signs, and approximate reference profiles all degrade the result. Sign-level bigrams with clean token extraction are needed.
5. **No ergative suffix identified** — either the ergative is expressed by word order, by a preverbal particle, or the absolutive interpretation of -JA is incorrect. This is a useful negative result.
6. **Support type case-sensitivity bug**: corpus uses "Stone vessel" (capitalized) but analysis scripts used lowercase, causing all ritual rate calculations to compute as 0.0%. Relative comparisons between suffixes remain valid; absolute ritual rates are incorrect.
7. **Two new tokens identified for future analysis:** JA-DI-KI-TU (IOZa2 slot 1; compare to A-DI-KI-TE at Palaikastro) and TA-NA-RA-TE-U-TI-NU (coda of IOZa2).

#### Why a Re-attempt Needs to Differ

- N-gram analysis: needs clean token extraction (filter \n, 𐄁, numerals, logograms) and sign-level bigrams rather than consonant-class bigrams
- New tokens JA-DI-KI-TU and TA-NA-RA-TE-U-TI-NU need full corpus analysis
- The -ME suffix function needs syntactic slot analysis
- The ergative should be investigated through word-order analysis (SOV pattern testing)
- The n-gram vs. morphological contradiction must be addressed before Hurrian can be elevated as preferred hypothesis

#### Follow-up Questions Generated
- [ ] What is `JA-DI-KI-TU`? Find all occurrences; compare to `A-DI-KI-TE` at Palaikastro (shared DI-KI element)
- [ ] What is `TA-NA-RA-TE-U-TI-NU`? Compare to `TA-NA-I-*301-U-TI-NU` — same token with scribal variation?
- [ ] Run n-gram analysis with clean token extraction and sign-level bigrams
- [ ] Is the n-gram vs. morphological contradiction explainable by contact-language dynamics?
- [ ] What is the syntactic slot of -ME words? (comitative? essive? perlative?)
- [ ] Is there word-order (SOV) evidence in the corpus that explains why no ergative suffix is visible?

---

### Attempt #3 — Libation Table Formula Analysis + Proper Noun Isolation + Hurrian Morphology Testing

**Date:** 2026-03-18
**Hypothesis file:** `hypotheses/2026-03-18-libation-proper-nouns-hurrian.md`
**Session:** claude/continue-deciphering-xuj7F
**Strategy:** Libation Table Analysis / Proper Noun Isolation / Hurrian Language Testing
**Language tested (if applicable):** Hurrian (systematic comparison); Aegean toponyms (cross-reference)

#### Summary of Approach

Three-pronged extension of Attempt #2: (1) analyzed the ritual register (stone vessels, metal objects) using JA-SA-SA-RA-ME as an anchor to find structurally equivalent companion tokens across sites; (2) computed formal site-specificity scores for all multi-syllable tokens to isolate proper noun candidates, cross-referencing against known Aegean toponym consonant skeletons; (3) systematically tested whether Linear A's suffix distribution is compatible with the Hurrian case/voice morpheme inventory using a three-factor scoring system.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records), `analysis/outputs/suffix_paradigm_results_2026-03-18.json`
- Inscriptions analyzed: all 1721 for proper nouns and Hurrian testing; 136 ritual records for libation analysis
- Methods: support-type filtering, context window analysis, site-specificity scoring, consonant skeleton matching, three-factor morpheme alignment scoring, corpus-validated hypothesis testing

#### Results
**Outcome:** PARTIAL SUCCESS
**Key finding:** 10 ritual-exclusive tokens identified (100% ritual support); -JA confirmed as absolutive/intransitive marker (zero KI-RO at 17 sites, 59% word-initial); possible four-unit liturgical sequence `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` suggested by three overlapping bigram confirmations.
**Confidence:** Medium (ritual analysis), Medium-High (-JA morphology), Low (toponym candidates)

#### What Was Learned

1. The ritual register is structurally separate: 10 tokens are categorically exclusive to stone vessels and metal objects, never appearing on tablets or nodules. Mixing ritual and administrative corpora may obscure patterns in both.
2. -JA absolutive marker is now the most robustly supported grammatical claim in the project — zero KI-RO across 17 sites + word-initial dominance + low accounting co-occurrence all converge.
3. The -NA locative hypothesis PARTIALLY FAILED: -NA words appear in terminal accounting positions (33%) far more than a pure locative predicts. Either -NA is an accounting morpheme, or the locative is used in accounting contexts for commodity storage locations.
4. Proper noun isolation via consonant skeleton matching produces suggestive but low-confidence results — single-site candidates cannot be validated without cross-site occurrence.
5. Hurrian morphological alignment matrix found 14 high-confidence alignments, but this test needs to be run against other agglutinative languages (Luwian, Kartvelian, etc.) before Hurrian can be preferred over alternatives.
6. The `*301` sign (232 records as opening token; 11 ritual occurrences in `A-TA-I-*301-WA-JA`) is the most important unidentified sign in the corpus. Its paleographic identification is the single highest-priority action for future sessions.

#### Why a Re-attempt Needs to Differ

To advance beyond current Tier 3–5 findings:
- The liturgical sequence hypothesis needs a search for complete four-unit sequences in single inscriptions
- The -NA locative/accounting ambiguity needs a direct grammatical position test (pre-number vs. pre-logogram vs. record-initial)
- Toponym candidates need grammatical slot analysis, not just specificity scores
- The Hurrian test should be replicated against Luwian (Strategy 4) to determine which language family's morphology fits better
- N-gram fingerprinting (Strategy 9) should be run to provide an independent language family compatibility score

#### Follow-up Questions Generated
- [ ] Can `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` be found complete in a single inscription?
- [ ] What is sign `*301`? It appears in 232 records as opening token and in `A-TA-I-*301-WA-JA` (11 ritual occurrences at 3 sites)
- [ ] Is -NA a locative OR an accounting terminal marker OR both? Line-level positional analysis required.
- [ ] Does KU-NI-SU appear in destination/origin grammatical slot at Haghia Triada? If so, this could be "Knossos" as a trade partner reference.
- [ ] What is -ME in JA-SA-SA-RA-ME? If it's a grammatical suffix, what is the bare root JA-SA-SA-RA?
- [ ] Run Luwian morpheme comparison (Strategy 4) as a control against the Hurrian results from this attempt.

---

### Attempt #2 — Administrative Formula Bootstrapping + Suffix Paradigm Reconstruction

**Date:** 2026-03-18
**Hypothesis file:** `hypotheses/2026-03-18-admin-formula-bootstrapping.md`
**Session:** claude/text-deciphering-plan-BBC6j
**Strategy:** Administrative Bootstrapping / Suffix Analysis
**Language tested (if applicable):** N/A (structural analysis; secondary Hurrian morphology comparison)

#### Summary of Approach

First corpus-scale computational analysis of all 1721 inscriptions. Used KU-RO ("total") as a positional anchor to find other tokens appearing in the closing-formula slot (immediately before a terminal number). Separately computed a suffix × logogram co-occurrence matrix to test whether word-final syllables cluster around specific administrative contexts, providing preliminary evidence for grammatical case suffixes.

#### Data Used
- Files: `corpus/linear_a_llm_master.jsonl` (all 1721 records)
- Inscriptions analyzed: all 1721
- Methods: positional frequency analysis, terminal-slot extraction, bigram frequency, suffix co-occurrence matrix

#### Results
**Outcome:** PARTIAL SUCCESS
**Key finding:** One new closing-formula candidate (*23M, 3 sites), two stable cross-site ritual bigrams discovered, and suffix differentiation confirms -RE strongly correlates with accounting contexts while -JA shows zero KI-RO co-occurrence.
**Confidence:** Medium

#### What Was Learned

1. KI-RO is almost exclusively a Haghia Triada token (16/16 occurrences at HT) — cannot be used as a multi-site anchor without caution.
2. Unknown sign `*23M` appears in KU-RO-equivalent structural position at 3 sites — warrants paleographic investigation.
3. Ritual formula `I-PI-NA-MA SI-RU-TE` is stable across 4 cult sites; `JA-SA-SA-RA-ME U-NA-KA-NA-SI` confirmed as fixed bigram at 2 sites.
4. Suffix -RE correlates most strongly with accounting vocabulary (KU-RO/KI-RO); -JA shows zero deficit-context co-occurrence at 17 sites — suggests distinct grammatical roles.
5. -TI strongly co-occurs with VIR (person logogram) — possible personal name or occupational suffix.

#### Why a Re-attempt Needs to Differ

This attempt used record-level co-occurrence. A follow-up should use line-level positional analysis to get finer-grained grammatical information. The `*23M` finding requires paleographic identification before any semantic claim. The ritual register bigrams should be analyzed separately using the `corpus/linear_a_rag_chunks.jsonl` for full inscription context.

#### Follow-up Questions Generated
- [ ] What is sign `*23M`? Paleographic comparison with Linear B needed.
- [ ] Can line-level positional analysis strengthen suffix role assignment?
- [ ] Why is KI-RO restricted to Haghia Triada? Scribal convention or palace-specific accounting practice?
- [ ] What is `U-NA-KA-NA-SI` — divine title, personal name, or ritual action?
- [ ] Do -TI words at HT cluster around specific scribes (personal name suffix hypothesis)?

---

### Attempt #1 — Prior Scholarship Survey (Pre-Computational Era)

**Date:** 2026-03-18
**Hypothesis file:** N/A (literature survey, not a corpus analysis)
**Session:** Project initialization
**Strategy:** Historical survey of published decipherment attempts
**Language tested:** Multiple (see below)

#### Summary of Approach

Survey of all major published decipherment attempts prior to this project, compiled to prevent re-inventing already-failed approaches. This is a seed entry — not a new attempt but a summary of 70 years of scholarly failure that must inform all future work.

#### Data Used

- Files: N/A (published scholarly literature)
- Inscriptions analyzed: N/A
- Methods: Literature review

#### Results

**Outcome:** FAILED (all prior scholarly attempts to date)
**Key finding:** No proposed decipherment of Linear A has achieved scholarly consensus. The language family and lexicon remain unknown.
**Confidence:** High (that all prior attempts failed)

#### Known Failed Approaches

**Cyrus Gordon (1960s–1990s) — Northwest Semitic**
- Proposed a Northwest Semitic (Phoenician-type) connection based on lexical parallels.
- Initial interest from some scholars, but ultimately rejected.
- Failure reason: Phonological correspondences were inconsistent; many proposed cognates were cherry-picked rather than arising from systematic rules. The methodology allowed too many degrees of freedom.
- What was learned: Any future Semitic hypothesis must enforce strict phonological correspondence rules with at least 3 independent corpus occurrences before accepting a cognate.

**Giulio Facchetti / early Chadwick — Etruscan Connection**
- Noted similarities between certain Linear A sequences and Etruscan vocabulary.
- Not broadly accepted.
- Failure reason: Insufficient systematic correspondences. The similarities may be coincidental given both languages are isolates with limited attested vocabulary.
- What was learned: Typological similarity between two isolates is not evidence of relationship. Etruscan comparisons require a sound-law framework, not ad hoc resemblances.

**Hubert La Marle — Semitic**
- Proposed a Semitic reading of Linear A with specific sign-value assignments.
- Rejected by specialists.
- Failure reason: Methodological problems — too many ad hoc choices in sign-value assignments, producing the appearance of readings without constraint. The method was not falsifiable.
- What was learned: Any new Semitic attempt must start from the conventional Linear B-derived transliteration values as a constraint, not invent new sign values from scratch.

**Yves Duhoux, Fred Woudhuizen, and others — Luwian/Anatolian**
- Proposed that Minoan is related to Luwian, an Anatolian Indo-European language.
- Continues to attract scholarly attention but no consensus.
- Failure reason (partial): Luwian morphology does not cleanly map onto Linear A endings in a systematic way. The proposed phonological equations have exceptions that are unaccounted for.
- What was learned: The Luwian hypothesis is not fully closed — it remains one of the more promising candidate language families. A computational test against the full 1721-inscription corpus (which these scholars did not have) is warranted. See Strategy 4 in CLAUDE.md.

**Linear A as Early Greek**
- Proposal that Minoan is a form of early or pre-classical Greek.
- Not taken seriously in modern scholarship.
- Failure reason: The script predates documented Greek presence on Crete by centuries. The phonological system is inconsistent with Proto-Greek reconstruction. Vocabulary does not align.
- What was learned: This hypothesis is closed. Do not re-attempt.

**Brent Davis (2014) — Structural Analysis Only**
- Careful computational analysis showing Linear A is consistent with agglutinative morphology with suffixing tendencies.
- Outcome: Structural characterization established, no language identification achieved.
- What was learned: The language is very likely agglutinative with SOV or SOV-adjacent word order. This is positive knowledge that constrains future hypotheses. Non-agglutinative language families (most Indo-European branches) are now lower priority.

**Yves Duhoux / Anaïs Clin — Statistical Approaches**
- Various statistical analyses of sign distribution in the 20th-21st century.
- Established frequency tables, positional distributions, and bigram statistics.
- Outcome: Structural knowledge confirmed; no lexical breakthroughs.
- What was learned: The corpus behaves statistically like a natural language (Zipf distribution, consistent positional patterns). The sign inventory is bounded (~50–60 core syllabic signs + logograms). This is established ground truth, not a frontier to re-explore from scratch.

#### What Was Learned (Synthesis)

1. The language is very likely **agglutinative** with **suffixing morphology** — this is the strongest structural constraint on future hypotheses.
2. The **commodity logograms and numeral system are understood** — this is established ground truth (GRA, VIN, OLE, KU-RO, KI-RO, the decimal system).
3. The language family is **genuinely unknown** — no hypothesis has been eliminated with certainty except early Greek.
4. **Computational corpus-scale analysis has not been systematically applied** to the full 1721-inscription dataset with the quality of data now available. This is the primary opportunity.
5. The **libation table religious register** has not been systematically separated from the administrative register for independent analysis.
6. **Proper noun isolation** (place names, personal names cross-referenced with Linear B and later Greek) has not been attempted with the current corpus at scale.

#### Why a Re-attempt Needs to Differ

Any new attempt that resembles the above must either:
- Apply strict phonological correspondence rules (not ad hoc)
- Use the full 1721-inscription corpus (not a small sample)
- Cross-validate findings across at least 3 distinct archaeological sites
- Anchor hypotheses to the confirmed vocabulary (KU-RO, KI-RO, logograms) as constraint

#### Follow-up Questions Generated

- [ ] Is the agglutinative structure consistent with Hurrian (ergative-absolutive) or Luwian (nominative-accusative)?
- [ ] Do any Linear A suffix paradigms map onto Hurrian case suffixes (-ne, -ve, -ra, -da)?
- [ ] Can the "JA-SA-SA-RA-ME" libation table formula be isolated as a test case for Semitic comparison with strict rules?
- [ ] What is the full distribution of "I-DA-MA-TE" and its variants across the corpus?
- [ ] Are there any objects in the corpus with both Linear A and another script system (potential bilinguals)?
- [ ] Which tokens have the highest site-specificity scores and are thus strongest proper noun candidates?
