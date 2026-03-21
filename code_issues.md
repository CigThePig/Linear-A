# Code Issues and Implementation Pitfalls

## Purpose

This file is the permanent record of **implementation errors, script bugs, analytical logic flaws, bad assumptions in code, data-handling mistakes, metric-definition mistakes, and output-generation mistakes** that have been found and corrected in this project.

**This file is NOT the same as `failed_attempts.md`.**

| File | Records |
|------|---------|
| `failed_attempts.md` | Research and hypothesis failures: inconclusive analyses, rejected decipherment strategies, methodological dead ends in the linguistics or decipherment work |
| `code_issues.md` | Engineering failures: bugs, incorrect metric definitions, wrong sample spaces, silent calculation errors, and other implementation problems that could silently corrupt analytical outputs |

A research failure is expected and useful — it is how hypotheses are tested. A code issue is a defect that must be fixed because it distorts or disables the measurement machinery the research depends on.

---

## Mandatory Process Requirements

**Before writing any new analysis script or patching an existing one:**

1. Read this file in full.
2. Check whether the pattern you are about to implement resembles any previously logged issue.
3. If you find a new bug while working, log it here **immediately upon discovery** — do not silently correct it without logging.

**When a code issue is discovered:**

- Create an entry in this file following the schema below.
- Patch the affected script(s).
- Regenerate any affected outputs.
- Update any findings or hypothesis files that cited numbers derived from the buggy code.
- Do not delete or overwrite old output files without replacing them with the corrected version.

---

## Entry Schema / Template

Copy this block for each new entry:

```
### CI-NNN — Short Description

| Field | Value |
|-------|-------|
| Date discovered | YYYY-MM-DD |
| Date fixed | YYYY-MM-DD |
| File(s) affected | script name(s) |
| Issue type | [metric definition / sample space / logic error / data handling / silent failure / dead code / other] |
| Outputs regenerated | yes / no / N/A |

#### Description
One clear paragraph describing the bug. What the code did. What it should have done. Why the error was non-obvious.

#### Analytical Impact
What metric or result was corrupted. Direction of distortion (inflated / deflated / silently zeroed). Whether any conclusions rested on the bad value.

#### Fix Applied
Exactly what was changed. Reference the relevant function or line numbers if helpful.

#### Conclusion Status
- **Unchanged:** conclusion still holds
- **Softened:** conclusion is weaker but still directionally correct
- **Strengthened:** conclusion is stronger after correction
- **Overturned:** conclusion was wrong
- **Newly decidable:** result that was previously unavailable is now computable

#### Prevention Note
What pattern or check would catch this class of bug in the future.
```

---

## Issue Log (newest first)

---

### CI-004

**Date:** 2026-03-21
**Severity:** Medium
**Scripts affected:** `da_disambiguation_2026-03-21.py`, `ni_commodity_context_2026-03-21.py`
**Outputs affected:** `da_disambiguation_2026-03-21.json`, `ni_commodity_context_2026-03-21.json`

#### Description

Both scripts defined `RITUAL_SUPPORTS = {"stone vessel", "metal object", "stone object", "architecture"}` (all lowercase). The corpus `support` field uses Title Case values: `"Stone vessel"`, `"Metal object"`, `"Stone object"`, `"Architecture"`. The mismatch caused `baseline_ritual_rate = 0.0` and `ritual_enrichment = None` or `ZeroDivisionError`. The ni_commodity_context script computed ritual_rate=0 for NI records (should be 0.045) and baseline=0 (should be 0.090), causing ritual_enrichment to compute as infinity or divide-by-zero instead of 0.5.

#### Analytical Impact

`da_disambiguation_2026-03-21.py`: Class B and Class A ritual enrichment was initially computed as `null`/`INCONCLUSIVE`. After fix: Class B = 6.06x, Class A = 3.7x. This STRENGTHENS the conclusion that -DA is ritual-enriched (the bug had hidden the enrichment).

`ni_commodity_context_2026-03-21.py`: Ritual enrichment was initially `None`; after fix: 0.5x (below baseline). This CHANGES the commodity classification note from "insufficient data" to "NI is administrative, not ritual" — strengthening the fig/agricultural commodity hypothesis.

