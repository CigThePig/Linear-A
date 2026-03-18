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
