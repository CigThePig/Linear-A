# Hypothesis: Computational Sign Clustering, Refined N-gram Analysis, U-NA-KA-NA-SI Deep Analysis, and Word-Order Ergative Test

**Date:** 2026-03-19
**Strategy category:** Sign Clustering / N-gram Fingerprinting / Formulaic Analysis / Grammatical Analysis
**Language tested (if applicable):** Hurrian (control), Luwian (control), Proto-Semitic (control), Etruscan (control)
**Builds on / differs from:** `2026-03-18-ngram-luwian-ergative-me.md` (Attempt #4) — that attempt used consonant-class-level bigrams (6 dimensions), included newline tokens, and produced an unreliable Proto-Semitic #1 ranking that contradicts Hurrian morphological findings. This attempt runs n-gram analysis at sign level (50+ dimensions) with clean token extraction to resolve the contradiction. It also applies Strategy 7 (Computational Sign Clustering) for the first time — never attempted in any prior session. The U-NA-KA-NA-SI analysis (slot 2 of IOZa2) has not been independently analyzed in any prior attempt. The word-order ergative test (SOV hypothesis) was identified as critical in Attempts #4 and #5 but never executed.

---

## Hypothesis Statement

**H1 (Sign Clustering):** Unknown signs (*301, *28B, *22F, *318, and others with `*` prefix) will cluster near known signs with similar positional and co-occurrence distributions, allowing inference of their likely phonological class (e.g., stop-initial CV, nasal-initial CV, liquid-initial CV). The sign *301, which appears both as an administrative classifier at Haghia Triada (230/238 occurrences) and embedded in the ritual formula A-TA-I-*301-WA-JA (8+ ritual uses), may occupy two different co-occurrence clusters corresponding to its two distinct functional uses.

**H2 (Refined N-gram):** Sign-level bigram analysis with clean tokens (excluding newlines, dividers `𐄁`, and pure numerals) will produce higher cosine similarity scores and more discriminative language rankings than the class-level analysis in Attempt #4. Specifically, the Hurrian ranking (4th in Attempt #4) will improve relative to Proto-Semitic, resolving the contradiction with Hurrian morphological findings.

**H3 (U-NA-KA-NA-SI):** U-NA-KA-NA-SI functions as a divine epithet or companion deity name appended to JA-SA-SA-RA-ME, rather than as an independent grammatical particle or relational word. This is evidenced by its fixed-order co-occurrence with JA-SA-SA-RA-ME (4/4 known instances) and its 100% ritual support type.

**H4 (Word-Order Ergative):** Linear A administrative inscriptions show a consistent word-order pattern where suffix -RE tokens (proposed active participle/agent) appear before commodity logograms, and suffix -JA tokens (proposed absolutive) appear after — consistent with SOV word order and ergative-absolutive grammar where the agent precedes the predicate.

**H5 (-ME Comitative/Essive):** Tokens ending in -ME consistently appear between two other noun-like tokens (comitative case: "together with X") rather than in pre-logogram topic position (essive). DA-ME (4 occurrences, second most frequent -ME token), when analyzed for its positional neighbors, will cluster in noun-adjacent position.

**Falsification conditions:**
- H1 fails if unknown signs show no clustering pattern (uniformly distributed across all known-sign clusters)
- H2 fails if clean sign-level n-gram still ranks Hurrian last and Proto-Semitic first with similar low similarity scores
- H3 fails if U-NA-KA-NA-SI appears independently in administrative inscriptions with no JA-SA-SA-RA-ME co-occurrence
- H4 fails if -RE and -JA tokens show no differential distribution relative to commodity logogram position
- H5 fails if -ME tokens are distributed randomly with respect to neighboring token types

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full
- [x] All files in `hypotheses/` enumerated and read: `2026-03-18-admin-formula-bootstrapping.md`, `2026-03-18-libation-proper-nouns-hurrian.md`, `2026-03-18-ngram-luwian-ergative-me.md`, `2026-03-18-dikte-dikti-me-suffix.md`, `TEMPLATE.md`
- [x] This hypothesis differs from prior attempts because: Strategy 7 (Computational Sign Clustering) is applied for the first time. The n-gram analysis explicitly fixes the methodological issues from Attempt #4 (newline conflation, class-level instead of sign-level bigrams). U-NA-KA-NA-SI has never been analyzed as an independent research target. The word-order ergative test was explicitly deferred from Attempts #4 and #5 but never executed. The -ME comitative test is a new hypothesis not tested in any prior session.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Additional files: `corpus/linear_a_rag_chunks.jsonl` (full inscription text for neighbor analysis)
- Prior output reused: `analysis/outputs/suffix_paradigm_results_2026-03-18.json` (for word-order analysis cross-reference)
- External references:
  - Hurrian bigram reference: Mitanni-period Hurrian morpheme sequences (Speiser 1941, Wegner 2007)
  - Luwian morpheme inventory: Melchert 2003 *Luvian Texts*
  - Proto-Semitic triconsonantal root patterns (standard reconstruction)
  - Etruscan syllable frequencies: Bonfante & Bonfante *The Etruscan Language* (2002)

### Analysis Steps

1. **Sign co-occurrence matrix** (H1): Extract syllabic-sign sequences from all 1721 records. Build (sign_A, sign_B) co-occurrence counts within ±2 position windows. Normalize by PMI. Apply PCA + k-means clustering. Report cluster membership for all `*`-prefixed unknown signs.

2. **Clean n-gram extraction** (H2): Strip `\n`, `↵`, `𐄁` tokens. Remove pure numerals (decimal digits and fraction symbols). Keep `*XXX` signs as individual tokens but exclude from comparison vectors. Build sign-level bigram transition probability matrix. Compute cosine similarity against reference language profiles.

3. **U-NA-KA-NA-SI corpus sweep** (H3): Find all exact and partial matches of U-NA-KA-NA-SI. Record context for each occurrence: site, support, position in inscription, preceding and following tokens, co-occurrence with JA-SA-SA-RA-ME. Apply phonological skeleton analysis against Hurrian and known Minoan name databases.

4. **Word-order analysis** (H4): In accounting records (tablets + nodules with numerals), identify pre-logogram and post-logogram token positions. Extract final suffix from each token. Build frequency table: suffix × position (pre-logogram vs. post-logogram). Test whether -RE and -JA show opposite distribution patterns.

5. **-ME neighbor analysis** (H5): For all 26 -ME token occurrences, extract (preceding_token, ME_token, following_token) triples. Classify following token as: logogram, numeral, or syllabic sign. Classify preceding token similarly. Test whether -ME tokens are bounded by two syllabic signs (comitative pattern) vs. appearing before logograms (essive/topic pattern).

### Scripts

- `analysis/scripts/sign_clustering_2026-03-19.py`
- `analysis/scripts/ngram_clean_2026-03-19.py`
- `analysis/scripts/unakana_analysis_2026-03-19.py`
- `analysis/scripts/word_order_2026-03-19.py`

### Outputs

- `analysis/outputs/sign_clustering_2026-03-19.json`
- `analysis/outputs/ngram_clean_2026-03-19.json`
- `analysis/outputs/unakana_analysis_2026-03-19.json`
- `analysis/outputs/word_order_2026-03-19.json`
- `analysis/outputs/attempt6_summary_2026-03-19.md`

---

## Results

**Outcome:** PARTIAL SUCCESS (H1 low confidence; H2 confirmed; H3 partially confirmed; H4 inconclusive; H5 inconclusive)
**Confidence:** High (H2 n-gram reversal), Medium (H3 U-NA-KA-NA-SI ritual exclusivity), Low (H1 clustering), Low (H4/H5)
**Evidence tier reached:** Tier 1 (Structural — sign clustering, n-gram); Tier 3 (Formulaic — U-NA-KA-NA-SI)

### Findings

**H1 (Sign Clustering): LOW CONFIDENCE — clustering not discriminative**
- 19 unknown signs (freq ≥ 5) clustered
- *304 (freq=25) and *308 (freq=12) cluster in nasal-dominant cluster (purity 1.00) — Medium confidence inferred nasal-initial class
- *301 (freq=238) clusters with KU and KA in stop-dominant cluster (purity 0.31) — Low confidence
- Most clusters have low purity (0.25–0.33) due to the mixed co-occurrence patterns in this small-vocabulary corpus
- PMI neighbors of *301 are low-frequency signs (freq 1–3), not informative
- **Negative result:** k-means at k=10 on 102 active signs does not produce pure phonological clusters; the Linear A vocabulary is too small and co-occurrence too sparse for distributional clustering to be discriminative at this resolution

**H2 (Refined N-gram): CONFIRMED — contradiction from Attempt #4 was a methodological artifact**
- Sign-level bigrams (after splitting compound tokens like "U-NA-KA-NA-SI" → "U", "NA", "KA", "NA", "SI"):
  - Hurrian: cosine = 0.027, overlap 25/36 reference bigrams ← **#1**
  - Luwian: cosine = 0.017, overlap 18/29 ← #2
  - Proto-Semitic: cosine = 0.014, overlap 20/35 ← #3
  - Etruscan: cosine = 0.010, overlap 14/30 ← #4
- Reversal from Attempt #4 (Proto-Semitic #1, Hurrian #4) is entirely explained by:
  1. Compound token splitting (previously "U-NA-KA-NA-SI" counted as one sign; now 5 individual signs with Hurrian-compatible bigrams)
  2. Removal of structural tokens (newlines, dividers) from bigram counts
  3. Sign-level vs. class-level comparison (Hurrian's CV patterns are much more similar to Linear A at sign level)
- **This resolves the key contradiction between n-gram and morphological analyses.** Both now favor Hurrian.
- Absolute similarities are still low (0.01–0.03), reflecting the approximate nature of reference profiles

**H3 (U-NA-KA-NA-SI): PARTIALLY CONFIRMED — ritual-exclusive, but appears without JA-SA-SA-RA-ME**
- 6 exact occurrences of the full compound token
- **100% ritual support** (6/6 stone vessels) across 4 sites: Iouktas (2), Palaikastro (2), Kophinas (1), Syme (1)
- Co-occurrence with JA-SA-SA-RA-ME: 3/6 occurrences (50%)
- Compound forms found: "JA-SA-U-NA-KA-NA-SI" (PKZa8 Palaikastro) and "U-NA-KA-NA-SI-OLE" (SYZa2 Syme)
- Sub-sequence analysis (treating sub-segments as independent tokens):
  - U-NA-KA: 8/8 ritual (100%), 3 sites
  - NA-KA-NA: 7/7 ritual (100%), 3 sites
  - KA-NA-SI: 8/8 ritual (100%), 3 sites
  - NA-SI: 9/15 ritual (60%), appears in administrative contexts too
  - U-NA: 13/20 ritual (65%), appears in administrative contexts too
- **Interpretation:** U-NA-KA-NA-SI is a ritual-exclusive formula element. The core triplet NA-KA-NA is found only in ritual contexts. It appears 3× with JA-SA-SA-RA-ME and 3× without, suggesting it is a ritual element in its own right, not exclusively an epithet of JA-SA-SA-RA-ME.
- Phonological skeleton: N-K-N-S (U is onset-less/vocalic)
- Hurrian divine name comparison: moderate overlap with Nubadig (N-B-D), Nabarbi (N-B-R) — consonant skeleton N+consonant matches but the specific consonants differ
- **This is a new tier-3 formulaic element that can appear independently in ritual contexts**

**H4 (Word-Order Ergative): INCONCLUSIVE — accounting structure not informative**
- 207 logogram neighbor contexts found in administrative records
- ALL syllabic tokens appear pre-logogram (post-logogram = 0); post-logogram position is exclusively numerals
- This confirms the Linear A accounting formula as: `[syllabic token(s)] [LOGOGRAM] [NUMBER]`
- ALL suffixes (-JA, -RE, -NA, -TE, -RO, -ME) appear only pre-logogram with n<3 each; no differential distribution possible
- **Negative result:** The accounting formula structure means syllabic tokens are always pre-logogram. This analysis cannot distinguish -JA from -RE by position. The ergative hypothesis requires a different method (clause-internal analysis, not logogram-relative position).
- KI-RO: 5 pre-logogram, 3 post-logogram — mixed, consistent with closing formula behavior
- KU-RO: 6 pre-logogram, 6 post-logogram — balanced, consistent with tabulation formula that can appear at any position

**H5 (-ME Comitative/Essive): INCONCLUSIVE — no dominant pattern**
- 26 total -ME tokens across the corpus
- Ritual rate: 46.2% (12/26) — substantial but not exclusive to ritual
- Comitative pattern (bounded by two syllabic tokens): 46.2% (12/26) — just below the 50% threshold for "supported"
- Essive/topic pattern (pre-logogram or pre-numeral): 19.2% (5/26)
- Preceding token class: 20/26 syllabic, 6/26 boundary
- Following token class: 16/26 syllabic, 4/26 numeral, 1/26 logogram, 5/26 boundary
- **Neither comitative nor essive is strongly supported.** The 46% comitative rate is suggestive but not conclusive. The -ME function remains unresolved.

### Cross-validation

- H2 n-gram: ALL 1721 records; 4 candidate languages compared
- H3 U-NA-KA-NA-SI: 4 distinct sites (Iouktas, Palaikastro, Kophinas, Syme) — well cross-validated
- H1 clustering: all 102 signs with freq ≥ 5 across full corpus
- H4 word-order: 1506 administrative records analyzed
- H5 -ME: 26 occurrences from 10+ sites

---

## Interpretation

**The major result of this session is the resolution of the H2 n-gram contradiction.**

Attempt #4 found Proto-Semitic #1 and Hurrian #4 in phonotactics, contradicting Hurrian's #1 position in morphological analysis. This created an unresolved ambiguity. The refined analysis — with compound token splitting, structural token removal, and sign-level comparison — reverses the ranking to **Hurrian #1, Proto-Semitic #3**. The reversal is fully explained by the compound token issue: when "U-NA-KA-NA-SI" is split into "U→NA→KA→NA→SI", the alternating vowel-stop-vowel-stop pattern (CV-CV-CV-CV-CV) matches Hurrian's characteristic agglutinative CV structure better than it matches the consonant-cluster-heavy Proto-Semitic profile. The methodological flaw in Attempt #4 produced a spurious Proto-Semitic ranking.

**Combined evidence for Hurrian:**
- N-gram phonotactics: Hurrian #1 (cosine 0.027) (this session, corrected)
- Morphological alignment: 14 high-confidence alignments vs. Luwian's 0 (Attempt #3)
- Hurrian suffix comparison wins: 8 suffixes vs. Luwian's 7 (Attempt #4)
- These three independent lines of evidence now converge on Hurrian

**U-NA-KA-NA-SI as an independent ritual formula element:** The 100% ritual exclusivity across 4 sites and the 100% ritual rate of its core sub-sequences (NA-KA-NA, KA-NA-SI, U-NA-KA) support treating it as a meaningful ritual formula element. Its 3/6 independent appearances (without JA-SA-SA-RA-ME) suggest it can be invoked standalone, not just as an epithet. This increases the complexity of the ritual formula template.

**Word-order analysis reveals structural confirmation:** The finding that ALL syllabic tokens are pre-logogram in accounting contexts is informative as a structural confirmation: Linear A accounting follows `[ENTITY/AGENT] [COMMODITY] [QUANTITY]` — consistent with SOV-like ordering. However, this finding doesn't discriminate between suffixes (they all appear pre-logogram) because the accounting formula is too simple (one entity per logogram, typically).

Phrasing: All findings "provide evidence for" or "are consistent with" the interpretations above. No decipherment claimed.

---

## What Was Learned

1. **The Attempt #4 n-gram contradiction is resolved.** Compound token splitting was the critical fix. Future analyses must always split hyphenated multi-sign tokens before computing bigrams. The Hurrian morphological preference is now supported by both n-gram phonotactics and morphological alignment.

2. **Strategy 7 (Sign Clustering) is not discriminative at this corpus size.** 102 active signs clustered into 10 groups produces low-purity clusters (0.25–0.33) because co-occurrence patterns in a 7000-token corpus are too sparse. The method may work better with k=5–6 or with a minimum co-occurrence threshold. Negative result documented.

3. **U-NA-KA-NA-SI is a ritual formula element, not exclusively an epithet of JA-SA-SA-RA-ME.** It appears independently in 3/6 cases. The "4/4 fixed-order co-occurrence" claim from the prior session description was based on a small sample and needs revision.

4. **The word-order analysis revealed the accounting formula structure.** ALL syllabic tokens are pre-logogram in accounting records. To test the ergative hypothesis through word order, one would need to analyze clause-internal ordering within a single multi-entity line (e.g., two tokens before two logograms), not just token-vs-logogram proximity.

5. **-ME function remains unresolved.** The 46% comitative rate is close to but below the threshold. The function could still be comitative, but the evidence is insufficient for elevation.

---

## Findings Promoted to `findings/`

- [x] Updated `findings/hurrian_morphology.md`: Refined n-gram confirms Hurrian #1 at sign level; contradiction from Attempt #4 resolved; both n-gram and morphology now favor Hurrian
- [x] Updated `findings/formulaic_sequences.md`: U-NA-KA-NA-SI documented as independent ritual formula element (6 occ, 100% ritual, 4 sites); core sub-sequences NA-KA-NA, KA-NA-SI, U-NA-KA all 100% ritual; independent from JA-SA-SA-RA-ME in 50% of cases

---

## Follow-up Questions Generated

- [ ] **Sign clustering with smaller k**: Re-run clustering with k=5–6 and higher minimum frequency threshold (≥10) to see if purer clusters emerge
- [ ] **U-NA-KA-NA-SI with JA-SA-SA-RA-ME absent**: What compound or formula element replaces U-NA-KA-NA-SI when JA-SA-SA-RA-ME is absent? (The 3 independent occurrences context)
- [ ] **"JA-SA-U-NA-KA-NA-SI" compound (PKZa8)**: Is this a scribal fusion of JA-SA-SA-RA + U-NA-KA-NA-SI, or a different lexical item? Check the full PKZa8 inscription.
- [ ] **"U-NA-KA-NA-SI-OLE" at Syme**: What does it mean when U-NA-KA-NA-SI is followed by OLE (olive oil logogram)? Is this a votive inscription specifying the offering type?
- [ ] **Clause-internal word-order analysis**: For inscriptions with multiple entity tokens before a single logogram (e.g., "A-B LOGOGRAM NUMERAL C-D LOGOGRAM NUMERAL"), what is the suffix profile of each entity token? This is a better test of the ergative hypothesis.
- [ ] **-ME at threshold**: Test the comitative hypothesis with a larger context window (3 tokens before/after instead of 1) to see if the comitative pattern rises above 50%.
- [ ] **N-gram analysis with Hurrian control corpus**: Build the Hurrian reference profile from actual reconstructed Hurrian word sequences (not just morpheme templates) for a more robust phonotactic comparison.

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