#### Fix Applied

Changed `RITUAL_SUPPORTS` values to Title Case in both scripts:
- `da_disambiguation_2026-03-21.py`: line ~30
- `ni_commodity_context_2026-03-21.py`: line ~25

Both scripts re-run after fix; outputs regenerated.

#### Conclusion Status

- `da_disambiguation` H10c: **Strengthened** — ritual enrichment evidence is now correctly computed; the Hurrian dative rejection is stronger after fix
- `ni_commodity_context` H10b: **Strengthened** — NI's administrative (non-ritual) character is now correctly confirmed; fig hypothesis score unchanged but ritual evidence is now valid

#### Prevention Note

Before using any support-type filter in a new script, always check the corpus support field values against the actual values in `corpus/linear_a_llm_master.jsonl`. Run `Counter(r.get('support','') for r in records).most_common()` at the top of the script as a diagnostic step. The corpus uses Title Case (e.g., "Stone vessel", not "stone vessel").

---

---

### CI-003 — Mixed Sample-Space PMI in *304 Logogram Analysis

| Field | Value |
|-------|-------|
| Date discovered | 2026-03-21 |
| Date fixed | 2026-03-21 |
| File(s) affected | `analysis/scripts/sign304_logogram_2026-03-20.py` |
| Issue type | metric definition / sample space |
| Outputs regenerated | yes — `analysis/outputs/sign304_logogram_2026-03-20.json` |

#### Description

The `compute_pmi()` function was called with an inconsistent mixture of sample spaces:

- `count_304`: set to `total_occ` — total token **occurrences** of `*304` (= 25), not the number of records containing `*304` (= 22)
- `count_lgm`: computed as `sum(tokens.count(lgm) for ...)` — total token **occurrences** of each logogram across all records
- `count_both`: number of **records** containing both `*304` and the logogram (record-level)
- denominator: `len(records)` = 1721 (record-level)

The resulting probabilities therefore used occurrence-level numerators with a record-level denominator, which is not a valid probability formulation. When logograms appear multiple times per record (especially high-frequency signs like GRA), `count_lgm` inflates relative to what a record-level count would give, which in turn deflates PMI for those logograms.

Additionally, `total_tokens` was computed but never used — a dead variable left over from an earlier draft of the function.

#### Analytical Impact

All five PMI values shifted upward after correction to fully record-level formulation:

| Logogram | Buggy PMI | Corrected PMI | Change |
|----------|-----------|---------------|--------|
| OLE | 3.968 | 4.219 | +0.251 |
| OLIV | 4.328 | 5.009 | +0.681 |
| GRA | 3.958 | 4.512 | +0.554 |
| VIN | 1.377 | 1.798 | +0.421 |
| VIR | 0.000 | 0.000 | 0.000 (correct: genuine zero, no co-occurrence) |

GRA and OLIV showed the largest shifts because they tend to appear multiple times per record, inflating `count_lgm` most under the buggy version. The OLIV–OLE rank ordering (OLIV > OLE) was already correct under the buggy version and remains correct after correction.

The `*304` hypothesis was supported by a ≥70% numeral-after rate and presence at ≥5 sites — neither of which depended on PMI values — so the hypothesis verdict did not change. The PMI values were cited as supporting evidence, not as the primary threshold metric.

#### Fix Applied

Replaced the mixed-space block with a consistent record-level computation:

```python
count_304_records = len(target_records)  # records containing *304
count_lgm_records = sum(1 for r in records if lgm in get_tokens(r))  # records containing lgm
count_both = sum(1 for r in records if target in get_tokens(r) and lgm in get_tokens(r))
pmi = compute_pmi(count_both, count_304_records, count_lgm_records, len(records))
```

Also added `"pmi_sample_space": "record_level"` to the output JSON, and removed the unused `total_tokens` variable. Updated cited PMI values in `findings/known_logograms.md` and `failed_attempts.md`.

#### Conclusion Status

**Unchanged:** *304 logogram hypothesis (H8a) remains SUPPORTED. PMI values are now higher and more trustworthy, which marginally strengthens the evidence for the olive-commodity association, but the primary thresholds (numeral-after rate, site count) were already met and are unaffected.

