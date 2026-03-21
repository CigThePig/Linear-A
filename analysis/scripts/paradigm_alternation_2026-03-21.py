"""
Paradigmatic Stem Alternation Search — H9a
Finds Linear A word stems that appear with multiple different grammatical
suffixes in the corpus. This is a language-assumption-free test of whether
Linear A has an inflectional case system (Tier 5 evidence).

Method: Extract (stem, suffix) pairs from all multi-sign tokens, then find
stems appearing with 2+ different confirmed suffixes. Cross-validate by site.

Confirmed suffixes to test (from prior work):
  -JA: absolutive/intransitive (Medium-High confidence)
  -RU: ergative candidate (Medium confidence)
  -TE: directive candidate (Low-Medium)
  -NA: locative candidate (Low-Medium)
  -RE: accounting participant (Low-Medium)
  -DA: tested in H9d
  -NE: nominative plural candidate

Output: analysis/outputs/paradigm_alternation_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/paradigm_alternation_2026-03-21.json"

# Grammatical suffix syllables to search for
# These are the final syllable of a token
GRAMMATICAL_SUFFIXES = {"JA", "RU", "TE", "NA", "RE", "DA", "NE", "TI", "MA", "ME"}

# High-confidence grammatical suffixes (for scoring)
HIGH_CONF_SUFFIXES = {"JA", "RU", "TE", "NA", "RE", "DA"}

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

def extract_stem_and_suffix(token):
    """
    For a multi-sign token like A-TU-NA, return stem='A-TU' and suffix='NA'.
    For two-sign token DA-RE, return stem='DA' and suffix='RE'.
    Only considers tokens with at least 2 signs.
    """
    parts = token.split("-")
    if len(parts) < 2:
        return None, None
    # Filter out pure-numeral tokens
    if is_numeral(token):
        return None, None
    suffix = parts[-1]
    stem = "-".join(parts[:-1])
    return stem, suffix

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
    print(f"Loaded {len(records)} records")

    # stem -> suffix -> set of (record_id, site)
    stem_suffix_occurrences = defaultdict(lambda: defaultdict(set))
    # stem -> all tokens (to show examples)
    stem_tokens = defaultdict(set)

    for rec in records:
        rid = rec.get("id", "")
        site = rec.get("site", "") or "unknown"
        tokens = get_token_values(rec)

        for tok in tokens:
            if is_numeral(tok):
                continue
            stem, suffix = extract_stem_and_suffix(tok)
            if stem is None:
                continue
            if suffix not in GRAMMATICAL_SUFFIXES:
                continue
            # Require stem to be at least 1 sign (already guaranteed by len(parts)>=2)
            stem_suffix_occurrences[stem][suffix].add((rid, site))
            stem_tokens[stem].add(tok)

    # Find stems with 2+ different grammatical suffixes
    paradigm_stems = []
    for stem, suffix_dict in stem_suffix_occurrences.items():
        grammatical_variants = {s: occ for s, occ in suffix_dict.items() if s in GRAMMATICAL_SUFFIXES}
        if len(grammatical_variants) < 2:
            continue

        # High-confidence suffix count
        hc_variants = {s: occ for s, occ in grammatical_variants.items() if s in HIGH_CONF_SUFFIXES}

        # All sites across all suffix variants
        all_sites = set()
        for occ_set in grammatical_variants.values():
            all_sites.update(site for _, site in occ_set)

        # Total occurrences
        total_occ = sum(len(occ_set) for occ_set in grammatical_variants.values())

        # Scoring: prioritize stems with more variants, more sites, more HC suffixes
        score = (
            len(hc_variants) * 3 +      # High-confidence suffix pairs
            len(grammatical_variants) +  # Total suffix variety
            len(all_sites) * 2 +         # Geographic spread
            min(total_occ, 10)            # Frequency (capped)
        )

        # Build variant detail
        variants_detail = {}
        for suf, occ_set in sorted(grammatical_variants.items()):
            sites_for_suf = sorted(set(site for _, site in occ_set))
            record_ids = sorted(set(rid for rid, _ in occ_set))
            variants_detail[suf] = {
                "suffix": suf,
                "occurrences": len(occ_set),
                "sites": sites_for_suf,
                "record_ids": record_ids[:5],
            }

        paradigm_stems.append({
            "stem": stem,
            "suffix_count": len(grammatical_variants),
            "hc_suffix_count": len(hc_variants),
            "suffixes": sorted(grammatical_variants.keys()),
            "hc_suffixes": sorted(hc_variants.keys()),
            "total_site_count": len(all_sites),
            "sites": sorted(all_sites),
            "total_occurrences": total_occ,
            "score": score,
            "tokens": sorted(stem_tokens[stem]),
            "variants": variants_detail,
        })

    # Sort by score descending
    paradigm_stems.sort(key=lambda x: -x["score"])

    print(f"\nTotal stems with 2+ grammatical suffix variants: {len(paradigm_stems)}")

    # Filter to stems with at least 2 high-confidence suffixes
    strong_paradigms = [s for s in paradigm_stems if s["hc_suffix_count"] >= 2]
    print(f"Stems with 2+ HIGH-CONFIDENCE suffix variants: {len(strong_paradigms)}")

    print(f"\n=== TOP PARADIGMATIC STEMS (ranked by score) ===")
    for p in paradigm_stems[:25]:
        hc_mark = " ***" if p["hc_suffix_count"] >= 2 else ""
        print(f"  STEM: {p['stem']:<20s}  suffixes={p['suffixes']}  hc={p['hc_suffixes']}  sites={p['total_site_count']}  total={p['total_occurrences']}{hc_mark}")
        print(f"    tokens: {p['tokens'][:6]}")
        for suf, detail in p["variants"].items():
            if suf in HIGH_CONF_SUFFIXES:
                print(f"    -{suf}: {detail['occurrences']} occ @ {detail['sites']}")

    print(f"\n=== STRONG PARADIGMS (2+ HC suffixes) — DETAILED ===")
    for p in strong_paradigms[:15]:
        print(f"\n  STEM: {p['stem']}")
        print(f"  All tokens: {p['tokens']}")
        print(f"  Sites: {p['sites']}")
        for suf in p["hc_suffixes"]:
            detail = p["variants"][suf]
            print(f"  -{suf}: {detail['occurrences']} occ | sites: {detail['sites']} | records: {detail['record_ids'][:3]}")

    # Special case: check DA-KU paradigm found as preview
    print("\n=== CHECKING DA-KU PARADIGM (pre-identified) ===")
    if "DA-KU" in stem_suffix_occurrences:
        for suf, occ in stem_suffix_occurrences["DA-KU"].items():
            sites = sorted(set(site for _, site in occ))
            rids = sorted(set(rid for rid, _ in occ))
            print(f"  DA-KU-{suf}: {len(occ)} occ | {sites} | {rids}")
    else:
        print("  DA-KU not found as a stem.")
        # Try to find manually
        for rec in records:
            tokens = get_token_values(rec)
            dakus = [t for t in tokens if t.startswith("DA-KU")]
            if dakus:
                print(f"  [{rec['id']}] {rec.get('site')}: {dakus}")

    result = {
        "analysis": "paradigm_alternation",
        "date": "2026-03-21",
        "corpus_records": len(records),
        "grammatical_suffixes_tested": sorted(GRAMMATICAL_SUFFIXES),
        "high_confidence_suffixes": sorted(HIGH_CONF_SUFFIXES),
        "total_stems_with_2plus_variants": len(paradigm_stems),
        "stems_with_2plus_HC_variants": len(strong_paradigms),
        "top_paradigm_stems": paradigm_stems[:30],
        "strong_paradigms": strong_paradigms[:15],
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
