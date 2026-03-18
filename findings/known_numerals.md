# Confirmed Numeral System

This file documents the Linear A numeral system, which is well-understood from repeated corpus patterns and Linear B parallels.

---

## Overview

Linear A uses a **decimal positional system** inherited from or parallel to the broader Aegean administrative tradition. The numeral system is the most securely understood component of Linear A, independent of any language identification.

| Symbol type | Value | Basis for identification |
|-------------|-------|--------------------------|
| Vertical stroke (𐝀) | 1 | Positional analysis + Linear B parallel |
| Horizontal bar or dash (𐝁) | 10 | Positional analysis + Linear B parallel |
| Circle or large round sign | 100 | Positional analysis + Linear B parallel |
| Large complex sign | 1000 | Positional analysis + Linear B parallel |
| Fraction sign variant 1 | 1/2 | Positional analysis in fractional commodity contexts |
| Fraction sign variant 2 | 1/3 | Positional analysis |
| Fraction sign variant 3 | 1/4 | Positional analysis |
| Fraction sign variant 4 | 1/5 | Positional analysis |

---

## How Numbers Are Written

Numbers in Linear A are written additively from largest to smallest unit, left to right:

```
Example: 234 = [100][100][10][10][10][1][1][1][1]
         (two hundreds, three tens, four ones)
```

This is the same convention used in Linear B and Egyptian hieratic numerals.

---

## Fractions

Fractional signs appear in commodity tallies where quantities are not whole numbers (e.g., partial jars of oil, fractional grain measures). They appear after the whole number component:

```
Example: 2½ = [10][1][1][½]
```

The exact commodity measure units (e.g., what volume of liquid constitutes "1") are not yet established for Linear A, though they are assumed to be similar to Linear B dry and liquid measure units.

---

## Use in Corpus

In the `linear_a_llm_master.jsonl` corpus, numerals are typically represented in the `stats` field and as inline tokens in `transliteration_tokens`. The convention is to use Arabic numerals in the transliteration when signs are unambiguous numerals:

```json
"transliteration_tokens": ["JA-KI-SI-KI-TE", "GRA", "10", "2", "VIN", "5"]
```

---

## Confidence Level

**High** — The numeral system is the best-understood aspect of Linear A. The positional decimal structure is confirmed beyond reasonable doubt by:
1. Internal consistency across thousands of corpus occurrences
2. Exact parallel to Linear B numeral conventions
3. Archaeological context confirming accounting purpose
4. Agreement across all 52 sites in the corpus

---

## Open Questions

- [ ] What are the standard unit measures (volume, weight, area) implied by "1" for each commodity type?
- [ ] Are there any numeral signs in Linear A that have no Linear B equivalent? (Could indicate a different counting tradition)
- [ ] Do fractional signs differ by commodity type, or is the same set of fraction signs used universally?
- [ ] Are numbers ever used in non-accounting contexts (e.g., on libation tables), and if so, what do they represent?
