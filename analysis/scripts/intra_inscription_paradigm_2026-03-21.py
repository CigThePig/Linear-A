"""
Intra-Inscription Case Paradigm Validation — H10a
Tests whether case forms of the same stem (from H9a paradigm results)
co-occur within single inscriptions. If they do, and if absolutive (-JA)
forms appear at structurally earlier positions than ergative (-RU) forms,
this is Tier 5 evidence for a real case system operating within texts.

Reuses helper functions from paradigm_alternation_2026-03-21.py verbatim.

Output: analysis/outputs/intra_inscription_paradigm_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
PARADIGM_PATH = "analysis/outputs/paradigm_alternation_2026-03-21.json"
OUTPUT_PATH = "analysis/outputs/intra_inscription_paradigm_2026-03-21.json"

# Reused from paradigm_alternation_2026-03-21.py
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

def load_paradigm():
    """Load paradigm stems and their confirmed case tokens from H9a output."""
    with open(PARADIGM_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Use high_confidence_suffixes only
    # Use top_paradigm_stems (all 30) not just strong_paradigms (15 subset)
    hc_suffixes = set(data.get("high_confidence_suffixes", []))
    stem_tokens = {}  # stem -> {token -> suffix}
    for entry in data.get("top_paradigm_stems", []):
        stem = entry["stem"]
        token_map = {}
        for suffix, sdata in entry.get("variants", {}).items():
            if suffix in hc_suffixes:
                token = f"{stem}-{suffix}"
                token_map[token] = suffix
        if len(token_map) >= 2:
            stem_tokens[stem] = token_map
    return stem_tokens, hc_suffixes

def main():
    records = load_corpus()
    stem_tokens, hc_suffixes = load_paradigm()

    # Build reverse index: token -> (stem, suffix) for quick lookup
    token_to_stem_suffix = {}
    for stem, token_map in stem_tokens.items():
        for token, suffix in token_map.items():
            token_to_stem_suffix[token] = (stem, suffix)

    # Find inscriptions with 2+ case forms of the same stem
    co_occurrence_records = []
    for rec in records:
        tokens = get_token_values(rec)
        if not tokens:
            continue
        # Find all paradigmatic tokens in this inscription
        found = defaultdict(list)  # stem -> [(token, suffix, position)]
        for pos, tok in enumerate(tokens):
            if tok in token_to_stem_suffix:
                stem, suffix = token_to_stem_suffix[tok]
                found[stem].append((tok, suffix, pos))
        # Only keep stems with 2+ different suffixes
        for stem, occurrences in found.items():
            unique_suffixes = set(s for _, s, _ in occurrences)
            if len(unique_suffixes) >= 2:
                co_occurrence_records.append({
                    "record_id": rec.get("id", ""),
                    "site": rec.get("site", ""),
                    "support": rec.get("support", ""),
                    "stem": stem,
                    "forms_found": [
                        {"token": tok, "suffix": suf, "position": pos, "total_tokens": len(tokens)}
                        for tok, suf, pos in occurrences
                    ],
                    "suffixes_present": sorted(unique_suffixes),
                    "full_token_list": tokens,
                })

    # Positional analysis: -JA vs -RU mean positions when they co-occur
    ja_positions = []
    ru_positions = []
    ja_ru_cooccurrences = []

    for entry in co_occurrence_records:
        suffixes_here = {f["suffix"]: f["position"] for f in entry["forms_found"]}
        if "JA" in suffixes_here and "RU" in suffixes_here:
            ja_pos = suffixes_here["JA"]
            ru_pos = suffixes_here["RU"]
            ja_positions.append(ja_pos)
            ru_positions.append(ru_pos)
            ja_ru_cooccurrences.append({
                "record_id": entry["record_id"],
                "site": entry["site"],
                "stem": entry["stem"],
                "JA_position": ja_pos,
                "RU_position": ru_pos,
                "JA_before_RU": ja_pos < ru_pos,
                "tokens": entry["full_token_list"],
            })

    # Positional analysis for all suffix pairs
    suffix_pair_stats = defaultdict(lambda: {"same_order": 0, "reverse_order": 0, "count": 0})
    for entry in co_occurrence_records:
        forms = entry["forms_found"]
        for i in range(len(forms)):
            for j in range(i + 1, len(forms)):
                s1, p1 = forms[i]["suffix"], forms[i]["position"]
                s2, p2 = forms[j]["suffix"], forms[j]["position"]
                if s1 != s2:
                    pair = tuple(sorted([s1, s2]))
                    key = f"{pair[0]}-{pair[1]}"
                    suffix_pair_stats[key]["count"] += 1
                    if (s1 < s2 and p1 < p2) or (s1 > s2 and p1 > p2):
                        suffix_pair_stats[key]["same_order"] += 1
                    else:
                        suffix_pair_stats[key]["reverse_order"] += 1

    # Summary statistics
    n_co_occurrences = len(co_occurrence_records)
    sites_represented = sorted(set(e["site"] for e in co_occurrence_records))
    stems_represented = sorted(set(e["stem"] for e in co_occurrence_records))

    ja_mean = sum(ja_positions) / len(ja_positions) if ja_positions else None
    ru_mean = sum(ru_positions) / len(ru_positions) if ru_positions else None
    ja_before_ru_count = sum(1 for x in ja_ru_cooccurrences if x["JA_before_RU"])

    output = {
        "analysis": "H10a: Intra-Inscription Case Paradigm Validation",
        "date": "2026-03-21",
        "corpus_records": len(records),
        "paradigm_stems_tested": len(stem_tokens),
        "inscriptions_with_cooccurrence": n_co_occurrences,
        "sites_represented": sites_represented,
        "stems_represented": stems_represented,
        "positional_analysis_JA_vs_RU": {
            "cooccurrence_count": len(ja_ru_cooccurrences),
            "ja_mean_position": round(ja_mean, 2) if ja_mean is not None else None,
            "ru_mean_position": round(ru_mean, 2) if ru_mean is not None else None,
            "ja_before_ru_count": ja_before_ru_count,
            "ja_before_ru_rate": round(ja_before_ru_count / len(ja_ru_cooccurrences), 3) if ja_ru_cooccurrences else None,
            "interpretation": (
                "ABSOLUTIVE-BEFORE-ERGATIVE CONFIRMED" if ja_mean is not None and ru_mean is not None and ja_mean < ru_mean
                else "insufficient data or no positional asymmetry"
            ),
        },
        "suffix_pair_positional_stats": {k: dict(v) for k, v in suffix_pair_stats.items()},
        "ja_ru_cooccurrence_details": ja_ru_cooccurrences,
        "all_cooccurrence_records": co_occurrence_records,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"H10a complete. {n_co_occurrences} inscriptions with intra-inscription case co-occurrence.")
    print(f"Stems: {stems_represented}")
    print(f"Sites: {sites_represented}")
    if ja_ru_cooccurrences:
        print(f"JA/RU co-occurrences: {len(ja_ru_cooccurrences)}")
        print(f"Mean JA position: {ja_mean:.2f}, mean RU position: {ru_mean:.2f}")
        print(f"JA before RU: {ja_before_ru_count}/{len(ja_ru_cooccurrences)} ({100*ja_before_ru_count/len(ja_ru_cooccurrences):.0f}%)")
    else:
        print("No JA/RU co-occurrences in same inscription.")

if __name__ == "__main__":
    main()
