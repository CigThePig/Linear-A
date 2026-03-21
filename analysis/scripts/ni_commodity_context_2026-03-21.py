"""
NI Commodity Identification — H10b
Systematically analyzes all corpus occurrences of the NI token to identify
what commodity it represents. NI has been confirmed as a logogram candidate
(68.4% numeral-after, 7 sites, 76 occurrences). This analysis computes
co-occurrence patterns with known logograms and cross-site context to
determine whether NI is most consistent with figs, a plant product, a
beverage, or another commodity.

Hypothesis: NI is the Linear A equivalent of the Linear B fig logogram
(*NI/FIG), since token "FIG" appears 0 times in the corpus.

Output: analysis/outputs/ni_commodity_context_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/ni_commodity_context_2026-03-21.json"

# Known logograms to test co-occurrence against
KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "*304", "NI",
    # Compound forms
    "GRA+QE", "GRA+PA", "GRA+KU",
    "OLE+U", "OLE+KI", "OLE+MI", "OLE+NE", "OLE+TA", "OLE+RI", "OLE+TU",
    "CYP+E", "CYP+D",
    "VIN+RA", "VIN+A",
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

def is_fraction(v):
    FRACTION_TOKENS = {"½", "¹⁄₂", "¹⁄₃", "¹⁄₄", "¹⁄₅", "¾", "²⁄₃", "¹⁄₆", ".3", ".5"}
    if v in FRACTION_TOKENS:
        return True
    if "⁄" in v or "½" in v:
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

def main():
    records = load_corpus()

    # 1. Find all records containing NI
    ni_records = []
    for rec in records:
        tokens = get_token_values(rec)
        if "NI" in tokens:
            ni_records.append((rec, tokens))

    # 2. For each NI occurrence, build context window and gather co-occurrence info
    ni_occurrences = []
    logogram_cooc_counts = defaultdict(int)  # logogram -> count of NI records where it also appears
    logogram_immediate_cooc = defaultdict(int)  # logogram -> count of times it's within ±3 of NI

    for rec, tokens in ni_records:
        for ni_pos, tok in enumerate(tokens):
            if tok != "NI":
                continue
            # Context window ±3
            ctx_start = max(0, ni_pos - 3)
            ctx_end = min(len(tokens), ni_pos + 4)
            context = tokens[ctx_start:ctx_end]

            # What's immediately after NI?
            after_tok = tokens[ni_pos + 1] if ni_pos + 1 < len(tokens) else None
            before_tok = tokens[ni_pos - 1] if ni_pos > 0 else None
            numeral_after = after_tok is not None and is_numeral(after_tok)
            fraction_before = before_tok is not None and is_fraction(before_tok)

            # Log all logograms in ±3 window
            for ctx_tok in context:
                if ctx_tok != "NI" and ctx_tok in KNOWN_LOGOGRAMS:
                    logogram_immediate_cooc[ctx_tok] += 1

            ni_occurrences.append({
                "record_id": rec.get("id", ""),
                "site": rec.get("site", ""),
                "support": rec.get("support", ""),
                "ni_position": ni_pos,
                "total_tokens": len(tokens),
                "context_window": context,
                "token_before": before_tok,
                "token_after": after_tok,
                "numeral_after": numeral_after,
                "fraction_before": fraction_before,
                "full_tokens": tokens,
            })

        # Record-level co-occurrence (any NI in record, any logogram in record)
        if "NI" in tokens:
            for log in KNOWN_LOGOGRAMS:
                if log != "NI" and log in tokens:
                    logogram_cooc_counts[log] += 1

    total_ni_occ = len(ni_occurrences)
    total_ni_records = len(ni_records)

    # 3. Site-level breakdown
    site_stats = defaultdict(lambda: {"records": 0, "occurrences": 0, "numeral_after_count": 0})
    for occ in ni_occurrences:
        s = occ["site"]
        site_stats[s]["occurrences"] += 1
        if occ["numeral_after"]:
            site_stats[s]["numeral_after_count"] += 1
    for rec, _ in ni_records:
        site_stats[rec.get("site", "")]["records"] += 1

    # 4. NI co-occurrence rates with known logograms (record level)
    logogram_cooc_rates = {}
    for log, cnt in sorted(logogram_cooc_counts.items(), key=lambda x: -x[1]):
        logogram_cooc_rates[log] = {
            "record_cooccurrences": cnt,
            "rate_among_NI_records": round(cnt / total_ni_records, 3),
            "immediate_cooccurrences_within3": logogram_immediate_cooc.get(log, 0),
        }

    # 5. What token most commonly follows NI?
    after_counts = defaultdict(int)
    before_counts = defaultdict(int)
    numeral_after_count = sum(1 for o in ni_occurrences if o["numeral_after"])
    fraction_before_count = sum(1 for o in ni_occurrences if o["fraction_before"])

    for occ in ni_occurrences:
        if occ["token_after"]:
            after_counts[occ["token_after"]] += 1
        if occ["token_before"]:
            before_counts[occ["token_before"]] += 1

    # 6. Support type breakdown
    support_counts = defaultdict(int)
    for rec, _ in ni_records:
        support_counts[rec.get("support", "unknown")] += 1

    ritual_records = sum(1 for rec, _ in ni_records if rec.get("support", "") in RITUAL_SUPPORTS)
    baseline_ritual_rate = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS) / len(records)
    ni_ritual_rate = ritual_records / total_ni_records if total_ni_records else 0

    # 7. Quantity analysis: what quantities appear with NI?
    quantities_seen = []
    for occ in ni_occurrences:
        if occ["numeral_after"] and occ["token_after"]:
            try:
                quantities_seen.append(float(occ["token_after"]))
            except:
                pass

    avg_quantity = sum(quantities_seen) / len(quantities_seen) if quantities_seen else None
    max_quantity = max(quantities_seen) if quantities_seen else None

    # 8. VIN adjacency: check if NI appears between VIN variants (as seen on Cretan stone object)
    vin_adjacent_count = sum(1 for occ in ni_occurrences
                              if any(t.startswith("VIN") for t in occ["context_window"] if t != "NI"))

    # 9. Agricultural context score
    # Score = rate of appearing in records that have GRA, VIN, or OLE (plant commodities)
    plant_logogram_records = 0
    for rec, tokens in ni_records:
        if any(t in {"GRA", "VIN", "OLE", "OLIV", "CYP", "OLE+KI", "OLE+NE", "OLE+TA"} for t in tokens):
            plant_logogram_records += 1

    # 10. Commodity classification
    # NI is most consistent with figs if:
    #   - appears in agricultural commodity lists (near GRA/VIN/OLE)
    #   - large quantities (figs processed in bulk)
    #   - tablet support (not ritual)
    #   - no strong wine or oil context
    wine_cooc = logogram_cooc_counts.get("VIN", 0) + logogram_cooc_counts.get("VIN+RA", 0) + logogram_cooc_counts.get("VIN+A", 0)
    oil_cooc = logogram_cooc_counts.get("OLE", 0) + sum(v for k, v in logogram_cooc_counts.items() if k.startswith("OLE+"))
    grain_cooc = logogram_cooc_counts.get("GRA", 0)
    plant_cooc = wine_cooc + oil_cooc + grain_cooc

    commodity_hypothesis = {
        "fig_hypothesis_score": 0,
        "wine_adjunct_hypothesis_score": 0,
        "grain_adjunct_hypothesis_score": 0,
        "notes": [],
    }
    # FIG score: high quantities (figs are bulk), appears with other plant commodities, not VIN-dominated
    if avg_quantity and avg_quantity > 5:
        commodity_hypothesis["fig_hypothesis_score"] += 1
        commodity_hypothesis["notes"].append("avg quantity > 5 is consistent with bulk agricultural product (figs)")
    if plant_logogram_records > total_ni_records * 0.3:
        commodity_hypothesis["fig_hypothesis_score"] += 1
        commodity_hypothesis["notes"].append(f"NI appears in plant-commodity records {plant_logogram_records}/{total_ni_records} times")
    if wine_cooc > oil_cooc and wine_cooc > grain_cooc:
        commodity_hypothesis["wine_adjunct_hypothesis_score"] += 2
        commodity_hypothesis["notes"].append("NI has highest co-occurrence with VIN (wine-related)")
    if grain_cooc > wine_cooc and grain_cooc > oil_cooc:
        commodity_hypothesis["grain_adjunct_hypothesis_score"] += 2
        commodity_hypothesis["notes"].append("NI has highest co-occurrence with GRA (grain-related)")
    if vin_adjacent_count > 3:
        commodity_hypothesis["wine_adjunct_hypothesis_score"] += 1
        commodity_hypothesis["notes"].append(f"NI appears within ±3 of VIN tokens in {vin_adjacent_count} occurrences")
    if ni_ritual_rate < baseline_ritual_rate:
        commodity_hypothesis["fig_hypothesis_score"] += 1
        commodity_hypothesis["notes"].append("NI has lower ritual rate than baseline — consistent with administrative commodity")

    # Determine top hypothesis
    scores = {
        "fig": commodity_hypothesis["fig_hypothesis_score"],
        "wine_adjunct": commodity_hypothesis["wine_adjunct_hypothesis_score"],
        "grain_adjunct": commodity_hypothesis["grain_adjunct_hypothesis_score"],
    }
    top_hypothesis = max(scores, key=scores.get)

    output = {
        "analysis": "H10b: NI Commodity Identification",
        "date": "2026-03-21",
        "corpus_records_total": len(records),
        "ni_total_records": total_ni_records,
        "ni_total_occurrences": total_ni_occ,
        "numeral_after_count": numeral_after_count,
        "numeral_after_rate": round(numeral_after_count / total_ni_occ, 3) if total_ni_occ else None,
        "fraction_before_count": fraction_before_count,
        "fraction_before_rate": round(fraction_before_count / total_ni_occ, 3) if total_ni_occ else None,
        "ritual_rate": round(ni_ritual_rate, 3),
        "baseline_ritual_rate": round(baseline_ritual_rate, 3),
        "ritual_enrichment": round(ni_ritual_rate / baseline_ritual_rate, 2) if baseline_ritual_rate else None,
        "support_type_breakdown": dict(support_counts),
        "site_breakdown": {k: dict(v) for k, v in site_stats.items()},
        "quantity_stats": {
            "count": len(quantities_seen),
            "avg": round(avg_quantity, 1) if avg_quantity else None,
            "max": max_quantity,
        },
        "vin_adjacent_occurrences": vin_adjacent_count,
        "plant_commodity_record_cooccurrence": plant_logogram_records,
        "logogram_cooccurrence_rates": logogram_cooc_rates,
        "top_10_tokens_after_NI": sorted(after_counts.items(), key=lambda x: -x[1])[:10],
        "top_10_tokens_before_NI": sorted(before_counts.items(), key=lambda x: -x[1])[:10],
        "commodity_classification": {
            "top_hypothesis": top_hypothesis,
            "scores": scores,
            "notes": commodity_hypothesis["notes"],
            "wine_cooc": wine_cooc,
            "oil_cooc": oil_cooc,
            "grain_cooc": grain_cooc,
        },
        "sample_occurrences": ni_occurrences[:15],
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"H10b complete. NI found in {total_ni_records} records, {total_ni_occ} occurrences across sites.")
    print(f"Numeral-after rate: {numeral_after_count}/{total_ni_occ} = {100*numeral_after_count/total_ni_occ:.1f}%")
    print(f"VIN adjacent: {vin_adjacent_count} occurrences; wine_cooc={wine_cooc}, oil_cooc={oil_cooc}, grain_cooc={grain_cooc}")
    print(f"Top commodity hypothesis: {top_hypothesis} (score={scores[top_hypothesis]})")

if __name__ == "__main__":
    main()
