"""
Coda / TA-NA- / U-TI-NU Sequence Analysis
Date: 2026-03-18
Hypothesis: The IOZa2 coda TA-NA-RA-TE-U-TI-NU and the IOZa6 header TA-NA-I-*301-U-TI-NU
share a -U-TI-NU terminal element that may be a formulaic closing or dedicant marker.
Tests positional distribution of TA-NA-* and *-U-TI-NU tokens across the corpus.
Output: analysis/outputs/coda_analysis_2026-03-18.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/coda_analysis_2026-03-18.json"

RITUAL_SUPPORTS = {"Stone vessel", "Metal object", "Architecture", "Stone object"}


def load_corpus():
    records = []
    with open(CORPUS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_token_values(tokens):
    values = []
    for t in tokens:
        if isinstance(t, dict):
            values.append(t.get("value", ""))
        elif isinstance(t, str):
            values.append(t)
    return values


def is_word_token(val):
    """True if this is a real word token (not separator, line break, numeral-only, etc.)."""
    if not val:
        return False
    if val in {"𐄁", "\\n", "\n", "↵", "|", "≈", "I", "II", "III", "IIII"}:
        return False
    # Skip pure numeral tokens (just digits)
    if val.isdigit():
        return False
    return True


def analyze_corpus(records):
    total = len(records)
    ritual_total = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS)

    # Collect TA-NA-* tokens
    tana_entries = defaultdict(list)
    # Collect *-U-TI-NU tokens
    utinu_entries = defaultdict(list)

    for record in records:
        raw_tokens = record.get("transliteration_tokens", [])
        if not isinstance(raw_tokens, list):
            continue

        token_values = get_token_values(raw_tokens)
        site = record.get("site", "Unknown")
        support = record.get("support", "Unknown")
        rec_id = record.get("id", "?")
        is_ritual = support in RITUAL_SUPPORTS

        # Word tokens only for position calculations
        word_vals = [v for v in token_values if is_word_token(v)]
        n_words = len(word_vals)

        for pos_idx, val in enumerate(token_values):
            if not val:
                continue

            # Compute word-level position (among word tokens only)
            word_pos = sum(1 for v in token_values[:pos_idx] if is_word_token(v))
            rel_word_pos = word_pos / max(n_words - 1, 1) if n_words > 1 else 0

            entry = {
                "id": rec_id,
                "site": site,
                "support": support,
                "is_ritual": is_ritual,
                "token": val,
                "raw_position": pos_idx,
                "total_raw_tokens": len(token_values),
                "word_position": word_pos,
                "total_word_tokens": n_words,
                "relative_word_position": round(rel_word_pos, 3),
                "full_token_list": token_values,
            }

            if val.startswith("TA-NA-"):
                tana_entries[val].append(entry)

            if val.endswith("U-TI-NU"):
                utinu_entries[val].append(entry)

    def summarize_entries(entries_dict):
        summary = {}
        for token_val, occurrences in entries_dict.items():
            n = len(occurrences)
            sites = sorted(set(o["site"] for o in occurrences))
            supports_found = sorted(set(o["support"] for o in occurrences))
            ritual_count = sum(1 for o in occurrences if o["is_ritual"])
            mean_rel_pos = sum(o["relative_word_position"] for o in occurrences) / n if n > 0 else 0

            # Position distribution: initial (0-0.2), early (0.2-0.4), mid (0.4-0.6), late (0.6-0.8), final (0.8-1.0)
            position_bins = {"initial": 0, "early": 0, "mid": 0, "late": 0, "final": 0}
            for o in occurrences:
                rp = o["relative_word_position"]
                if rp <= 0.2:
                    position_bins["initial"] += 1
                elif rp <= 0.4:
                    position_bins["early"] += 1
                elif rp <= 0.6:
                    position_bins["mid"] += 1
                elif rp <= 0.8:
                    position_bins["late"] += 1
                else:
                    position_bins["final"] += 1

            summary[token_val] = {
                "token": token_val,
                "occurrences": n,
                "sites": sites,
                "site_count": len(sites),
                "supports": supports_found,
                "ritual_count": ritual_count,
                "ritual_rate": round(ritual_count / n, 3) if n > 0 else 0,
                "mean_relative_word_position": round(mean_rel_pos, 3),
                "position_bins": position_bins,
                "inscription_ids": [o["id"] for o in occurrences],
                "details": [
                    {"id": o["id"], "site": o["site"], "support": o["support"],
                     "word_pos": o["word_position"], "total_words": o["total_word_tokens"],
                     "rel_pos": o["relative_word_position"]}
                    for o in occurrences
                ],
            }
        return summary

    tana_summary = summarize_entries(tana_entries)
    utinu_summary = summarize_entries(utinu_entries)

    # Special: look up full context for IOZa2 and IOZa6
    ioza2_context = None
    ioza6_context = None
    for record in records:
        rec_id = record.get("id", "")
        if rec_id == "IOZa2":
            ioza2_context = {
                "id": rec_id,
                "site": record.get("site"),
                "support": record.get("support"),
                "tokens": get_token_values(record.get("transliteration_tokens", [])),
            }
        elif rec_id == "IOZa6":
            ioza6_context = {
                "id": rec_id,
                "site": record.get("site"),
                "support": record.get("support"),
                "tokens": get_token_values(record.get("transliteration_tokens", [])),
            }

    return {
        "metadata": {
            "corpus_total": total,
            "ritual_total": ritual_total,
            "baseline_ritual_rate": round(ritual_total / total, 3),
        },
        "tana_token_summary": tana_summary,
        "utinu_token_summary": utinu_summary,
        "ioza2_full_context": ioza2_context,
        "ioza6_full_context": ioza6_context,
    }


def print_summary(results):
    meta = results["metadata"]
    print(f"\n=== CODA / TA-NA- / U-TI-NU ANALYSIS (2026-03-18) ===\n")
    print(f"Corpus: {meta['corpus_total']} records | Ritual baseline: {meta['baseline_ritual_rate']*100:.1f}%")

    print(f"\n--- TA-NA-* TOKENS ---")
    ts = results["tana_token_summary"]
    for token in sorted(ts.keys(), key=lambda t: ts[t]["occurrences"], reverse=True):
        d = ts[token]
        print(f"  {token:40s} occ={d['occurrences']:2d}  sites={d['site_count']}  "
              f"ritual={d['ritual_rate']:.0%}  mean_pos={d['mean_relative_word_position']:.2f}  "
              f"bins={d['position_bins']}")
        for det in d["details"]:
            print(f"      {det['id']:15s} ({det['site']:20s}, {det['support']:15s}) "
                  f"word {det['word_pos']}/{det['total_words']-1}  rel={det['rel_pos']:.2f}")

    print(f"\n--- *-U-TI-NU TOKENS ---")
    us = results["utinu_token_summary"]
    for token in sorted(us.keys(), key=lambda t: us[t]["occurrences"], reverse=True):
        d = us[token]
        print(f"  {token:40s} occ={d['occurrences']:2d}  sites={d['site_count']}  "
              f"ritual={d['ritual_rate']:.0%}  mean_pos={d['mean_relative_word_position']:.2f}  "
              f"bins={d['position_bins']}")
        for det in d["details"]:
            print(f"      {det['id']:15s} ({det['site']:20s}, {det['support']:15s}) "
                  f"word {det['word_pos']}/{det['total_words']-1}  rel={det['rel_pos']:.2f}")

    print(f"\n--- IOZa2 FULL INSCRIPTION ---")
    if results["ioza2_full_context"]:
        ctx = results["ioza2_full_context"]
        print(f"  {ctx['id']} ({ctx['site']}, {ctx['support']})")
        for i, t in enumerate(ctx["tokens"]):
            print(f"    [{i:2d}] {t}")

    print(f"\n--- IOZa6 FULL INSCRIPTION ---")
    if results["ioza6_full_context"]:
        ctx = results["ioza6_full_context"]
        print(f"  {ctx['id']} ({ctx['site']}, {ctx['support']})")
        for i, t in enumerate(ctx["tokens"]):
            print(f"    [{i:2d}] {t}")

    print(f"\n--- HYPOTHESIS EVALUATION ---")
    # Check if TA-NA-* is predominantly initial or final
    ts = results["tana_token_summary"]
    all_tana = []
    for d in ts.values():
        all_tana.extend(d["details"])
    if all_tana:
        initial_count = sum(1 for d in all_tana if d["rel_pos"] <= 0.2)
        final_count = sum(1 for d in all_tana if d["rel_pos"] >= 0.8)
        total_tana = len(all_tana)
        print(f"  All TA-NA-* tokens: {total_tana}")
        print(f"  Initial position (rel ≤ 0.2): {initial_count} ({initial_count/total_tana:.0%})")
        print(f"  Final position (rel ≥ 0.8): {final_count} ({final_count/total_tana:.0%})")
        if final_count > initial_count:
            print("  >> SUPPORTS H2 coda hypothesis (more final than initial)")
        elif initial_count > final_count:
            print("  >> CONTRADICTS H2 coda hypothesis (more initial than final) — TA-NA- may be a header")
        else:
            print("  >> INCONCLUSIVE (equal initial and final)")

    # Check if -U-TI-NU appears cross-site
    us = results["utinu_token_summary"]
    if us:
        all_utinu_sites = set()
        for d in us.values():
            all_utinu_sites.update(d["sites"])
        print(f"\n  -U-TI-NU terminal found in {len(us)} token types across sites: {sorted(all_utinu_sites)}")


if __name__ == "__main__":
    import os
    os.chdir("/home/user/Linear-A")

    print("Loading corpus...")
    records = load_corpus()
    print(f"Loaded {len(records)} records")

    print("Analyzing TA-NA- and U-TI-NU tokens...")
    results = analyze_corpus(records)

    print_summary(results)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {OUTPUT_PATH}")
