# Hypothesis: DI-KI Element Analysis, IOZa2 Coda Identification, and -ME Suffix Function

**Date:** 2026-03-18
**Strategy category:** Libation Table Analysis / Grammatical Analysis / Proper Noun Isolation
**Language tested (if applicable):** Hurrian (morphological comparison), Minoan (internal)
**Builds on / differs from:** `2026-03-18-ngram-luwian-ergative-me.md` (Attempt #4) — that attempt confirmed the IOZa2 liturgical sequence and identified -ME as 3.01x ritual-enriched, but left three specific IOZa2 tokens unanalyzed: `JA-DI-KI-TU` (slot 1), `TA-NA-RA-TE-U-TI-NU` (coda), and the grammatical function of -ME. This attempt specifically targets these three unresolved items through corpus-wide token searches.

---

## Hypothesis Statement

**H1 (JA-DI-KI-TU / DI-KI element):** The token `JA-DI-KI-TU` in IOZa2 shares the DI-KI element with `A-DI-KI-TE` at Palaikastro, suggesting DI-KI is a toponymic/theophoric root potentially corresponding to Mt. Dikte (Δίκτη) or Dikti, the sacred Cretan mountain associated with divine birth (Zeus/Minoan deity). If DI-KI tokens appear on ritual support types at mountain cult sites but not at palace administrative centers, this is consistent with a sacred toponym.

**Falsification condition H1:** If DI-KI tokens appear predominantly on administrative clay tablets at palace centers with no ritual enrichment, the toponym hypothesis fails. If DI-KI appears in quantity-preceding position (like a logogram), it is not a toponym.

**H2 (TA-NA-RA-TE-U-TI-NU coda):** The IOZa2 coda `TA-NA-RA-TE-U-TI-NU` is a variant or extended form of `TA-NA-I-*301-U-TI-NU` documented among A-TA-I-*301-WA-JA variants (Attempt #4). The shared `-U-TI-NU` terminal element may be a formulaic closing morpheme (dedicant marker, scribal convention, or fixed closing phrase).

**Falsification condition H2:** If TA-NA-* tokens appear in inscription-initial rather than inscription-final positions, they are not coda variants. If -U-TI-NU appears in clearly non-formulaic contexts, the closing-formula hypothesis fails.

**H3 (-ME suffix function):** The suffix -ME, which appears as a detachable element on the divine name root JA-SA-SA-RA and has 3.01x ritual enrichment (Attempt #4), functions as a vocative or divine invocation marker — appearing specifically in early syntactic slots of ritual inscriptions when a deity is being addressed directly.

**Falsification condition H3:** If -ME tokens appear uniformly distributed across inscription positions (not concentrated in early/invoking positions), the vocative hypothesis fails. If -ME appears frequently in administrative contexts with quantity associations, it is more likely a grammatical number or class marker.

---

## Prior Attempts Read

- [x] `failed_attempts.md` read in full
- [x] All files in `hypotheses/` enumerated and read
- [x] This hypothesis differs from prior attempts because: Prior attempts (1–4) did not systematically search for the DI-KI element across all 1721 inscriptions; did not analyze the distribution of -U-TI-NU terminal; did not test -ME positional distribution by syntactic slot. This attempt makes three targeted token searches rather than broad strategy sweeps.

---

## Method

### Data Used

- Primary corpus file: `corpus/linear_a_llm_master.jsonl`
- Inscriptions analyzed: all 1721
- External references: Conventional toponymy of Minoan Crete (Dikte/Dikti, Mt. Ida); Hurrian morphology (Speiser 1941, Wilhelm 1989 — see `findings/hurrian_morphology.md`)

### Analysis Steps

**H1 (DI-KI corpus search):**
1. Load full corpus (1721 records)
2. Search all `transliteration_tokens` lists for tokens containing the hyphen-delimited elements "DI" followed by "KI" (i.e., "DI-KI" as a contiguous pair within a longer token, or as a standalone bigram)
3. Record: token form, inscription ID, site, support type, position index within inscription
4. Compute ritual percentage per DI-KI token type (ritual = "Stone vessel" or "Metal object")
5. Compare structural contexts: does JA-DI-KI-TU appear in same slot as A-DI-KI-TE?
6. Test: do DI-KI tokens cluster at mountain cult sites (Iouktas, Kophinas, Palaikastro, Troullos) vs. administrative centers (Haghia Triada, Khania)?

**H2 (TA-NA- / -U-TI-NU search):**
1. Search all tokens for those ending in exactly "U-TI-NU"
2. Search all tokens for those beginning with "TA-NA-"
3. For each match: record position index from inscription start and from inscription end
4. Test: are TA-NA-* tokens concentrated in final positions? (>60% in last 2 inscription slots = supporting evidence)
5. Collect all -U-TI-NU variants and check cross-site distribution

**H3 (-ME positional analysis):**
1. Extract all tokens ending in "-ME" across all 1721 inscriptions
2. For each: record absolute position (0-indexed from start), inscription length, relative position (0.0=start, 1.0=end)
3. Split by support type: ritual (stone vessel, metal object, architecture) vs. administrative
4. Compute mean relative position for ritual -ME tokens vs. non-ME ritual tokens
5. Test: do -ME tokens appear significantly earlier in ritual inscriptions than other ritual tokens?
6. Check co-occurrence: does JA-SA-SA-RA-ME always precede (rather than follow) U-NA-KA-NA-SI?

### Scripts

- `analysis/scripts/dikte_corpus_analysis_2026-03-18.py`
- `analysis/scripts/coda_analysis_2026-03-18.py`
- `analysis/scripts/me_suffix_position_2026-03-18.py`

### Outputs

- `analysis/outputs/dikte_analysis_2026-03-18.json`
- `analysis/outputs/coda_analysis_2026-03-18.json`
- `analysis/outputs/me_suffix_analysis_2026-03-18.json`

---

## Results

**Outcome:** PARTIAL SUCCESS (H1 substantially supported; H2 partially refuted and reframed; H3 inconclusive as stated but new structural finding on -ME ordering)
**Confidence:** Low-Medium (H1), Low (H2 revised), Low (H3)
**Evidence tier reached:** Tier 3–4

### Findings

#### H1 (DI-KI Element) — SUBSTANTIALLY SUPPORTED

Corpus-wide search found **9 DI-KI occurrences** in 8 distinct token types across 4 sites:

| Token | Inscription | Site | Support | Ritual |
|-------|-------------|------|---------|--------|
| JA-DI-KI-TU | IOZa2 | Iouktas | Stone vessel | Yes |
| A-DI-KI-TE | PKZa12 | Palaikastro | Stone vessel | Yes |
| A-DI-KI-TE-TE | PKZa11 | Palaikastro | Stone vessel | Yes |
| JA-DI-KI-TE-TE-DU-PU₂-RE | PKZa15 | Palaikastro | Stone vessel | Yes |
| JA-DI-KI-TE-TE-*307-PU₂-RE | PKZa8 | Palaikastro | Stone vessel | Yes |
| DI-KI | ZA27 | Zakros | Stone vessel | Yes |
| DI-KI-SE | HT117b, HT87 | Haghia Triada | Tablet | No |
| RA-O-DI-KI | PH2 | Phaistos | Tablet | No |

**Overall DI-KI ritual rate: 6/9 = 67% vs. 9% baseline (7.4x ritual enrichment)**

Key structural finding: The DI-KI token occupies the **same structural slot** (slot 1: immediately after ritual header) in BOTH Iouktas (IOZa2) and Palaikastro (PKZa11, PKZa12):

- IOZa2: `A-TA-I-*301-WA-JA` → **`JA-DI-KI-TU`** → `JA-SA-SA-RA-ME` → ...
- PKZa11: `A-TA-I-*301-WA-E` → **`A-DI-KI-TE-TE`** → ... → `SA-SA-RA-ME` → ...
- PKZa12: `A-TA-I-*301-WA-JA` → **`A-DI-KI-TE`** → ... → `RA-ME` → ...

This confirms DI-KI is an **integral part of the liturgical sequence template** — it consistently occupies slot 1 and is followed by a divine name at both sites. The -TU (Iouktas) vs -TE (Palaikastro) suffix distinction may be dialectal or case-based (locative/directive).

Administrative DI-KI contexts: `DI-KI-SE` appears in HT personal name lists (KU-RE-JU, MA-KA-RI-TE, PI-TA-KE-SI), suggesting -SE is a personal name suffix and DI-KI-SE is a personal name (possibly "one from Dikte" or derived from the sacred place name). `RA-O-DI-KI` at PH2 appears before quantity "60" — likely another personal name.

#### H2 (TA-NA-* / -U-TI-NU Coda) — PARTIALLY REFUTED, REFRAMED

Results contradicted the original coda hypothesis:
- TA-NA-I-*301-U-TI-NU appears at **position 0/2** (inscription-initial) in IOZa6 — it is a **header variant**, not a coda
- TA-NA-RA-TE-U-TI-NU appears at **position 6/6** (inscription-final) in IOZa2 — this IS a coda
- TA-NA-TI appears in HT administrative tablets at varied positions — different function entirely

**Revised finding:** The TA-NA- family covers at least two distinct formula types:
1. **TA-NA-I-*301-U-TI-NU** (IOZa6): A header variant of A-TA-I-*301-WA-JA. Both are inscription-initial, both contain *301. The variant uses U-TI-NU terminal instead of WA-JA terminal.
2. **TA-NA-RA-TE-U-TI-NU** (IOZa2): A true coda — appears at inscription end after all liturgical elements. May be a dedicant name or closing formula.

**Key new finding:** The -U-TI-NU terminal is **Iouktas-site-specific** (3 tokens, all Iouktas stone vessels). IOZa11 has bare `U-TI-NU` at position 2/3 (near end). This suggests -U-TI-NU may be a sanctuary-specific marker for the Iouktas peak sanctuary, appearing in both the header variant and coda of Iouktas inscriptions.

#### H3 (-ME Suffix Position) — INCONCLUSIVE AS STATED, NEW STRUCTURAL FINDING

**Positional hypothesis failed:** Ritual -ME tokens show no early-position clustering (mean position 0.471 vs. 0.448 for non-ME ritual tokens — not significantly different).

**New finding: -ME ritual enrichment confirmed at 5.13x** (higher than previous 3.01x estimate, which was affected by support-type case bug). The ritual enrichment is real and substantial.

**Consistent ordering finding:** JA-SA-SA-RA-ME **always precedes** U-NA-KA-NA-SI when both appear in the same inscription (4/4 co-occurrences: IOZa2, IOZa9, PKZa27, TLZa1). This ordering is structurally locked — it is not explained by position alone (both occur in middle of inscription), but by fixed sequence convention.

**The -ME suffix remains a mystery** positionally, but its ritual enrichment (5.13x) and exclusive divine-name attachment (JA-SA-SA-RA-ME, SA-SA-RA-ME, A-SA-SA-*802-ME) remain consistent with it being a ritual-register grammatical morpheme.

**Surprise finding:** PKZa8 contains `JA-SA-U-NA-KA-NA-SI` — a compressed or contracted form of `JA-SA-SA-RA` + `U-NA-KA-NA-SI` run together. This may indicate that in some scribal traditions, the divine name and its companion were written as a compound.

### Cross-validation

**H1 (DI-KI):**
- Iouktas: 1 occurrence (JA-DI-KI-TU, IOZa2) ✓
- Palaikastro: 4 occurrences (A-DI-KI-TE, A-DI-KI-TE-TE, JA-DI-KI-TE-TE variants) ✓
- Zakros: 1 occurrence (DI-KI bare, ZA27) ✓
- **3-site cross-validation achieved for DI-KI ritual use**

**H2 (-U-TI-NU):**
- Iouktas only (3 occurrences) — single-site, cannot cross-validate

**H3 (-ME):**
- JA-SA-SA-RA-ME appears at: Iouktas (4×), Palaikastro (2×), Platanos (1×), Troullos (1×), Psykhro (1×) — 5 sites
- JA-SA-SA-RA-ME → U-NA-KA-NA-SI ordering confirmed across 4 inscriptions at 3 sites ✓

---

## Interpretation

**H1:** The DI-KI element is strongly consistent with a sacred toponym. Its distribution (6/9 occurrences on stone vessels, clustering at mountain cult sites, occupying a fixed "slot 1" position in the liturgical sequence after the header and before the divine name) suggests it functions as a locative or theophoric element in ritual inscriptions — possibly meaning "at/from Dikte" or "of the Dikti goddess." The -TU vs -TE suffix contrast (Iouktas vs Palaikastro) may reflect dialectal variation or a grammatical case distinction (e.g., -TU = dative/directional, -TE = locative/ablative). The personal name uses (DI-KI-SE at HT) suggest DI-KI was also a recognizable toponym in non-ritual administrative contexts (personal names derived from place of origin). This is compatible with a Minoan sacred toponym corresponding to Mt. Dikte/Dikti.

**Confidence: Low-Medium (Tier 4, Lexical)**

**H2:** The TA-NA- formula family is more complex than expected. TA-NA-I-*301-U-TI-NU is a header variant (not coda). -U-TI-NU is Iouktas-specific. The TA-NA-RA-TE-U-TI-NU coda in IOZa2 may record the name or title of the dedicant. The *301 sign appearing in both header families (A-TA-I-*301-WA-JA and TA-NA-I-*301-U-TI-NU) confirms its header-formula membership but its specific phonetic/logographic value remains unknown.

**H3:** The -ME positional hypothesis is inconclusive. -ME's function remains uncertain but its 5.13x ritual enrichment and exclusive divine-root attachment point to a ritual-register suffix (possibly divine case, reverential form, or dedicatory marker). The finding that it is NOT positionally early-biased rules out a simple "vocative at start of sentence" analysis.

---

## What Was Learned

1. **DI-KI is an integral slot-1 element of the liturgical sequence**, confirmed at 2 sites in the same structural position. It is not an incidental token in IOZa2.
2. **The liturgical sequence template is now 7 elements** (updated from 4): [HEADER] → [DI-KI epithet] → [JA-SA-SA-RA-ME] → [U-NA-KA-NA-SI] → [I-PI-NA-MA] → [SI-RU-TE] → [CODA]
3. **TA-NA-I-*301-U-TI-NU is a header variant**, not a coda variant — it appears inscription-initial in IOZa6.
4. **-U-TI-NU is Iouktas-site-specific** — 3 occurrences, all Iouktas stone vessels; possibly a sanctuary identifier.
5. **-ME positional hypothesis failed** — -ME is not early-biased, ruling out a strict vocative analysis.
6. **JA-SA-SA-RA-ME → U-NA-KA-NA-SI ordering is structurally locked** — 4/4 co-occurrences show this fixed sequence.
7. Even in failure, H3 ruled out a specific interpretation, narrowing the search space for -ME's grammatical function.

---

## Findings Promoted to `findings/`

- [x] Appended to `findings/formulaic_sequences.md`: DI-KI element slot-1 structural role, expanded liturgical sequence template (7 elements), -U-TI-NU Iouktas specificity, TA-NA-I-*301-U-TI-NU as header variant

---

## Follow-up Questions Generated

- [ ] **What does the -TU vs -TE suffix contrast on DI-KI mean?** (JA-DI-KI-TU at Iouktas vs A-DI-KI-TE at Palaikastro) — if this is a case distinction, it may provide evidence for the Minoan case system
- [ ] **What is *307 in JA-DI-KI-TE-TE-*307-PU₂-RE?** Unknown sign; only appears in this Palaikastro token
- [ ] **What is U-NA-KA-NA-SI?** Consistently follows JA-SA-SA-RA-ME — divine epithet? companion deity? ritual action?
- [ ] **Does DI-KI appear in Linear B Knossos tablets?** If Knossos scribes mentioned a Minoan sanctuary, its name may appear in Linear B records as a logogram or toponym
- [ ] **Is -U-TI-NU a sanctuary identifier for Iouktas?** If yes, it may appear in Linear B records mentioning goods sent to or from Iouktas

---

## Update `failed_attempts.md`

- [x] Entry added (see below)
