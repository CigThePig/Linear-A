"""
Pre-Logogram Lexical Sweep — H10d
Collects all tokens appearing immediately before known logograms and
identifies cross-site recurring patterns. Tokens at 3+ sites with ≥5
occurrences are vocabulary candidates (commodity modifiers, variety names,
or grammatical words like "fine/best/allocated").

Two candidate types:
  - Multi-logogram tokens (precede 3+ different logograms): likely grammatical/functional words
  - Single-logogram tokens (precede only 1 logogram at 3+ sites): likely variety/specific descriptors

Output: analysis/outputs/pre_logogram_sweep_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/pre_logogram_sweep_2026-03-21.json"

# Target logograms to search for pre-tokens
TARGET_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "CYP", "VIR", "MUL", "NI", "*304",
    # Compound forms also count as logogram occurrences
    "GRA+QE", "GRA+PA", "GRA+KU",
    "OLE+KI", "OLE+NE", "OLE+TA", "OLE+RI", "OLE+TU", "OLE+U", "OLE+MI",
    "CYP+E", "CYP+D",
    "VIN+RA", "VIN+A",
}

# Tokens to exclude from pre-logogram sweep
EXCLUDE_PRE_TOKENS = {
    # Known formula words
    "KU-RO", "KI-RO", "PO-TO-KU-RO", "A-DU", "*301",
    # Structural signs
    "𐄁", "𐝂", "𐝂𐝂", "𐝂𐝂𐝂", "𐝂𐝂𐝂𐝂",
    # Known logograms themselves (logogram before logogram = compound, not pre-token)
    "GRA", "VIN", "OLE", "OLIV", "CYP", "VIR", "MUL", "NI", "*304",
    "GRA+QE", "GRA+PA", "GRA+KU",
    "OLE+KI", "OLE+NE", "OLE+TA", "OLE+RI", "OLE+TU", "OLE+U", "OLE+MI",
    "CYP+E", "CYP+D",
    "VIN+RA", "VIN+A",
    "*308", "*22F", "*22M", "*21M", "*21F",
    "OLIV",
}

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
    if not v:
        return False
    v = v.strip()
    try:
        int(v); return True
    except: pass
    try:
        float(v); return True
    except: pass
    if any(c in v for c in "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁄") and len(v) <= 8:
        return True
    FRACTION_TOKENS = {"½", "¹⁄₂", "¹⁄₃", "¹⁄₄", "¹⁄₅", "¾", "²⁄₃", "¹⁄₆", ".3", ".5"}
    return v in FRACTION_TOKENS

def load_corpus():
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def main():
    records = load_corpus()

    # (pre_token, logogram) -> {sites, records, count}
    pre_token_data = defaultdict(lambda: {
        "count": 0,
        "sites": set(),
        "records": [],
        "logograms_preceded": set(),
    })

    for rec in records:
        tokens = get_token_values(rec)
        site = rec.get("site", "")
        rec_id = rec.get("id", "")

        for i, tok in enumerate(tokens):
            if tok not in TARGET_LOGOGRAMS:
                continue
            if i == 0:
                continue
            pre_tok = tokens[i - 1]
            # Exclude numerals, fractions, and known formula words / logograms
            if is_numeral(pre_tok):
                continue
            if pre_tok in EXCLUDE_PRE_TOKENS:
                continue
            if not pre_tok or pre_tok in ("\n", "\\n", "𐄁"):
                continue

            key = pre_tok
            pre_token_data[key]["count"] += 1
            pre_token_data[key]["sites"].add(site)
            pre_token_data[key]["records"].append(rec_id)
            pre_token_data[key]["logograms_preceded"].add(tok)

    # Build candidate list with filters
    candidates = []
    for pre_tok, data in pre_token_data.items():
        site_count = len(data["sites"])
        occ_count = data["count"]
        logograms = sorted(data["logograms_preceded"])
        n_logograms = len(logograms)

        if site_count < 3 or occ_count < 5:
            continue

        # Classify
        if n_logograms >= 3:
            candidate_type = "functional/grammatical (precedes multiple logogram types)"
        elif n_logograms == 2:
            candidate_type = "possible commodity group modifier"
        else:
            candidate_type = f"specific descriptor for {logograms[0]}"

        candidates.append({
            "pre_token": pre_tok,
            "total_occurrences": occ_count,
            "site_count": site_count,
            "sites": sorted(data["sites"]),
            "logograms_preceded": logograms,
            "n_distinct_logograms": n_logograms,
            "candidate_type": candidate_type,
            "score": site_count * occ_count,
            "sample_records": sorted(set(data["records"]))[:8],
        })

    # Sort by score descending
    candidates.sort(key=lambda x: -x["score"])

    # Separate by type
    functional_candidates = [c for c in candidates if c["n_distinct_logograms"] >= 3]
    specific_descriptor_candidates = [c for c in candidates if c["n_distinct_logograms"] == 1]
    group_modifier_candidates = [c for c in candidates if c["n_distinct_logograms"] == 2]

    # Also compute how many distinct records each pre_token appears in
    # (vs. total occurrences)

    output = {
        "analysis": "H10d: Pre-Logogram Lexical Sweep",
        "date": "2026-03-21",
        "corpus_records": len(records),
        "target_logograms": sorted(TARGET_LOGOGRAMS),
        "total_candidates_before_filter": len(pre_token_data),
        "candidates_meeting_threshold": len(candidates),
        "threshold": {"min_site_count": 3, "min_occurrences": 5},
        "all_candidates_ranked": candidates[:30],
        "functional_grammatical_candidates": functional_candidates[:10],
        "commodity_specific_descriptors": specific_descriptor_candidates[:10],
        "commodity_group_modifiers": group_modifier_candidates[:10],
        "vocabulary_promotion_recommendations": [
            c for c in candidates if c["site_count"] >= 5 or c["total_occurrences"] >= 10
        ][:10],
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"H10d complete. {len(candidates)} candidates meeting 3-site/5-occurrence threshold.")
    print(f"  Functional/grammatical (≥3 logograms): {len(functional_candidates)}")
    print(f"  Commodity-specific descriptors (1 logogram): {len(specific_descriptor_candidates)}")
    print(f"  Group modifiers (2 logograms): {len(group_modifier_candidates)}")
    if candidates:
        print(f"\nTop candidates:")
        for c in candidates[:8]:
            print(f"  {c['pre_token']:20s} occ={c['total_occurrences']:3d} sites={c['site_count']} "
                  f"logs={c['logograms_preceded']} type={c['candidate_type'][:40]}")

if __name__ == "__main__":
    main()
