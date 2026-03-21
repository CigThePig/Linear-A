# Linear A Decipherment Research Project

## Project Purpose

This project is a systematic research effort to apply computational and linguistic methods to the decipherment of Linear A, the undeciphered writing system of Minoan Crete (~1800–1450 BCE).

**The goal is not to fabricate a translation.** The goal is to accumulate incremental, defensible evidence pointing toward the language family, grammar type, and lexical content of Linear A.

Every hypothesis must be testable against the 1721-inscription corpus in `corpus/linear_a_llm_master.jsonl`.

**A successful outcome is defined as:**
- Identifying the language family with high confidence
- Reading 20+ lexical items with cross-inscription consistency
- Constructing a partial grammar sketch

---

## WARNING: Read Before Doing Anything Else

Before proposing any new decipherment approach, you MUST:

1. **Read `failed_attempts.md` in full.**
2. **Read `code_issues.md` in full.**
3. **Enumerate all hypothesis files** with `ls hypotheses/` and read each one.
4. **State explicitly** which prior hypothesis your new attempt differs from and how.

Before writing or patching any analysis script, you MUST additionally:

5. **Re-read `code_issues.md`** to check whether the pattern you are implementing resembles a previously logged bug.

Never repeat a strategy that has already been documented as failed or inconclusive unless you have a documented reason to believe a substantially different angle will yield different results.

Never assert that Linear A has been deciphered. All claims must be phrased as hypotheses with explicit confidence levels.

### The Two Mandatory Error Logs Are Distinct — Do Not Confuse Them

| File | Purpose |
|------|---------|
| `failed_attempts.md` | Records **research and hypothesis failures**: inconclusive analyses, rejected decipherment strategies, methodological dead ends in the linguistics or decipherment work. A research failure is expected and useful — it is how hypotheses are tested. |
| `code_issues.md` | Records **implementation errors**: script bugs, incorrect metric definitions, wrong sample spaces, silent calculation errors, data-handling mistakes, output-generation mistakes, and other engineering defects that could distort or disable analytical measurements. |

**Coding problems must NOT be buried or silently corrected.** If you discover a bug while working — even a minor one — you must:
1. Fix the script.
2. Regenerate any affected outputs.
3. Update any findings or hypothesis files that cited numbers derived from the buggy code.
4. Log the issue in `code_issues.md` using the entry schema in that file.

Do not treat a code fix as a research event logged in `failed_attempts.md`. Do not treat a research failure as a bug logged in `code_issues.md`. They are separate audit trails.

---

## Established Facts (Do Not Re-Derive)

### The Sign System

- Linear A shares roughly 60–80% of its sign inventory with Linear B (Mycenaean Greek), deciphered by Michael Ventris in 1952.
- Standard practice transfers Linear B phonetic values to visually similar Linear A signs — these are "conventional transliterations" and appear in the `transliteration_tokens` field of the corpus.
- **These conventional values are hypotheses, not proven readings.** They are borrowed phonetic labels, not demonstrated readings of the Minoan language.

### The Corpus

- 1721 inscriptions from 52 sites across the Aegean (~1800–1450 BCE)
- Haghia Triada: 1110 records (64%) — do not over-index on this site
- Other major sites: Khania (226), Phaistos (66), Knossos (59), Zakros (53)
- Support types: nodules (886), tablets (393), roundels (151), stone vessels (107), clay vessels (74), metal objects (23), and others
- Most inscriptions are administrative: inventories, accounting, commodity tallies

### Confirmed Vocabulary

See `findings/` for full documentation. Summary:

| Sequence | Meaning | Confidence | Basis |
|----------|---------|------------|-------|
| KU-RO | "total" | High | Positional analysis — appears at end of accounting sequences, 39 bigram occurrences |
| KI-RO | "owed / deficit" | High | Positional analysis — appears in deficit contexts, ~17 occurrences |
| GRA | grain (logogram) | High | Linear B parallel + archaeological context |
| VIN | wine (logogram) | High | Linear B parallel + archaeological context |
| OLE | olive oil (logogram) | High | Linear B parallel + archaeological context |
| OLIV | olives (logogram) | High | Linear B parallel |
| VIR | person / man (logogram) | High | Linear B parallel |
| CYP | cyperus plant (logogram) | Medium | Linear B parallel |

### Numeral System

Decimal positional system: symbols for 1, 10, 100, 1000, and fractions (1/2, 1/3, 1/4, 1/5). Well understood from repeated corpus patterns. See `findings/known_numerals.md`.

### Most Frequent Word-Final Suffixes

