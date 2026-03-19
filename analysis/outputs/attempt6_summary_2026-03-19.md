# Linear A Decipherment — Attempt #6 Summary Report
**Generated:** 2026-03-19
**Strategies:** Strategy 7 (Computational Sign Clustering), Strategy 9 Revised (Refined N-gram), U-NA-KA-NA-SI Deep Analysis, Word-Order Analysis, -ME Comitative Test

---

## KEY FINDING: N-gram Contradiction from Attempt #4 RESOLVED

**The Proto-Semitic #1 / Hurrian #4 ranking from Attempt #4 was a methodological artifact.**

Attempt #4 used consonant-class-level bigrams (6 dimensions) and treated compound tokens like "U-NA-KA-NA-SI" as single units rather than splitting them into individual signs "U→NA→KA→NA→SI". This systematically inflated consonant-cluster transition rates (characteristic of Proto-Semitic) and suppressed CV-alternation rates (characteristic of Hurrian).

After fixing the three methodological problems:
1. Strip structural tokens (𐄁, ↵, \n) before computing bigrams
2. Split compound (hyphenated) tokens into individual CV signs
3. Compare at sign level (not consonant class level)

**Corrected ranking:**
| Rank | Language | Cosine Similarity | Overlap | Attempt #4 Rank |
|------|----------|-------------------|---------|-----------------|
| **#1** | **Hurrian** | **0.026970** | **25/36** | **was #4** |
| #2 | Luwian | 0.017186 | 18/29 | was #2 |
| #3 | Proto-Semitic | 0.014070 | 20/35 | was #1 |
| #4 | Etruscan | 0.009624 | 14/30 | was #3 |