#### Prevention Note

When computing PMI or any co-occurrence statistic, explicitly define the sample space at the top of the computation block as a code comment. All three counts (`count_a`, `count_b`, `count_ab`) and the denominator must use the same unit (records or tokens). Use descriptive variable names that include the unit: `count_304_records`, `count_lgm_records`, `count_both_records`. Never mix token-level and record-level counts in the same PMI call.

---

### CI-002 — Missing -SA from Hurrian Ergative Prediction Sweep

| Field | Value |
|-------|-------|
| Date discovered | 2026-03-21 |
| Date fixed | 2026-03-21 |
| File(s) affected | `analysis/scripts/ergative_search_2026-03-20.py` |
| Issue type | logic error / silent failure |
| Outputs regenerated | yes — `analysis/outputs/ergative_candidate_2026-03-20.json` |

#### Description

The script docstring (line 12) explicitly stated: *"Hurrian prediction: Hurrian ergative is -š, which may appear as -SI or **-SA** in Linear A's consonant inventory."* The `hurrian_prediction_check` output block referenced `profiles.get("SA")` and was prepared to print SA's inverse-JA score. However, `"SA"` was never included in `suffixes_to_test`. As a result, `profiles["SA"]` was always `None`, the SA-branch of the Hurrian prediction was never computed, and the script could only partially evaluate its own stated hypothesis.

A superficial run of the script would not reveal this problem: the Hurrian prediction check printed nothing for SA, silently treating the half-tested prediction as a full test.

Note: the bare token `"SA"` is in `KNOWN_LOGOGRAMS` and would be filtered out by `is_syllabic()`. The suffix sweep operates on the *final syllable* of multi-syllable tokens (e.g., `"TA-SA"`, `"KA-SA"`), which are not affected by the logogram classification of bare `"SA"`. Adding `"SA"` to `suffixes_to_test` is therefore safe and correct.

#### Analytical Impact

The Hurrian ergative prediction was previously reported as: *"-SI ranks 17th (not -RU)"* — implicitly treating only -SI as the Hurrian candidate despite the docstring naming both. With SA now profiled, the result is: -SI ranks 18th (inv-JA score 1.068) and -SA scores 0.990 — both well below the ≥3.0 threshold and below the -JA absolutive baseline. The Hurrian ergative prediction is now **definitively rejected** on corpus grounds for both stated candidates, not just one.

#### Fix Applied

Added `"SA"` after `"SI"` in `suffixes_to_test`:

```python
"TE", "NA", "RE", "RO", "TI", "MI", "NE", "SI", "SA", "WA", ...
```

Added clarifying comments at the `suffixes_to_test` definition and at the `hurrian_candidates` check explaining that both are now profiled.

#### Conclusion Status

**Strengthened (in a negative direction):** The Hurrian ergative prediction is more definitively rejected. The overall H8c verdict (-RU as ergative candidate) is unchanged — SUPPORTED. The Hurrian morphological challenge is now clearer: neither -SI nor -SA shows ergative-like distribution. The implication that -RU does not map cleanly to Hurrian -š is now more firmly established.

#### Prevention Note

Whenever a docstring or comment names multiple items to be tested, immediately verify that all named items appear in the corresponding data structure (list, set, dict). Code review should check that stated hypotheses and their named predictions have matching test coverage in the code. If a prediction block references `profiles.get("SA")`, SA must be in the collection being profiled.

---

### CI-001 — VIR Family Co-occurrence Missed in Ergative Suffix Profiling

| Field | Value |
|-------|-------|
| Date discovered | 2026-03-21 |
| Date fixed | 2026-03-21 |
| File(s) affected | `analysis/scripts/ergative_search_2026-03-20.py` |
| Issue type | logic error / silent failure |
| Outputs regenerated | yes — `analysis/outputs/ergative_candidate_2026-03-20.json` |

#### Description

In `compute_suffix_profile()`, the VIR person-logogram co-occurrence was checked with:

```python
if "VIR" in tokens:
    vir_cooc += 1
```