The six most common word-final syllables (likely grammatical suffixes): **-RO** (78), **-JA** (65), **-RE** (58), **-TE** (56), **-NA** (54), **-TI** (49)

### Top 25 Core Syllabic Signs

A, I, JA, TA, SI, SA, NA, KA, KU, DA, RE, KI, RA, MA, DI, TE, PA, TI, RO, MI, RU, DU, RI, U, TU — each appears in 54–130 distinct inscriptions.

---

## Decipherment Methodology

### Process for Each New Attempt

Every new attempt must follow this procedure:

1. Read `failed_attempts.md` and all files in `hypotheses/`
2. State explicitly which prior hypothesis this new attempt differs from and how
3. Create a new file `hypotheses/YYYY-MM-DD-hypothesis-name.md` using the template in `hypotheses/TEMPLATE.md`
4. Run analysis against `corpus/linear_a_llm_master.jsonl`. Scripts go in `analysis/scripts/`. Outputs go in `analysis/outputs/`
5. Record results — **including negative results** — back into the hypothesis file and into `failed_attempts.md`
6. If the hypothesis yields confirmed findings, move only the confirmed portion to the appropriate file in `findings/`

### Tiers of Evidence

All claims must cite their tier. Never jump to Tier 6 without completing lower tiers.

| Tier | Name | Description |
|------|------|-------------|
| 1 | Structural | Mathematical/distributional patterns requiring no language assumption (sign frequency, positional statistics, co-occurrence graphs) |
| 2 | Logographic | Commodity logograms identified through Linear B parallels and archaeological context |
| 3 | Formulaic | Recurring sequences (KU-RO, KI-RO) identified through positional analysis |
| 4 | Lexical | Specific sign sequences hypothesized to be words, supported by cross-language comparison |
| 5 | Grammatical | Inflectional patterns inferred from suffix/prefix distribution |
| 6 | Translational | Full or partial rendering of inscriptions — only reached after Tiers 1–5 are solid |

### Core Analytical Workflows

1. **Frequency and distribution analysis** — Compute sign/bigram/trigram frequency tables. Compare distributions across sites to separate scribal convention from language patterns.

2. **Positional analysis** — Identify word-initial, word-medial, and word-final sign distributions. Grammatical markers in agglutinative languages cluster at specific positions.

3. **Formulaic pattern mining** — Use `corpus/linear_a_rag_chunks.jsonl` to find exact and fuzzy repeating sequences across all sites. Cross-site repetition is strong evidence for functional words.

4. **Linear B comparison** — For each syllabic sign, retrieve the Linear B phonetic value and test whether applying it to Linear A sequences produces recognizable roots in candidate languages.

5. **Language family testing** — Apply candidate vocabulary from Proto-Semitic, Luwian/Anatolian, Hurrian, Proto-Indo-European, and isolate hypotheses. Document each test completely regardless of outcome.

6. **Administrative document analysis** — Use the known numeric structure to anchor meaning. A sign appearing before numbers in the same position as GRA appears before grain quantities is likely another commodity logogram.

7. **Cross-site comparison** — Signs or formulas appearing at every site are likely functional words or universal administrative terms. Signs unique to one site may be proper nouns or local commodity names.

8. **Scribe identification analysis** — The corpus includes `scribe` field data. Signs or spellings unique to one scribe may reflect personal conventions. Shared patterns across scribes are more linguistically significant.

---

## Decipherment Strategies

Ordered from most to least immediately promising, based on available corpus data and prior scholarship.

### Strategy 1 — Administrative Formula Bootstrapping (Start Here)

**Rationale:** The equivalent of Ventris's method for Linear B. The corpus is dominated by administrative tallies with the structure `[entity] [logogram] [number]`. KU-RO ("total") and KI-RO ("owed/deficit") are confirmed anchors.

**Actions:**
- Map all positions where KU-RO and KI-RO appear across all 1721 tablets
- Identify every other token appearing in the same structural slot (closing formula position)
- Those tokens are likely synonyms or related administrative terms (received, dispatched, assessed)
- Validate findings from Haghia Triada against the 611 non-HT records

---

### Strategy 2 — Suffix Paradigm Reconstruction

**Rationale:** Word-final distributions (-RO 78, -JA 65, -RE 58, -TE 56, -NA 54, -TI 49) are far from random and strongly suggest grammatical suffixes. Agglutinative languages cluster case/number markers at word boundaries.

**Actions:**
- For every multi-sign token, extract the final syllable
- Group all words by final syllable; check whether words with the same suffix cluster around the same commodity, person-type, or site
- If -RO words consistently appear in deficit/owed contexts (KI-RO is one), -RO may be a case or grammatical marker
- Compare the paradigm to Hurrian, Luwian, and Proto-Semitic morphology