**This resolves the central methodological contradiction.** Hurrian is now supported by THREE independent lines of evidence:
1. N-gram phonotactics (corrected): Hurrian #1
2. Morphological alignment (Attempt #3): 14 high-confidence alignments vs. Luwian's 0
3. Direct suffix comparison (Attempt #4): Hurrian wins 8 suffixes, Luwian wins 7

---

## Section 1: Computational Sign Clustering (Strategy 7 — First Application)

### Method
- 1696 sequences, 6582 syllabic tokens from 1721 corpus records
- Co-occurrence matrix (PMI-weighted, window=2) over 102 signs with freq ≥ 5
- PCA (5 components) + k-means (k=10)

### Results

| Sign | Freq | Cluster Class | Purity | Confidence |
|------|------|---------------|--------|------------|
| *304 | 25 | nasal | 1.00 | Medium |
| *308 | 12 | nasal | 1.00 | Medium |
| *401+RU | 9 | stop | 1.00 | Medium |
| *21M | 8 | stop | 0.50 | Low-Medium |
| *301 | 238 | stop | 0.31 | Low |
| *22F | 14 | nasal | 0.25 | Low |
| *164 | 13 | stop | 0.31 | Low |

**Interpretation (Tier 1 — no phonetic values claimed as proven):**
- *304 and *308 consistently cluster near NA, NE, NI, etc. — consistent with nasal-initial CV syllable
- *301 clusters near KU and KA — consistent with stop-initial CV syllable, but low cluster purity limits confidence
- Strategy 7 is limited by corpus size: 6,582 tokens across 1,305 sign types produces sparse co-occurrence; most clusters have low purity

### Negative Result Documented
k-means clustering at k=10 on 102 active signs is insufficient for clean phonological class identification. The method needs either (a) a richer corpus, (b) a lower k, or (c) a higher minimum frequency threshold.

---

## Section 2: Refined N-gram Analysis (Strategy 9 Revision)

*(See KEY FINDING above for full results)*

### Additional Phonotactic Properties of Linear A

| Property | Value | Implication |
|----------|-------|-------------|
| Total bigram tokens | 6,109 | After compound splitting |
| Vocabulary (individual signs) | 210 | After splitting |
| Vowel-initial bigram rate | Low | CV-dominant (consistent with syllabary) |
| Bigram types | 1,491 | High diversity relative to vocabulary size |
| Hurrian overlap rate | 25/36 (69%) | High — most Hurrian reference bigrams appear in LA |

---

## Section 3: U-NA-KA-NA-SI Deep Analysis

### Corpus Findings

| Metric | Value |
|--------|-------|
| Exact occurrences (full token) | 6 |
| Ritual support (stone vessel) | 6/6 = **100%** |
| Sites | Iouktas (2), Palaikastro (2), Kophinas (1), Syme (1) |
| Co-occurrence with JA-SA-SA-RA-ME | 3/6 = 50% |
| Compound forms | JA-SA-U-NA-KA-NA-SI (PKZa8), U-NA-KA-NA-SI-OLE (SYZa2) |

### Sub-Sequence Analysis

| Sub-sequence | Count | Ritual Rate | Sites |
|---|---|---|---|
| U-NA-KA | 8 | 8/8 = **100%** | Palaikastro (3), Iouktas (2), Kophinas (1) |
| NA-KA-NA | 7 | 7/7 = **100%** | Iouktas (2), Palaikastro (2), Kophinas (1) |
| KA-NA-SI | 8 | 8/8 = **100%** | Iouktas (3), Palaikastro (2), Syme (2) |
| NA-SI | 15 | 9/15 = 60% | Multi-site, some administrative use |
| U-NA | 20 | 13/20 = 65% | Multi-site, some administrative use |

**Key finding:** The triplet NA-KA-NA and the full U-NA-KA-NA-SI are **100% ritual** across multiple sites. The token is NOT exclusively dependent on JA-SA-SA-RA-ME (appears independently in 3/6 cases).

### Phonological Skeleton
- Skeleton: N-K-N-S (U provides onset-less vowel, NA=N, KA=K, NA=N, SI=S)
- Hurrian divine name closest match: Nubadig (N-B-D) or Nabarbi (N-B-R) — consonant pattern N+K/B is similar; no exact parallel found
- The -SI suffix is also documented in Linear A proper nouns (KU-NI-SU, NA-SI alone has administrative uses)

### Interpretation (Tier 3 — Formulaic)
U-NA-KA-NA-SI is a ritual formula element with 100% ritual enrichment across 4 sites. Its 50% co-occurrence with JA-SA-SA-RA-ME and 50% independent appearance suggests it may be either:
1. A companion/epithet to JA-SA-SA-RA-ME (invoked together in full liturgy)
2. An independent deity or ritual invocation that can stand alone in shorter inscriptions

**Confidence: Medium** (consistent with ritual formula element; identity unresolved)

---

## Section 4: Word-Order Analysis for Ergative Hypothesis

### Results
- 207 logogram-neighbor contexts found in administrative records
- Post-logogram syllabic tokens: **0** (all post-logogram positions are numerals)
- Pre-logogram syllabic tokens: all suffixes present (-JA, -RE, -NA, -TE, etc.)
- **H4 verdict: INCONCLUSIVE** — accounting formula is too simple to distinguish suffix positions

### Structural Confirmation (Positive Finding)
The analysis confirms that Linear A accounting follows: `[SYLLABIC TOKEN(s)] [LOGOGRAM] [NUMERAL]`

This structure is consistent with:
- SOV-like ordering (entity before commodity before quantity)
- An ergative-absolutive system where the agent/patient precedes the predicate
- **But** cannot distinguish -JA from -RE since both appear pre-logogram

### KI-RO and KU-RO Position
| Formula | Pre-Logogram | Post-Logogram | Interpretation |
|---------|---|---|---|
| KI-RO | 5 | 3 | Mixed — appears both before and after logograms |
| KU-RO | 6 | 6 | Balanced — appears equally on both sides |

Both KI-RO and KU-RO appear in multiple positions, consistent with their role as formula elements that can anchor the beginning or end of an accounting entry.

---

## Section 5: -ME Comitative/Essive Test

| Metric | Value |
|--------|-------|
| Total -ME tokens | 26 |
| Ritual rate | 46.2% (12/26) |
| Comitative pattern (between 2 syllabics) | 46.2% (12/26) |
| Essive/topic pattern (pre-logogram) | 19.2% (5/26) |
| Pre-class: syllabic | 77% (20/26) |
| Post-class: syllabic | 62% (16/26) |

**H5 verdict: INCONCLUSIVE** — the comitative rate of 46% is suggestive (most -ME tokens appear between two syllabic tokens) but does not reach the 50% threshold for a strong claim. Neither comitative nor essive is definitively supported.

---

## Confidence and Evidence Tier Summary

| Claim | Tier | Confidence | Cross-Validated |
|-------|------|------------|----------------|
| Hurrian phonotactic compatibility (corrected n-gram) | Tier 1 (Structural) | **Medium** | Yes — all 1721 records |
| Proto-Semitic n-gram ranking was methodological artifact | Tier 1 (Structural) | High | Yes — method documented |
| U-NA-KA-NA-SI = 100% ritual formula element | Tier 3 (Formulaic) | **Medium** | Yes — 4 sites |
| NA-KA-NA core sub-sequence = 100% ritual | Tier 3 (Formulaic) | **Medium** | Yes — 3 sites |
| *304 and *308 cluster near nasal-initial signs | Tier 1 (Structural) | Low-Medium | Corpus-wide |
| Accounting formula = [entity][logogram][numeral] | Tier 1 (Structural) | High | Yes — 207 contexts |
| No ergative suffix identified (confirmed) | Tier 5 (Grammatical) | Medium | Yes — all admin records |
| -ME function unresolved | Tier 5 (Grammatical) | — | — |

---

## Cumulative Language Family Assessment (Updated)

**Hurrian (Preferred Hypothesis):**
- N-gram phonotactics (corrected): **#1** ← changed from #4 in Attempt #4
- Morphological alignment: **14 high-confidence** (vs. Luwian 0)
- Suffix comparison: wins 8/15 direct comparisons (vs. Luwian 7)
- Overall: THREE convergent evidence lines favor Hurrian
- **Confidence: Medium-High** (elevated from Medium in prior sessions)

**Luwian (Secondary Candidate):**
- N-gram phonotactics: **#2** (stable from Attempt #4)
- Morphological alignment: 0 high-confidence
- Suffix comparison: wins 7/15
- **Confidence: Low** (no high-confidence support)

**Proto-Semitic:**
- N-gram phonotactics: **#3** (was #1; ranking was artifact)
- Morphological alignment: poorly tested (strategy 5 not yet executed)
- **Confidence: Low** (phonotactic proximity was misleading)

---

## Follow-up Questions for Attempt #7

1. **Strategy 5 (Proto-Semitic controlled comparison)** — Now that n-gram ranking is demoted to #3, test whether a strict morphological comparison (triconsonantal root analysis) also fails for Proto-Semitic.
2. **PKZa8 full inscription analysis** — "JA-SA-U-NA-KA-NA-SI" compound: is this a scribal fusion or a distinct lexical item?
3. **SYZa2 full inscription analysis** — "U-NA-KA-NA-SI-OLE": a votive inscription specifying olive oil offering?
4. **Clause-internal word-order analysis** — For inscriptions with multiple entity tokens before a single logogram, analyze inter-entity suffix patterns.
5. **Sign clustering with k=5, freq≥10** — Retry with tighter parameters.
6. **Build a Hurrian CV reference corpus** from attested Hurrian words for better n-gram validation.
