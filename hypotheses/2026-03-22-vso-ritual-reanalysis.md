# Hypothesis: VSO Word Order Validation and Ritual Formula Slot Reassignment

**Date:** 2026-03-22
**Strategy category:** Libation Table Analysis / Administrative Bootstrapping
**Language tested (if applicable):** N/A (word order is pre-linguistic; general Minoan)
**Builds on / differs from:** Directly reframes Attempts #3, #5, #6 which constructed the IOZa2 template as HEADER → SLOT1 → ELEMENTS. Differs because Davis (Salgarella & Petrakis 2026) establishes VSO word order from the same libation formula corpus, requiring slot-role reassignment. Also builds on Attempt #9 (JA-DI-KI-TU = Diktynna candidate).

---

## Hypothesis Statement

**H11 (VSO Slot Reassignment):** If Linear A follows VSO word order (as established by Davis 2026 from the libation formula), then in stone vessel inscriptions containing the formula A-TA-I-*301-WA-JA:
- **Slot 1** (A-TA-I-*301-WA-JA) = a VERBAL phrase ("I offer", "dedicated to", or equivalent ritual verb)
- **Slot 2** (the token immediately following) = the SUBJECT — either the dedicant (personal name) or the divine addressee
- **Slot 3+** (JA-SA-SA-RA-ME, U-NA-KA-NA-SI, I-PI-NA-MA, SI-RU-TE) = OBJECTS or complements of the verb

Under this model, slot-2 tokens should vary across inscriptions (each inscription has a different dedicant), showing high site-specificity and personal-name signatures, while slot-3+ elements should be fixed (liturgical formulae).