---

### Strategy 3 — Proper Noun Isolation via Site-Specificity

**Rationale:** Tokens appearing almost exclusively in one site's records are strong proper noun candidates (place names, personal names). These can sometimes be cross-referenced with later Greek place names or Linear B records.

**Actions:**
- Compute a site-specificity score for each sign sequence (proportion at one site vs. total occurrences)
- High-specificity tokens at each site are candidates for local personal names or place names
- Cross-reference with Minoan place names preserved in Greek: Amnisos, Tylissos, Knossos, Phaistos, Zakros
- Cross-reference with Linear B tablets from Knossos that mention Minoan (non-Greek) names

---

### Strategy 4 — Luwian/Anatolian Lexical Comparison

**Rationale:** Luwian is an Anatolian Indo-European language with well-documented syllabic writing. The Minoans had Anatolian trading contacts. Several Linear A sequences are phonologically plausible Luwian cognates (Woudhuizen, Yakubovich debate).

**Actions:**
- Apply Linear B phonetic values to the 50 most frequent sign sequences
- Compare against Melchert's Luvian glossary (standard reference)
- Focus on administrative/commodity vocabulary where Luwian equivalents are known
- First test case: "I-DA-MA-TE" on the Arkhalkhori axe — compare to Luwian *tati-* and "Dictaean" (Mt. Ida/Dikte)

---

### Strategy 5 — Proto-Semitic Comparison (Constrained Revival)

**Rationale:** Cyrus Gordon's Semitic hypothesis was rejected partly for methodological reasons. A constrained re-test with strict phonological correspondence rules (not cherry-picking) is warranted given the richer corpus now available.

**Actions:**
- Identify Linear A sequences that, with Linear B phonetic values applied, produce plausible Proto-Semitic triconsonantal roots
- Constraint: at least 3 independent occurrences in the corpus; proposed meaning must match archaeological/administrative context
- Priority test cases: "NA-SI", "I-PI-NA-MA", and especially "JA-SA-SA-RA-ME" (recurring on libation tables — likely a divine name or ritual formula)

---

### Strategy 6 — Libation Table Formula Analysis (Religious Register)

**Rationale:** A significant body of inscriptions appears on stone libation tables (ritual contexts). These repeat a small set of formulas, offering access to a non-administrative register that can cross-validate administrative findings.

**Actions:**
- Filter corpus to support types: stone vessel, metal object, architecture
- Find all inscriptions sharing structural similarity across different sites
- Use "JA-SA-SA-RA-ME" as the anchor — it appears across multiple libation tables at different sites (cross-dialectal, likely a liturgical term)
- If site A has `X JA-SA-SA-RA-ME Y` and site B has `X' JA-SA-SA-RA-ME Y'`, then X/X' and Y/Y' are structurally equivalent — a bilingual-like context within one script

---

### Strategy 7 — Computational Sign Clustering

**Rationale:** Some Linear A signs have no Linear B parallel (marked with `*` prefix: *301, *131B, *22F, *318, etc.). Distributional clustering can assign these unknown signs to phonological neighborhoods of known signs.

**Actions:**
- Build a sign co-occurrence matrix from the full corpus
- Apply PCA or UMAP to place signs in a distributional space
- Unknown `*` signs will cluster near known signs with similar behavior, providing phonetic value hypotheses
- Signs that cluster together likely belong to the same phonological class (e.g., all CV syllables where C is a stop vs. sonorant)

---

### Strategy 8 — Hurrian Language Testing

**Rationale:** Hurrian is a 2nd-millennium BCE language isolate with well-attested agglutinative ergative-absolutive grammar. The Minoan language appears to be agglutinative (Brent Davis 2014) — Hurrian morphology may be a better structural match than Semitic or Indo-European.

**Actions:**
- Apply Hurrian morpheme inventory to Linear A suffix paradigm
- Hurrian case suffixes: -ne (nominative plural), -ve (genitive), -ra (locative), -da (dative/directive) — cross-check against Linear A's -NA, -RA, -TE, -DA
- Hurrian divine names (Teššub, Šauška, Ḫebat) documented in Mitanni-period texts — check for phonological matches in ritual contexts

---

### Strategy 9 — N-gram Language Model Fingerprinting

**Rationale:** Every natural language has characteristic phonotactic patterns producing distinctive bigram/trigram frequency distributions. The Linear A "fingerprint" can be compared against candidate language fingerprints even without knowing the language.

