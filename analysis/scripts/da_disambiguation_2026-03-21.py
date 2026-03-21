"""
-DA Grammatical Disambiguation — H10c
Separates the 16 unique -DA tokens (from H9d) into two classes:
  Class A: Proper nouns / toponyms (e.g., I-DA = Mt. Ida)
  Class B: Grammatical -DA case suffix on stems that also inflect for other cases

If Class A accounts for the high ritual enrichment (4.40x) found in H9d,
Class B alone should show a cleaner distributional profile compatible with
the Hurrian dative -da marker (low KI-RO, moderate KU-RO, low ritual).

Methodology:
- Class B criterion: stem (token minus -DA) appears in H9a paradigm with ≥1 other HC suffix
- Class A default: everything not classified as Class B

Output: analysis/outputs/da_disambiguation_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
DA_SUFFIX_PATH = "analysis/outputs/da_suffix_test_2026-03-21.json"
PARADIGM_PATH = "analysis/outputs/paradigm_alternation_2026-03-21.json"
OUTPUT_PATH = "analysis/outputs/da_disambiguation_2026-03-21.json"

# Known ritual sequence elements (from findings/formulaic_sequences.md)
RITUAL_SEQUENCE_ELEMENTS = {
    "JA-SA-SA-RA-ME", "JA-SA-SA-RA-MA", "JA-SA-SA-RA",
    "DI-KI-TE", "DI-KI",
    "U-NA-KA-NA-SI",
    "I-PI-NA-MA",
    "SI-RU-TE",
    "JA-DI-KI-TU",
    "A-TA-I-*301-WA-JA",
}

RITUAL_SUPPORTS = {"Stone vessel", "Metal object", "Stone object", "Architecture"}

def get_token_values(rec):
    raw = rec.get("transliteration_tokens", [])
    result = []
    for t in raw:
        if isinstance(t, dict):
            if t.get("type") == "token":
                v = t.get("value", "").strip()
                if v and v not in ("\n", "\\n", ""):
                    result.append(v)
        else:
            v = str(t).strip()
            if v and v not in ("\n", "\\n", ""):
                result.append(v)
    return result

def is_numeral(v):
    try:
        int(v); return True
    except: pass
    try:
        float(v); return True
    except: pass
    if any(c in v for c in "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁄") and len(v) <= 8:
        return True
    return False

def load_corpus():
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def extract_stem_from_da_token(token):
    """Extract stem by removing the final -DA sign."""
    parts = token.split("-")
    if len(parts) < 2 or parts[-1] != "DA":
        return None
    return "-".join(parts[:-1])

def main():
    records = load_corpus()

    # Load -DA token list from H9d
    with open(DA_SUFFIX_PATH, "r", encoding="utf-8") as f:
        da_data = json.load(f)
    da_tokens_list = da_data["results"]["-DA"]["unique_tokens_list"]

    # Load paradigm stems from H9a
    with open(PARADIGM_PATH, "r", encoding="utf-8") as f:
        paradigm_data = json.load(f)
    hc_suffixes = set(paradigm_data.get("high_confidence_suffixes", []))
    paradigm_stems = set()
    for entry in paradigm_data.get("strong_paradigms", []):
        paradigm_stems.add(entry["stem"])
    # Also include top_paradigm_stems
    for entry in paradigm_data.get("top_paradigm_stems", []):
        paradigm_stems.add(entry["stem"])

    # Also build a token -> suffixes map for cross-validation
    paradigm_stem_to_suffixes = {}
    for entry in paradigm_data.get("top_paradigm_stems", []):
        paradigm_stem_to_suffixes[entry["stem"]] = entry.get("hc_suffixes", [])

    # Classify each -DA token
    class_a = []  # proper noun / toponym
    class_b = []  # grammatical -DA suffix

    classification_details = {}

    for token in da_tokens_list:
        stem = extract_stem_from_da_token(token)
        is_class_b = False
        reason = ""

        if stem is not None and stem in paradigm_stems:
            other_suffixes = [s for s in paradigm_stem_to_suffixes.get(stem, []) if s != "DA"]
            if len(other_suffixes) >= 1:
                is_class_b = True
                reason = f"Stem '{stem}' appears in paradigm with other HC suffixes: {other_suffixes}"

        if is_class_b:
            class_b.append(token)
            classification_details[token] = {"class": "B", "stem": stem, "reason": reason}
        else:
            # Class A by default — further characterize
            signs = len(token.split("-"))
            is_ritual = token in RITUAL_SEQUENCE_ELEMENTS or any(r in token for r in ["JA-SA", "DI-KI"])
            if signs <= 2:
                a_reason = f"Short token ({signs} signs) — likely toponym or personal name"
            elif is_ritual:
                a_reason = "Matches or contains known ritual sequence element"
            else:
                a_reason = "Stem not found in H9a paradigm list; treated as proper noun / unclassified"
            class_a.append(token)
            classification_details[token] = {"class": "A", "stem": stem, "reason": a_reason}

    # Now recompute distributional profiles for Class A and Class B separately
    def compute_profile(token_subset):
        """Compute KI-RO rate, KU-RO rate, ritual rate, VIR rate for a set of tokens."""
        target_set = set(token_subset)
        records_with_token = []
        for rec in records:
            tokens = get_token_values(rec)
            if any(t in target_set for t in tokens):
                records_with_token.append((rec, tokens))

        if not records_with_token:
            return None

        n = len(records_with_token)
        kiro_count = sum(1 for rec, toks in records_with_token if "KI-RO" in toks)
        kuro_count = sum(1 for rec, toks in records_with_token if "KU-RO" in toks)
        ritual_count = sum(1 for rec, toks in records_with_token if rec.get("support", "") in RITUAL_SUPPORTS)
        vir_count = sum(1 for rec, toks in records_with_token
                         if any(t.startswith("VIR") for t in toks))

        baseline_ritual = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS) / len(records)

        # Token-level word-terminal rate
        terminal_count = 0
        total_token_occ = 0
        for rec, toks in records_with_token:
            for i, t in enumerate(toks):
                if t in target_set:
                    total_token_occ += 1
                    # Word-terminal: next token is numeral or end of sequence
                    next_tok = toks[i + 1] if i + 1 < len(toks) else None
                    if next_tok is None or is_numeral(next_tok):
                        terminal_count += 1

        return {
            "record_count": n,
            "kiro_rate": round(kiro_count / n, 3),
            "kuro_rate": round(kuro_count / n, 3),
            "ritual_rate": round(ritual_count / n, 3),
            "ritual_enrichment": round((ritual_count / n) / baseline_ritual, 2) if baseline_ritual else None,
            "vir_rate": round(vir_count / n, 3),
            "word_terminal_rate": round(terminal_count / total_token_occ, 3) if total_token_occ else None,
            "hurrian_dative_prediction": {
                "kiro_rate_expected": "< 0.1",
                "ritual_enrichment_expected": "< 2.0",
                "word_terminal_expected": "> 0.5",
            },
            "hurrian_dative_fit": (
                "SUPPORTED" if kiro_count / n < 0.1 and baseline_ritual > 0 and (ritual_count / n) / baseline_ritual < 2.0
                else ("NOT SUPPORTED" if baseline_ritual > 0 else "INCONCLUSIVE (no baseline)")
            ),
        }

    profile_all = compute_profile(da_tokens_list)
    profile_class_b = compute_profile(class_b) if class_b else None
    profile_class_a = compute_profile(class_a) if class_a else None

    output = {
        "analysis": "H10c: -DA Grammatical Disambiguation",
        "date": "2026-03-21",
        "total_da_tokens_tested": len(da_tokens_list),
        "class_a_count": len(class_a),
        "class_b_count": len(class_b),
        "class_a_tokens": class_a,
        "class_b_tokens": class_b,
        "classification_details": classification_details,
        "profile_all_da": profile_all,
        "profile_class_a_proper_nouns": profile_class_a,
        "profile_class_b_grammatical": profile_class_b,
        "conclusion": {
            "class_b_hurrian_dative_fit": profile_class_b["hurrian_dative_fit"] if profile_class_b else "insufficient data",
            "separation_successful": len(class_b) >= 2 and len(class_a) >= 2,
            "interpretation": (
                f"Class A ({len(class_a)} tokens: {class_a}) — proper nouns / toponyms. "
                f"Class B ({len(class_b)} tokens: {class_b}) — grammatical -DA case suffix. "
                + (f"Class B ritual enrichment: {profile_class_b['ritual_enrichment']}x "
                   f"(was 4.4x for all -DA combined)." if profile_class_b else "")
            ),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"H10c complete. {len(class_a)} Class A (proper noun), {len(class_b)} Class B (grammatical).")
    print(f"Class A: {class_a}")
    print(f"Class B: {class_b}")
    if profile_class_b:
        print(f"Class B profile — KI-RO: {profile_class_b['kiro_rate']}, "
              f"ritual enrichment: {profile_class_b['ritual_enrichment']}x, "
              f"Hurrian dative fit: {profile_class_b['hurrian_dative_fit']}")

if __name__ == "__main__":
    main()