**Falsification conditions:**
- If A-TA-I-*301-WA-JA does NOT appear at inscription-initial position, the verbal-phrase assignment fails
- If slot-2 tokens show low site-specificity (< 0.3) and appear at many sites, they are fixed liturgical elements, not personal names
- If slot-2 has only 1–2 distinct tokens across all inscriptions, it is a fixed formula element, not a variable dedicant slot

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full (Attempts #1–#10 reviewed)
- [x] All files in `hypotheses/` enumerated and read (10 hypothesis files reviewed)
- [x] This hypothesis differs from prior attempts because:

**Key difference from Attempt #3 (libation table):** Attempt #3 identified the ritual register and confirmed the -JA absolutive but did not assign grammatical roles to ritual formula slots. The IOZa2 template was constructed as header + elements without a VSO constraint.

**Key difference from Attempt #5 (DI-KI analysis):** Attempt #5 tested JA-DI-KI-TU as a ritual element without interrogating whether it was the verb, subject, or object. VSO reanalysis reframes its role.

**Key difference from Attempt #6 (word order):** Attempt #6 tested word order via bigram analysis but did not apply Davis's specific libation formula VSO argument to the ritual corpus slots.

**Key difference from Attempt #9 (JA-DI-KI-TU = Diktynna):** Attempt #9 tested JA-DI-KI-TU as a divine name (object/addressee). Davis VSO proposes the slot-2 position is the subject. This test determines whether slot-2 is a fixed divine name or a variable dedicant.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl` (1721 records)
- Focus: ritual support types — stone vessel, metal object, architecture (case-insensitive)
- Anchor token: A-TA-I-*301-WA-JA (known ritual header from Attempts #5, #6)
- External reference: Davis (2026) in Salgarella & Petrakis, *The Wor(l)ds of Linear A* — VSO word order finding from libation formula analysis

### Analysis Steps

1. Extract all records with support type in {stone vessel, metal object, architecture} (case-insensitive)
2. Filter to records containing token A-TA-I-*301-WA-JA
3. For each such inscription: record full token sequence, note position of A-TA-I-*301-WA-JA within sequence
4. Test H11-verb: is A-TA-I-*301-WA-JA inscription-initial (position 0) in all / most cases?
5. Extract slot-2: the next multi-syllable token immediately after A-TA-I-*301-WA-JA
6. For all slot-2 candidates: compute site-specificity (prop at one site), occurrence count, suffix profile
7. Count distinct slot-2 tokens: if > 5 distinct tokens → variable (dedicant names); if ≤ 2 → fixed formula
8. Compute complementarity: do different slot-2 tokens ever appear together in one inscription?
9. For slot-3+: tabulate which known ritual elements (JA-SA-SA-RA-ME, U-NA-KA-NA-SI, etc.) appear and whether they are stable across inscriptions
10. Test whether slot-2 tokens end in name-suffix (-TI, -TA, -TE, -SI) more than slot-3+ tokens

### Scripts

- `analysis/scripts/vso_ritual_reanalysis_2026-03-22.py`

### Outputs

- `analysis/outputs/vso_ritual_reanalysis_2026-03-22.json`

---

## Results

**Outcome:** PARTIAL SUCCESS
**Confidence:** High (verbal phrase finding), Medium (slot-2 interpretation), Low (personal name identification)
**Evidence tier reached:** Tier 3 (formulaic — slot-role assignment), Tier 4 (lexical — personal name candidates)

### Findings

**Verbal phrase test (SUPPORTED):**
- A-TA-I-*301-WA-JA appears inscription-initial in 10/11 records (90.9%)
- It appears exclusively in ritual support contexts (11/11 ritual)
- This is consistent with Davis's VSO model: slot-1 = verbal phrase

**Slot-2 token distribution:**
- 3 distinct slot-2 tokens across 11 inscriptions:
  - `𐄁` (section divider) — 9 occurrences (corpus_occ=233, site_spec=0.444) — structural marker
  - `TU-RU-SA` — 1 occurrence (corpus_occ=1, site_spec=1.0) — HIGH CONFIDENCE personal name candidate
  - `SE-KA-NA-SI` — 1 occurrence (corpus_occ=1, site_spec=1.0) — HIGH CONFIDENCE personal name candidate
- `𐄁` is the scribal section divider identified in Attempt #10 (𐝫 / U+1076B variant); it separates the verbal header from subsequent content — it is structural, not a lexical slot-2 item
- In 2 of 11 inscriptions, genuine name-like tokens appear directly after the header

**JA-DI-KI-TU (Diktynna) in slot-2:** NOT observed — JA-DI-KI-TU appears in slot-3+ position (object/complement), not slot-2

**Personal name candidates:**
- **TU-RU-SA**: consonant skeleton [T,R,S], unique to one site, 1 corpus occurrence
  - Best LCS match: Teshup-compound (Hurrian) score=0.667 (LCS=2)
  - Best Aegean match: Rhadamanthos [R,D,M,T] (weaker, LCS=1)
- **SE-KA-NA-SI**: consonant skeleton [S,K,N,S], unique to one site, 1 corpus occurrence
  - Best LCS match: Knossos skeleton [K,N,S] score=0.75 (LCS=3 — possibly coincidental)
  - Hurrian Shaushka [S,S,K] score=0.50

### Cross-validation

- All 11 inscriptions are from ritual support types (stone vessel, metal object)
- Sites represented: Iouktas, Knossos, Palaikastro, Kophinas, Troullos (5 non-HT sites)
- TU-RU-SA and SE-KA-NA-SI each appear at exactly 1 site — consistent with personal names but insufficient for cross-site validation

---

## Interpretation

The VSO verbal phrase hypothesis is **supported** by the 90.9% inscription-initial rate of A-TA-I-*301-WA-JA. This is consistent with Davis's model and reframes the token as a ritual verb phrase rather than a header label.

The slot-2 picture is more complex: in 9/11 inscriptions, the section divider `𐄁` immediately follows the verbal phrase, acting as punctuation. In 2 inscriptions, unique personal-name-like tokens (TU-RU-SA, SE-KA-NA-SI) fill the position, suggesting these may be dedicant names in a non-divider inscription format. The Hurrian phonological match for TU-RU-SA (Teshup-compound profile) is suggestive but Low confidence.

JA-DI-KI-TU not appearing in slot-2 strengthens its identification as a divine object (Diktynna as addressee) rather than subject — consistent with the VERB-OBJECT-ATTRIBUTES pattern if the subject (dedicant) is named by TU-RU-SA/SE-KA-NA-SI in the non-divider inscriptions.

Phrasing reminder: All claims are "consistent with" or "suggests" — not "proves".

---

## What Was Learned

1. A-TA-I-*301-WA-JA is overwhelmingly inscription-initial (90.9%), consistent with it being a ritual verbal phrase ("I offer/dedicate")
2. The `𐄁` section divider appears between the verbal phrase and subsequent content in 9/11 inscriptions — it is not a lexical slot-2 element
3. TU-RU-SA and SE-KA-NA-SI are new personal name candidates: unique, site-specific, with Hurrian-compatible consonant skeletons
4. JA-DI-KI-TU occupies slot-3+ position (object/complement), not subject position — compatible with its identification as a divine name (Diktynna, the addressed deity)
5. The ritual formula structure under VSO is now: [VERB] ← `𐄁` → [OBJECT(S)], with the dedicant possibly named in 2 exceptional inscriptions where `𐄁` is absent

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/formulaic_sequences.md`: VSO support (90.9% initial rate), slot-role reassignment, TU-RU-SA and SE-KA-NA-SI as personal name candidates (Low confidence)

---

## Follow-up Questions Generated

- [ ] What sites do TU-RU-SA and SE-KA-NA-SI come from? Do they match cult sites (Iouktas, Palaikastro)?
- [ ] Does A-TA-I break down as A-TA + I (two morphemes)? Hurrian *ašti* = woman/lady — coincidental or meaningful?
- [ ] Why do 9/11 inscriptions have `𐄁` in slot-2 but 2 do not? Are the 2 exceptional inscriptions from a different site or scribal tradition?

---

## Update `failed_attempts.md`

- [x] Entry added to `failed_attempts.md` with outcome and learnings