**Actions:**
- Build a bigram transition probability matrix for Linear A sign sequences (using conventional transliteration values as proxies)
- Build equivalent matrices from known texts in Luwian, Hurrian, Proto-Semitic, and Etruscan
- Compute KL-divergence or cosine similarity between Linear A matrix and each candidate language
- The closest match is not proof, but it gives a ranked list of which language family's phonology best fits observed sign distribution

---

### Strategy 10 — Bilingual Object Analysis (Standing Watch Item)

**Rationale:** A small number of objects in the corpus use `≈` separator in transliterations, possibly indicating dual-script objects. Any true bilingual inscription would be transformative.

**Actions:**
- Filter corpus for all records containing `≈` in transliteration tokens
- Cross-reference with `support` field — these may be objects that circulated between cultures
- Research archaeological literature for objects found alongside multilingual labels
- Document as an open research thread; do not actively invest time unless a confirmed bilingual object is identified

---

## Data Files Guide

All source files are in `corpus/` — treat as read-only.

| File | Format | Best Used For |
|------|--------|---------------|
| `linear_a_llm_master.jsonl` | JSONL | Corpus-wide statistical analysis (1721 records, sign-by-sign data) |
| `linear_a_llm_flat.csv` | CSV | Column operations, pandas loading without custom parsing |
| `linear_a_rag_chunks.jsonl` | JSONL | Pattern-matching across grouped inscriptions |
| `linear_a_instruction_pairs.jsonl` | JSONL | Fine-tuning or structured prompting experiments |
| `linear_a_llm_reading_edition.md` | Markdown | Quickly reading inscriptions without writing code |
| `manifest.json` | JSON | Package metadata, site/support distribution |

### Minimal Python Loading Snippet

```python
import json

# Load full corpus
records = []
with open("corpus/linear_a_llm_master.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

# Access a record
r = records[0]
print(r["id"], r["site"], r["transliteration_tokens"])
```

Key fields in each record: `id`, `canonical_name`, `site`, `context`, `support`, `scribe`, `linear_a_text`, `transliteration_tokens`, `translation_or_gloss_tokens`, `stats`, `source_dataset`

---

## Output Conventions

| Artifact | Location | Naming Pattern |
|----------|----------|----------------|
| Python analysis scripts | `analysis/scripts/` | `script_name_YYYY-MM-DD.py` |
| Generated outputs | `analysis/outputs/` | `output_name_YYYY-MM-DD.{csv,json,md}` |
| New hypotheses | `hypotheses/` | `YYYY-MM-DD-hypothesis-name.md` |
| Confirmed findings | `findings/` | Append to appropriate existing file |
| Failed/inconclusive attempts | `failed_attempts.md` | Prepend new entries (newest at top) |

Always update `failed_attempts.md` at the end of each session, even for inconclusive results.

---

## Epistemic Guardrails

**Do not:**
- Claim decipherment. Use: "consistent with", "suggests", "provides evidence for", "is compatible with"
- Invent glosses not grounded in corpus data or comparative linguistics
- Treat Linear B phonetic values as proven Linear A phonetic values — they are hypotheses
- Over-index on Haghia Triada data (64% of records) — always cross-check findings against non-HT sites
- Discard a negative result without recording it in `failed_attempts.md`
- Start a new attempt without reading all previous attempts and hypothesis files

**Do:**
- Document everything, including failures
- State confidence levels (Low / Medium / High) on every claim
- Cite the tier of evidence for every claim (Tier 1–6, see above)
- Cross-validate any finding from HT against at least 2 other sites before elevating confidence
- Generate follow-up questions even when a hypothesis fails — negative results have direction

---

## Repository Structure

```
Linear-A/
├── CLAUDE.md                          # This file — project instructions
├── failed_attempts.md                 # MANDATORY READ — research/hypothesis failures
├── code_issues.md                     # MANDATORY READ — implementation bugs and code defects
├── corpus/                            # Source data (read-only)
│   ├── README.md
│   ├── manifest.json
│   ├── linear_a_llm_master.jsonl
│   ├── linear_a_llm_flat.csv
│   ├── linear_a_instruction_pairs.jsonl
│   ├── linear_a_rag_chunks.jsonl
│   └── linear_a_llm_reading_edition.md
├── analysis/
│   ├── scripts/                       # Python/analysis scripts
│   └── outputs/                       # Generated CSVs, reports
├── hypotheses/
│   └── TEMPLATE.md                    # Blank template for each new hypothesis
├── findings/
│   ├── known_logograms.md             # Confirmed commodity logograms
│   ├── known_numerals.md              # Confirmed numeral system
│   └── formulaic_sequences.md        # Confirmed KU-RO, KI-RO, suffix data
└── references/
    └── prior_scholarship.md           # Summary of published decipherment attempts
```
