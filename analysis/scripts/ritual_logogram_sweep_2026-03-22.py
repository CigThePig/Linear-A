"""
Numeral-Free Ritual Token Sweep — Attempt #13
==============================================
Searches for ritual logograms that appear WITHOUT following numerals.
Motivated by the Knossos Ivory Scepter (2025): ritual quadruped logograms
appear in a cultic inventory context WITHOUT numerals.

Prior logogram sweeps (Attempts #8, #9) required numeral-after rate > 65%.
This sweep tests the complementary class: ritual_enrichment >= 3x AND
numeral_after_rate < 20%.

Output: analysis/outputs/ritual_logogram_sweep_2026-03-22.json
"""

import json
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/ritual_logogram_sweep_2026-03-22.json"

RITUAL_SUPPORTS_LC = {"stone vessel", "metal object", "architecture", "stone object"}

# Known formula words to exclude from logogram candidates
KNOWN_FORMULA_WORDS = {
    "KU-RO", "KI-RO", "A-DU", "PO-TO-KU-RO",
    "A-TA-I-*301-WA-JA",
    "JA-SA-SA-RA-ME", "JA-SA-SA-RA-MA", "JA-SA-SA-RA",
    "U-NA-KA-NA-SI",
    "I-PI-NA-MA",
    "SI-RU-TE",
    "JA-DI-KI-TU",
    "A-DI-KI-TE-TE",
    "DI-KI-TE", "DI-KI",
    "TA-NA-RA-TE-U-TI-NU",
}

# Confirmed administrative logograms
ADMIN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "NI",
    "*304", "*22F", "*308", "*23M", "FIG", "TELA", "LANA", "AES",
    "GRA+TE", "GRA+QE", "OLE+KI",
}

# All confirmed vocabulary (to exclude from new candidates)
CONFIRMED_VOCAB = KNOWN_FORMULA_WORDS | ADMIN_LOGOGRAMS | {
    "SA-RA2", "*301", "*301-WA-JA",
}


def load_corpus():
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


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


def is_ritual_support(rec):
    s = rec.get("support", "").lower().strip()
    return s in RITUAL_SUPPORTS_LC