`"VIR" in tokens` is a Python list membership test: it checks for the exact string `"VIR"` in the token list. The corpus represents VIR compounds (gendered or qualified person logograms) as tokens like `"VIR+KA"`, `"VIR+MUL"`, etc. These compound tokens are correctly recognized as logograms elsewhere in the script (via `LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", ...)`), but the co-occurrence check does not match them.

The result: `vir_cooccurrence_rate` was 0.0 for every suffix, silently disabling the VIR feature in the ergative score numerator. The score formula includes `vir_rate` as part of the ergative-like signal:

```python
ergative_score = kiro_rate + vir_rate + terminal_rate + eps
```

With `vir_rate` permanently zero, all ergative scores were computed without this feature.

The error was non-obvious because the KNOWN_LOGOGRAMS set and LOGOGRAM_PREFIXES tuple already handled VIR+ forms correctly for *classification* purposes — the bug existed only in the *co-occurrence counting* branch, which used a separate, narrower check.

#### Analytical Impact

After fixing to use `is_vir_family()` (which matches bare `"VIR"` and all `"VIR+"` compounds), the -JA baseline gained a real VIR rate of 10.3%. This affects the denominator of the normalization used to compute inverse-JA scores, causing all scores to shift downward:

| Suffix | Buggy Inv-JA Score | Corrected Score | Change |
|--------|--------------------|-----------------|--------|
| -RU | 4.448 | 3.761 | −0.687 |
| -TU | 3.892 | 3.140 | −0.752 |
| -SE | 3.094 | 2.427 | −0.667 |
| -RE | 3.058 | 2.506 | −0.552 |
| -MU | 2.512 | 1.839 | −0.673 |

The rank order of the top candidates is preserved (RU > TU > RE > SE). The -RU inverse-JA score (3.761) still comfortably exceeds the ≥3.0 threshold. Complementarity (83.3%) and site count (5) are unaffected — they don't use the VIR feature.

The corrected VIR rates are: -RU 13.3%, -JA 10.3% — a small but real difference consistent with an ergative/agent marker appearing slightly more often with person-counting records than the absolutive does. This is modest evidence, not strong evidence.

Note also: the follow-up question in `failed_attempts.md` ("Is -RU instrumental rather than ergative? Would explain 0% VIR co-occurrence") was based entirely on this bug. The 0% was an artifact. With corrected rates the question is less pointed, though -RU's weak VIR elevation is still not diagnostically strong on its own.

#### Fix Applied

Added a new helper function after `is_punct()`:

```python
def is_vir_family(token):
    """Match bare VIR logogram and all VIR+ compound forms (e.g. VIR+KA, VIR+MUL).
    Bug-fix note (2026-03-21): prior code used `'VIR' in tokens` (list membership),
    which is an exact-string match and cannot detect VIR+ compound tokens.
    """
    return token == "VIR" or token.startswith("VIR+")
```

Replaced the co-occurrence check:

```python
# Before (buggy):
if "VIR" in tokens:
    vir_cooc += 1

# After (fixed):
if any(is_vir_family(t) for t in tokens):
    vir_cooc += 1
```

Updated `failed_attempts.md` to correct the -RU score and the VIR-rate caveat.

#### Conclusion Status

**Unchanged:** H8c (-RU ergative candidate) remains SUPPORTED. The ergative score is lower but still above threshold. The hypothesis conclusion does not change; the support is slightly less extreme than reported but is still the strongest ergative candidate in the corpus by a clear margin.

**One prior "open question" is resolved:** The follow-up question "Is -RU instrumental? Would explain 0% VIR co-occurrence" in `failed_attempts.md` was a bug artifact. The corrected VIR rate for -RU (13.3%) is non-zero and slightly above -JA (10.3%), which is weakly consistent with ergative but not diagnostic.

#### Prevention Note

When checking whether a token class is present in a record, always use the same classification logic used elsewhere in the script (i.e., the `is_logogram()` / `is_vir_family()` helper), not an ad hoc string equality check. The LOGOGRAM_PREFIXES structure already encodes the VIR compound pattern — any co-occurrence or presence check for VIR should use a function that reads from the same source of truth. Code review should flag any bare string literal comparison against a sign name that also has known compound or variant forms.

---

*End of issue log. New entries prepended above this line.*
