"""
DI-KI Element Corpus Analysis
Date: 2026-03-18
Hypothesis: JA-DI-KI-TU and A-DI-KI-TE share the DI-KI element which may correspond
to Mt. Dikte/Dikti (sacred Cretan mountain). Tests ritual enrichment and site distribution
of all DI-KI-containing tokens.
Output: analysis/outputs/dikte_analysis_2026-03-18.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/dikte_analysis_2026-03-18.json"

RITUAL_SUPPORTS = {"Stone vessel", "Metal object", "Architecture", "Stone object"}
MOUNTAIN_CULT_SITES = {"Iouktas", "Kophinas", "Palaikastro", "Troullos", "Vrysinas", "Syme"}
ADMIN_CENTERS = {"Haghia Triada", "Khania", "Phaistos", "Knossos", "Zakros"}


def load_corpus():
    records = []
    with open(CORPUS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_token_values(tokens):
    """Extract string values from transliteration_tokens list (list of dicts or strings)."""
    values = []
    for t in tokens:
        if isinstance(t, dict):
            values.append(t.get("value", ""))
        elif isinstance(t, str):
            values.append(t)
    return values


def token_contains_diki(token_val):
    """Check if a token value contains DI-KI as a contiguous syllable pair."""
    parts = token_val.split("-")
    for i in range(len(parts) - 1):
        if parts[i] == "DI" and parts[i + 1] == "KI":
            return True
    return False


def analyze_corpus(records):
    total = len(records)
    ritual_total = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS)

    # All tokens that contain DI-KI, keyed by token value
    diki_token_entries = defaultdict(list)

    # Full inscription details for each match
    full_inscription_details = []

    for record in records:
        raw_tokens = record.get("transliteration_tokens", [])
        if not isinstance(raw_tokens, list):
            continue

        token_values = get_token_values(raw_tokens)
        site = record.get("site", "Unknown")
        support = record.get("support", "Unknown")
        rec_id = record.get("id", "?")
        is_ritual = support in RITUAL_SUPPORTS

        # Find word tokens only (exclude separators, numerals, etc.)
        word_tokens = [v for v in token_values if v and not v.startswith("𐄁") and v != "\\n"]

        for pos_idx, val in enumerate(token_values):
            if token_contains_diki(val):
                entry = {
                    "id": rec_id,
                    "site": site,
                    "support": support,
                    "is_ritual": is_ritual,
                    "is_mountain_cult": site in MOUNTAIN_CULT_SITES,
                    "is_admin_center": site in ADMIN_CENTERS,
                    "token_position_in_full_list": pos_idx,
                    "total_tokens_in_list": len(token_values),
                    "full_token_list": token_values,
                }
                diki_token_entries[val].append(entry)

        has_diki = any(token_contains_diki(v) for v in token_values)
        if has_diki:
            full_inscription_details.append({
                "id": rec_id,
                "site": site,
                "support": support,
                "is_ritual": is_ritual,
                "tokens": token_values,
                "diki_tokens_found": [v for v in token_values if token_contains_diki(v)],
            })

    # Summarize per token type
    token_summary = {}
    for token_val, occurrences in diki_token_entries.items():
        sites = sorted(set(o["site"] for o in occurrences))
        supports_found = sorted(set(o["support"] for o in occurrences))
        ritual_count = sum(1 for o in occurrences if o["is_ritual"])
        mountain_count = sum(1 for o in occurrences if o["is_mountain_cult"])
        admin_count = sum(1 for o in occurrences if o["is_admin_center"])
        n = len(occurrences)
        ritual_rate = ritual_count / n if n > 0 else 0
        baseline_ritual_rate = ritual_total / total if total > 0 else 0
        ritual_enrichment = ritual_rate / baseline_ritual_rate if baseline_ritual_rate > 0 else 0

        token_summary[token_val] = {
            "token": token_val,
            "occurrences": n,
            "sites": sites,
            "site_count": len(sites),
            "supports": supports_found,
            "ritual_count": ritual_count,
            "ritual_rate": round(ritual_rate, 3),
            "ritual_enrichment_vs_baseline": round(ritual_enrichment, 2),
            "mountain_cult_count": mountain_count,
            "admin_center_count": admin_count,
            "inscription_ids": [o["id"] for o in occurrences],
        }

    return {
        "metadata": {
            "corpus_total": total,
            "ritual_support_total": ritual_total,
            "baseline_ritual_rate": round(ritual_total / total, 3),
            "diki_token_types": len(diki_token_entries),
            "total_diki_occurrences": sum(len(v) for v in diki_token_entries.values()),
            "inscriptions_with_diki": len(full_inscription_details),
        },
        "token_summary": token_summary,
        "full_inscription_details": full_inscription_details,
    }


def print_summary(results):
    meta = results["metadata"]
    print(f"\n=== DI-KI CORPUS ANALYSIS (2026-03-18) ===\n")
    print(f"Corpus: {meta['corpus_total']} records | Ritual records: {meta['ritual_support_total']} "
          f"({meta['baseline_ritual_rate']*100:.1f}% baseline)")
    print(f"DI-KI token types found: {meta['diki_token_types']}")
    print(f"Total DI-KI occurrences: {meta['total_diki_occurrences']}")
    print(f"Inscriptions with DI-KI: {meta['inscriptions_with_diki']}")

    print(f"\n--- DI-KI TOKEN INVENTORY (sorted by occurrence count) ---")
    ts = results["token_summary"]
    for token in sorted(ts.keys(), key=lambda t: ts[t]["occurrences"], reverse=True):
        d = ts[token]
        print(f"  {token:45s} occ={d['occurrences']:2d}  sites={d['site_count']}  "
              f"ritual={d['ritual_rate']:.0%}  enrich={d['ritual_enrichment_vs_baseline']:.1f}x  "
              f"mtn_cult={d['mountain_cult_count']}  ids={d['inscription_ids']}")

    print(f"\n--- INSCRIPTIONS WITH DI-KI ELEMENTS ---")
    for ins in results["full_inscription_details"]:
        print(f"\n  {ins['id']} ({ins['site']}, {ins['support']}, ritual={ins['is_ritual']})")
        print(f"    DI-KI tokens: {ins['diki_tokens_found']}")
        print(f"    Full: {ins['tokens']}")

    print(f"\n--- HYPOTHESIS EVALUATION ---")
    ts = results["token_summary"]
    all_diki = list(ts.values())
    total_diki = sum(d["occurrences"] for d in all_diki)
    total_ritual_diki = sum(d["ritual_count"] for d in all_diki)
    stone_vessel_diki = sum(1 for ins in results["full_inscription_details"] if ins["support"] == "Stone vessel")

    print(f"  Overall DI-KI ritual rate: {total_ritual_diki}/{total_diki} = {total_ritual_diki/total_diki:.0%}")
    print(f"  Baseline ritual rate: {meta['baseline_ritual_rate']*100:.1f}%")
    print(f"  DI-KI inscriptions on Stone vessels: {stone_vessel_diki}")

    mountain_ins = [ins for ins in results["full_inscription_details"] if ins["is_ritual"]]
    print(f"  DI-KI inscriptions at mountain/ritual sites: {len(mountain_ins)}")
    for ins in mountain_ins:
        print(f"    → {ins['id']} ({ins['site']}): {ins['diki_tokens_found']}")

    # Check common structure: JA- prefix vs A- prefix
    ja_prefix = {k: v for k, v in ts.items() if k.startswith("JA-DI-KI")}
    a_prefix = {k: v for k, v in ts.items() if k.startswith("A-DI-KI")}
    bare = {k: v for k, v in ts.items() if k == "DI-KI" or k.startswith("DI-KI-")}
    embedded = {k: v for k, v in ts.items() if "DI-KI" in k and not k.startswith("JA-DI-KI")
                and not k.startswith("A-DI-KI") and not k.startswith("DI-KI")}

    print(f"\n  JA- prefix forms: {list(ja_prefix.keys())}")
    print(f"  A- prefix forms: {list(a_prefix.keys())}")
    print(f"  Bare/DI-KI initial forms: {list(bare.keys())}")
    print(f"  Embedded DI-KI forms: {list(embedded.keys())}")


if __name__ == "__main__":
    import os
    os.chdir("/home/user/Linear-A")

    print("Loading corpus...")
    records = load_corpus()
    print(f"Loaded {len(records)} records")

    print("Analyzing DI-KI elements...")
    results = analyze_corpus(records)

    print_summary(results)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {OUTPUT_PATH}")
