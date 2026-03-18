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
