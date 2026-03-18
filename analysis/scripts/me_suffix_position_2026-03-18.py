"""
-ME Suffix Syntactic Position Analysis
Date: 2026-03-18
Hypothesis: -ME is a divine vocative/invocative suffix that appears specifically
in early (invocation) positions of ritual inscriptions.
Tests positional distribution of -ME tokens vs. non-ME ritual tokens,
and checks whether -ME tokens precede or follow companion ritual elements.
Output: analysis/outputs/me_suffix_analysis_2026-03-18.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/me_suffix_analysis_2026-03-18.json"

RITUAL_SUPPORTS = {"Stone vessel", "Metal object", "Architecture", "Stone object"}
ADMIN_SUPPORTS = {"Tablet", "Nodule", "Roundel", "Clay vessel"}


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
    if not val:
        return False
    if val in {"𐄁", "\\n", "\n", "↵", "|", "≈"}:
        return False
    if val.isdigit():
        return False
    # Exclude pure numeral tokens (Roman numeral style)
    if all(c in "IVX" for c in val):
        return False
    return True


def ends_in_me(val):
    """Return True if token ends with syllable -ME (not just any letters 'me')."""
    parts = val.split("-")
    return len(parts) >= 2 and parts[-1] == "ME"


def analyze_corpus(records):
    total = len(records)
    ritual_total = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS)

    # All -ME tokens
    me_entries = []
    # All ritual non-ME tokens (for baseline position comparison)
    ritual_non_me_entries = []
    # Token type frequency for -ME
    me_token_freq = defaultdict(int)

    # Ritual anchor tokens for co-occurrence analysis
    ritual_anchors = {
        "JA-SA-SA-RA-ME", "JA-SA-SA-RA", "A-TA-I-*301-WA-JA", "I-PI-NA-MA",
        "SI-RU-TE", "U-NA-KA-NA-SI"
    }

    # For each inscription with -ME token: check ordering relative to companions
    ordering_evidence = []

    for record in records:
        raw_tokens = record.get("transliteration_tokens", [])
        if not isinstance(raw_tokens, list):
            continue

        token_values = get_token_values(raw_tokens)
        site = record.get("site", "Unknown")
        support = record.get("support", "Unknown")
        rec_id = record.get("id", "?")
        is_ritual = support in RITUAL_SUPPORTS
        is_admin = support in ADMIN_SUPPORTS

        # Word tokens for position calculation
        word_vals = [v for v in token_values if is_word_token(v)]
        n_words = len(word_vals)

        has_me_token = False
        for pos_idx, val in enumerate(token_values):
            if not val or not is_word_token(val):
                continue

            word_pos = sum(1 for v in token_values[:pos_idx] if is_word_token(v))
            rel_pos = word_pos / max(n_words - 1, 1) if n_words > 1 else 0

            entry = {
                "id": rec_id,
                "site": site,
                "support": support,
                "is_ritual": is_ritual,
                "token": val,
                "word_position": word_pos,
                "total_word_tokens": n_words,
                "relative_word_position": round(rel_pos, 3),
            }

            if ends_in_me(val):
                me_entries.append(entry)
                me_token_freq[val] += 1
                has_me_token = True
            elif is_ritual:
                ritual_non_me_entries.append(entry)

        # Ordering analysis: for inscriptions with ritual-context -ME token
        if is_ritual:
            token_set = set(v for v in token_values if is_word_token(v))
            me_in_inscription = [v for v in token_values if is_word_token(v) and ends_in_me(v)]
            anchor_in_inscription = [v for v in token_values if v in ritual_anchors]

            if me_in_inscription:
                # Find positions of -ME and companions
                word_token_list = [v for v in token_values if is_word_token(v)]
                me_positions = [i for i, v in enumerate(word_token_list) if ends_in_me(v)]
                anchor_positions = {v: [i for i, wv in enumerate(word_token_list) if wv == v]
                                    for v in anchor_in_inscription if v != me_in_inscription[0]}

                ordering_evidence.append({
                    "id": rec_id,
                    "site": site,
                    "support": support,
                    "me_tokens": me_in_inscription,
                    "me_word_positions": me_positions,
                    "total_word_tokens": len(word_token_list),
                    "anchor_tokens_in_inscription": anchor_in_inscription,
                    "word_token_sequence": word_token_list,
                })

    # Compute position statistics for ritual -ME vs non-ME ritual tokens
    def position_stats(entries):
        if not entries:
            return {}
        positions = [e["relative_word_position"] for e in entries]
        mean_pos = sum(positions) / len(positions)
        bins = {"initial(0-0.2)": 0, "early(0.2-0.4)": 0, "mid(0.4-0.6)": 0,
                "late(0.6-0.8)": 0, "final(0.8-1.0)": 0}
        for p in positions:
            if p <= 0.2:
                bins["initial(0-0.2)"] += 1
            elif p <= 0.4:
                bins["early(0.2-0.4)"] += 1
            elif p <= 0.6:
                bins["mid(0.4-0.6)"] += 1
            elif p <= 0.8:
                bins["late(0.6-0.8)"] += 1
            else:
                bins["final(0.8-1.0)"] += 1
        return {
            "count": len(entries),
            "mean_relative_position": round(mean_pos, 3),
            "position_bins": bins,
        }

    ritual_me_entries = [e for e in me_entries if e["is_ritual"]]
    admin_me_entries = [e for e in me_entries if not e["is_ritual"]]

    return {
        "metadata": {
            "corpus_total": total,
            "ritual_total": ritual_total,
            "baseline_ritual_rate": round(ritual_total / total, 3),
            "total_me_tokens": len(me_entries),
            "ritual_me_tokens": len(ritual_me_entries),
            "admin_me_tokens": len(admin_me_entries),
        },
        "me_token_frequency": dict(sorted(me_token_freq.items(), key=lambda x: x[1], reverse=True)),
        "ritual_me_position_stats": position_stats(ritual_me_entries),
        "admin_me_position_stats": position_stats(admin_me_entries),
        "ritual_non_me_position_stats": position_stats(ritual_non_me_entries),
        "ritual_me_details": [
            {"id": e["id"], "site": e["site"], "support": e["support"],
             "token": e["token"], "word_pos": e["word_position"],
             "total_words": e["total_word_tokens"], "rel_pos": e["relative_word_position"]}
            for e in ritual_me_entries
        ],
        "admin_me_details": [
            {"id": e["id"], "site": e["site"], "token": e["token"],
             "word_pos": e["word_position"], "total_words": e["total_word_tokens"],
             "rel_pos": e["relative_word_position"]}
            for e in admin_me_entries
        ],
        "ordering_evidence": ordering_evidence,
    }


def print_summary(results):
    meta = results["metadata"]
    print(f"\n=== -ME SUFFIX POSITIONAL ANALYSIS (2026-03-18) ===\n")
    print(f"Corpus: {meta['corpus_total']} records | Ritual baseline: {meta['baseline_ritual_rate']*100:.1f}%")
    print(f"Total -ME suffix tokens: {meta['total_me_tokens']}")
    print(f"  Ritual context: {meta['ritual_me_tokens']}")
    print(f"  Administrative context: {meta['admin_me_tokens']}")
    ritual_rate = meta['ritual_me_tokens'] / meta['total_me_tokens'] if meta['total_me_tokens'] > 0 else 0
    ritual_enrichment = ritual_rate / meta['baseline_ritual_rate'] if meta['baseline_ritual_rate'] > 0 else 0
    print(f"  Ritual rate: {ritual_rate:.0%} (baseline {meta['baseline_ritual_rate']*100:.1f}%)")
    print(f"  Ritual enrichment: {ritual_enrichment:.2f}x")

    print(f"\n--- -ME TOKEN FREQUENCY ---")
    for token, count in list(results["me_token_frequency"].items())[:20]:
        print(f"  {token:40s}: {count}")

    print(f"\n--- POSITIONAL STATISTICS ---")
    rme = results["ritual_me_position_stats"]
    ame = results["admin_me_position_stats"]
    rnm = results["ritual_non_me_position_stats"]

    print(f"  Ritual -ME tokens (n={rme.get('count', 0)}): mean_pos={rme.get('mean_relative_position', 'N/A')}")
    if "position_bins" in rme:
        for bin_name, cnt in rme["position_bins"].items():
            total = rme["count"]
            print(f"    {bin_name}: {cnt} ({cnt/total:.0%})")

    print(f"\n  Admin -ME tokens (n={ame.get('count', 0)}): mean_pos={ame.get('mean_relative_position', 'N/A')}")
    if "position_bins" in ame:
        for bin_name, cnt in ame["position_bins"].items():
            total = ame["count"] if ame["count"] > 0 else 1
            print(f"    {bin_name}: {cnt} ({cnt/total:.0%})")

    print(f"\n  Ritual non-ME tokens (n={rnm.get('count', 0)}, baseline): mean_pos={rnm.get('mean_relative_position', 'N/A')}")

    print(f"\n--- RITUAL -ME TOKEN DETAILS ---")
    for d in results["ritual_me_details"]:
        print(f"  {d['id']:15s} ({d['site']:20s}, {d['support']:15s}) "
              f"token={d['token']:30s} word {d['word_pos']}/{d['total_words']-1}  rel={d['rel_pos']:.2f}")

    print(f"\n--- ORDERING EVIDENCE (ritual inscriptions with -ME) ---")
    for ev in results["ordering_evidence"]:
        print(f"\n  {ev['id']} ({ev['site']}, {ev['support']})")
        print(f"    -ME tokens: {ev['me_tokens']} at positions {ev['me_word_positions']} / {ev['total_word_tokens']-1}")
        print(f"    Anchor tokens: {ev['anchor_tokens_in_inscription']}")
        print(f"    Word sequence: {ev['word_token_sequence']}")

    print(f"\n--- HYPOTHESIS EVALUATION ---")
    rme = results["ritual_me_position_stats"]
    rnm = results["ritual_non_me_position_stats"]
    if rme.get("mean_relative_position") and rnm.get("mean_relative_position"):
        me_pos = rme["mean_relative_position"]
        non_me_pos = rnm["mean_relative_position"]
        print(f"  Mean position of ritual -ME tokens: {me_pos:.3f}")
        print(f"  Mean position of other ritual tokens: {non_me_pos:.3f}")
        if me_pos < non_me_pos - 0.1:
            print("  >> SUPPORTS H3: -ME tokens appear earlier than other ritual tokens (vocative/initial position)")
        elif me_pos > non_me_pos + 0.1:
            print("  >> CONTRADICTS H3: -ME tokens appear later than other ritual tokens")
        else:
            print("  >> INCONCLUSIVE: -ME position not significantly different from other ritual tokens")

    # Check JA-SA-SA-RA-ME specifically
    jasassarame_entries = [d for d in results["ritual_me_details"] if d["token"] == "JA-SA-SA-RA-ME"]
    print(f"\n  JA-SA-SA-RA-ME specifically: {len(jasassarame_entries)} ritual occurrences")
    for d in jasassarame_entries:
        pct = d["word_pos"] / max(d["total_words"] - 1, 1)
        print(f"    {d['id']}: word {d['word_pos']}/{d['total_words']-1} = {pct:.0%} through inscription")


if __name__ == "__main__":
    import os
    os.chdir("/home/user/Linear-A")

    print("Loading corpus...")
    records = load_corpus()
    print(f"Loaded {len(records)} records")

    print("Analyzing -ME suffix position...")
    results = analyze_corpus(records)

    print_summary(results)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {OUTPUT_PATH}")