def main():
    records = load_corpus()
    total_records = len(records)
    ritual_records = [r for r in records if is_ritual_support(r)]
    baseline_ritual_rate = len(ritual_records) / total_records

    print(f"Total records: {total_records}")
    print(f"Ritual records: {len(ritual_records)} (baseline rate: {baseline_ritual_rate:.2%})")

    # Build per-token stats
    token_stats = defaultdict(lambda: {
        "total_occurrences": 0,
        "ritual_occurrences": 0,
        "total_records": set(),
        "ritual_records_set": set(),
        "all_sites": set(),
        "ritual_sites": set(),
        "numeral_after_count": 0,
        "numeral_before_count": 0,
        "admin_logogram_cooccurrence": Counter(),
        "ritual_anchor_cooccurrence": Counter(),
        "context_records": [],
    })

    RITUAL_ANCHORS = {"JA-SA-SA-RA-ME", "U-NA-KA-NA-SI", "I-PI-NA-MA", "SI-RU-TE",
                      "A-TA-I-*301-WA-JA"}

    for rec in records:
        tokens = get_token_values(rec)
        is_ritual = is_ritual_support(rec)
        site = rec.get("site", "unknown")
        rec_id = rec.get("id", "")

        # Admin logogram presence in this record
        admin_logs_in_rec = {t for t in tokens if t in ADMIN_LOGOGRAMS}
        ritual_anchors_in_rec = {t for t in tokens if t in RITUAL_ANCHORS}

        for i, t in enumerate(tokens):
            stats = token_stats[t]
            stats["total_occurrences"] += 1
            stats["total_records"].add(rec_id)
            stats["all_sites"].add(site)

            if is_ritual:
                stats["ritual_occurrences"] += 1
                stats["ritual_records_set"].add(rec_id)
                stats["ritual_sites"].add(site)

            # Numeral after
            if i + 1 < len(tokens) and is_numeral(tokens[i + 1]):
                stats["numeral_after_count"] += 1

            # Numeral before
            if i > 0 and is_numeral(tokens[i - 1]):
                stats["numeral_before_count"] += 1

        # Co-occurrence at record level
        for t in set(tokens):
            for al in admin_logs_in_rec:
                if al != t:
                    token_stats[t]["admin_logogram_cooccurrence"][al] += 1
            for ra in ritual_anchors_in_rec:
                if ra != t:
                    token_stats[t]["ritual_anchor_cooccurrence"][ra] += 1

    # Compute derived stats and filter
    candidates = []
    all_token_data = {}

    for token, stats in token_stats.items():
        total_occ = stats["total_occurrences"]
        ritual_occ = stats["ritual_occurrences"]
        total_recs = len(stats["total_records"])
        ritual_recs = len(stats["ritual_records_set"])
        ritual_site_count = len(stats["ritual_sites"])
        all_site_count = len(stats["all_sites"])
        numeral_after_rate = stats["numeral_after_count"] / total_occ if total_occ else 0
        ritual_rate = ritual_recs / total_recs if total_recs else 0
        ritual_enrichment = ritual_rate / baseline_ritual_rate if baseline_ritual_rate else 0

        token_data = {
            "total_occurrences": total_occ,
            "total_records": total_recs,
            "ritual_occurrences": ritual_occ,
            "ritual_records": ritual_recs,
            "all_sites": sorted([s for s in stats["all_sites"] if s is not None]),
            "ritual_sites": sorted([s for s in stats["ritual_sites"] if s is not None]),
            "all_site_count": all_site_count,
            "ritual_site_count": ritual_site_count,
            "numeral_after_rate": round(numeral_after_rate, 3),
            "ritual_rate": round(ritual_rate, 3),
            "ritual_enrichment": round(ritual_enrichment, 2),
            "admin_logogram_cooccurrence": dict(stats["admin_logogram_cooccurrence"].most_common(5)),
            "ritual_anchor_cooccurrence": dict(stats["ritual_anchor_cooccurrence"].most_common(5)),
            "is_known_formula": token in KNOWN_FORMULA_WORDS,
            "is_known_logogram": token in ADMIN_LOGOGRAMS,
            "is_confirmed_vocab": token in CONFIRMED_VOCAB,
        }
        all_token_data[token] = token_data

        # Primary filter: numeral-free ritual logogram candidates
        if (
            not token_data["is_confirmed_vocab"] and
            numeral_after_rate < 0.20 and
            ritual_enrichment >= 3.0 and
            total_occ >= 3 and
            ritual_site_count >= 2
        ):
            candidates.append((token, token_data))

    # Sort candidates by ritual_enrichment * ritual_site_count
    candidates.sort(key=lambda x: -(x[1]["ritual_enrichment"] * x[1]["ritual_site_count"]))

    # Also report a "near-miss" list: meets enrichment but fails one criterion
    near_misses = []
    for token, stats in token_stats.items():
        token_data = all_token_data[token]
        if token_data["is_confirmed_vocab"]:
            continue
        total_occ = stats["total_occurrences"]
        if total_occ < 2:
            continue
        ritual_enrichment = token_data["ritual_enrichment"]
        numeral_after_rate = token_data["numeral_after_rate"]
        ritual_site_count = token_data["ritual_site_count"]
        if ritual_enrichment >= 2.0 and numeral_after_rate < 0.30:
            if not any(t == token for t, _ in candidates):
                near_misses.append((token, token_data))
    near_misses.sort(key=lambda x: -(x[1]["ritual_enrichment"]))

    # Context detail for top candidates
    candidate_contexts = {}
    for token, data in candidates[:10]:
        contexts = []
        for rec in ritual_records:
            toks = get_token_values(rec)
            if token in toks:
                idx = toks.index(token)
                contexts.append({
                    "id": rec.get("id", ""),
                    "site": rec.get("site", ""),
                    "support": rec.get("support", ""),
                    "prev_token": toks[idx - 1] if idx > 0 else None,
                    "next_token": toks[idx + 1] if idx + 1 < len(toks) else None,
                    "full_tokens": toks,
                })
        candidate_contexts[token] = contexts

    output = {
        "analysis": "Attempt #13: Numeral-Free Ritual Token Sweep",
        "date": "2026-03-22",
        "new_information_source": (
            "Knossos Ivory Scepter (2025): Kanta, Nakassis, Palaima & Perna, "
            "Ariadne 27-43. Ritual quadruped logograms appear WITHOUT numerals."
        ),
        "corpus_stats": {
            "total_records": total_records,
            "ritual_records": len(ritual_records),
            "baseline_ritual_rate": round(baseline_ritual_rate, 4),
        },
        "filter_criteria": {
            "numeral_after_rate_max": 0.20,
            "ritual_enrichment_min": 3.0,
            "total_occurrences_min": 3,
            "ritual_site_count_min": 2,
            "excluded_confirmed_vocab": True,
        },
        "candidates_count": len(candidates),
        "candidates": [
            {
                "token": tok,
                "numeral_after_rate": data["numeral_after_rate"],
                "ritual_enrichment": data["ritual_enrichment"],
                "ritual_site_count": data["ritual_site_count"],
                "ritual_sites": data["ritual_sites"],
                "total_occurrences": data["total_occurrences"],
                "ritual_records": data["ritual_records"],
                "admin_logogram_cooccurrence": data["admin_logogram_cooccurrence"],
                "ritual_anchor_cooccurrence": data["ritual_anchor_cooccurrence"],
                "logogram_interpretation": "Candidate ritual logogram (numeral-free)",
            }
            for tok, data in candidates
        ],
        "near_misses_count": len(near_misses[:15]),
        "near_misses": [
            {
                "token": tok,
                "numeral_after_rate": data["numeral_after_rate"],
                "ritual_enrichment": data["ritual_enrichment"],
                "ritual_site_count": data["ritual_site_count"],
                "total_occurrences": data["total_occurrences"],
            }
            for tok, data in near_misses[:15]
        ],
        "candidate_contexts": candidate_contexts,
        "conclusion": {
            "numeral_free_ritual_logogram_class_exists": len(candidates) > 0,
            "candidates_found": len(candidates),
            "top_candidate": candidates[0][0] if candidates else None,
            "interpretation": (
                f"Found {len(candidates)} numeral-free ritual logogram candidates." if candidates
                else "No numeral-free ritual logograms found meeting all criteria. "
                     "Ritual logograms in this corpus may always be accompanied by numerals, "
                     "or the Knossos Scepter format is not represented in this dataset."
            ),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nAttempt #13 (Ritual Logogram Sweep) complete.")
    print(f"  Candidates meeting all criteria: {len(candidates)}")
    if candidates:
        print("  Top candidates:")
        for tok, data in candidates[:10]:
            print(f"    {tok}: numeral_after={data['numeral_after_rate']:.1%}, "
                  f"ritual_enrichment={data['ritual_enrichment']:.1f}x, "
                  f"ritual_sites={data['ritual_site_count']}, "
                  f"total_occ={data['total_occurrences']}")
    else:
        print("  No candidates found.")
    print(f"  Near-misses: {len(near_misses[:15])}")


if __name__ == "__main__":
    main()
