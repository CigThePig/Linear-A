"""
Logogram Sweep — H9c
Systematically identifies all signs in the corpus with logogram-like behavior
(high numeral-after rate, multi-site distribution) that are not yet confirmed.

Output: analysis/outputs/logogram_sweep_2026-03-21.json

Fix notes: Previous version had incorrect token extraction (assumed plain strings);
corpus uses {'type': 'token', 'value': ...} dicts. Also numeral detection now
handles Unicode superscript fractions and plain digit strings.
"""

import json
import re
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/logogram_sweep_2026-03-21.json"

# Already confirmed logograms and administrative terms — exclude from sweep
ALREADY_CONFIRMED = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "*304", "KU-RO", "KI-RO", "PO-TO-KU-RO",
    # Compound forms of confirmed logograms
    "GRA+QE", "GRA+PA", "GRA+KU",
    "OLE+U", "OLE+KI", "OLE+MI", "OLE+NE", "OLE+TA", "OLE+RI", "OLE+TU",
    "CYP+E", "CYP+D",
    "VIR+KA", "VIR+MUL", "VIR+[?]",
    # Structural/administrative already identified
    "*301",
}

RITUAL_SUPPORTS = {"stone vessel", "metal object", "stone object", "architecture"}

def get_token_values(rec):
    """Extract transliteration token values from a record's token list (dict format)."""
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
    """Return True if the token is a numeral or fraction."""
    if not v:
        return False
    v = v.strip()
    # Plain integer
    try:
        int(v)
        return True
    except ValueError:
        pass
    # Float
    try:
        float(v)
        return True
    except ValueError:
        pass
    # Unicode superscript/subscript fraction characters
    if any(c in v for c in "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁄") and len(v) <= 8:
        return True
    # ASCII fraction patterns
    if re.match(r"^\d+/\d+$", v):
        return True
    # Double-mina weight marker
    if "mina" in v.lower():
        return True
    return False

def is_ritual_support(rec):
    sup = (rec.get("support") or "").lower()
    return any(x in sup for x in ["stone vessel", "metal", "stone object", "libation"])

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

    token_total = defaultdict(int)
    token_records = defaultdict(set)
    token_sites = defaultdict(set)
    token_numeral_after = defaultdict(int)
    token_fraction_after = defaultdict(int)
    token_ritual = defaultdict(int)
    token_contexts = defaultdict(list)  # store sample contexts

    total_records = len(records)
    ritual_record_count = sum(1 for r in records if is_ritual_support(r))
    baseline_ritual_rate = ritual_record_count / total_records

    for rec in records:
        rid = rec.get("id", "")
        site = rec.get("site", "") or "unknown"
        tokens = get_token_values(rec)
        is_ritual = is_ritual_support(rec)

        for i, tok in enumerate(tokens):
            # Skip numerals, line-breaks, separators
            if is_numeral(tok) or tok in ("\n", "\\n", "≈", "—", "𐄁"):
                continue

            token_total[tok] += 1
            token_records[tok].add(rid)
            token_sites[tok].add(site)
            if is_ritual:
                token_ritual[tok] += 1

            # Check if next non-separator token is a numeral
            for j in range(i + 1, min(i + 3, len(tokens))):
                nxt = tokens[j]
                if nxt in ("𐄁", "≈", "—"):
                    continue
                if is_numeral(nxt):
                    token_numeral_after[tok] += 1
                    # Fraction check
                    if any(c in nxt for c in "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁄") or re.match(r"^\d+/\d+$", nxt):
                        token_fraction_after[tok] += 1
                break  # only look at the first non-separator

            # Store context sample
            if len(token_contexts[tok]) < 5:
                ctx = tokens[max(0, i-2):i+4]
                token_contexts[tok].append({"record": rid, "site": site, "context": ctx})

    # Build candidate list
    candidates = []
    for tok, total in token_total.items():
        if total < 4:
            continue
        sites = token_sites[tok]
        site_count = len(sites)
        if site_count < 2:
            continue

        numeral_after = token_numeral_after[tok]
        numeral_after_rate = numeral_after / total

        fraction_after = token_fraction_after[tok]
        fraction_rate = fraction_after / total

        ritual_count = token_ritual[tok]
        ritual_rate = ritual_count / len(token_records[tok]) if token_records[tok] else 0
        ritual_enrichment = ritual_rate / baseline_ritual_rate if baseline_ritual_rate > 0 else 0

        candidates.append({
            "token": tok,
            "total_occurrences": total,
            "record_count": len(token_records[tok]),
            "site_count": site_count,
            "sites": sorted(sites),
            "numeral_after_count": numeral_after,
            "numeral_after_rate": round(numeral_after_rate, 4),
            "fraction_after_count": fraction_after,
            "fraction_rate": round(fraction_rate, 4),
            "ritual_count": ritual_count,
            "ritual_enrichment": round(ritual_enrichment, 3),
            "already_confirmed": tok in ALREADY_CONFIRMED,
            "sample_contexts": token_contexts[tok][:3],
        })

    candidates.sort(key=lambda x: (-x["numeral_after_rate"], -x["site_count"], -x["total_occurrences"]))

    # Separate out confirmed vs new candidates
    new_candidates = [c for c in candidates if not c["already_confirmed"]]
    strong_new = [c for c in new_candidates if c["numeral_after_rate"] >= 0.65 and c["site_count"] >= 3]
    borderline_new = [c for c in new_candidates
                      if 0.45 <= c["numeral_after_rate"] < 0.65 and c["site_count"] >= 2 and c["total_occurrences"] >= 5]

    print(f"\n=== NEW LOGOGRAM CANDIDATES (numeral_after >= 65%, site_count >= 3, not confirmed) ===")
    for c in strong_new[:20]:
        print(f"  {c['token']:25s}  numeral_after={c['numeral_after_rate']:.1%}  sites={c['site_count']}  total={c['total_occurrences']:3d}  {sorted(c['sites'])[:4]}")

    print(f"\n=== BORDERLINE (45-65%, site_count >= 2, total >= 5, not confirmed) ===")
    for c in borderline_new[:15]:
        print(f"  {c['token']:25s}  numeral_after={c['numeral_after_rate']:.1%}  sites={c['site_count']}  total={c['total_occurrences']:3d}")

    print(f"\n=== CONFIRMED LOGOGRAMS (for comparison) ===")
    confirmed_in_data = [c for c in candidates if c["already_confirmed"]]
    for c in confirmed_in_data[:15]:
        print(f"  {c['token']:25s}  numeral_after={c['numeral_after_rate']:.1%}  sites={c['site_count']}  total={c['total_occurrences']:3d}")

    result = {
        "analysis": "logogram_sweep",
        "date": "2026-03-21",
        "total_records_analyzed": total_records,
        "baseline_ritual_rate": round(baseline_ritual_rate, 4),
        "new_logogram_candidates_strong": strong_new,
        "new_logogram_candidates_borderline": borderline_new[:20],
        "confirmed_logogram_stats": confirmed_in_data,
        "all_new_candidates_above_40pct": [c for c in new_candidates if c["numeral_after_rate"] >= 0.40 and c["site_count"] >= 2][:40],
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to {OUTPUT_PATH}")
    print(f"Strong new logogram candidates: {len(strong_new)}")
    print(f"Borderline new candidates: {len(borderline_new)}")

if __name__ == "__main__":
    main()
