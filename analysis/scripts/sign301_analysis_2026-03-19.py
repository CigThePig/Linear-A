"""
Sign *301 Context Separation Analysis
Linear A Decipherment Project — 2026-03-19

H3: Sign *301 has a distinct distributional co-occurrence profile in administrative
vs. ritual records. If admin/ritual profiles share <30% of their top co-occurrence
partners (PMI-weighted), *301 may serve different functions across registers.

Secondary checks:
- Does *301 in admin records immediately precede numerals? (logographic indicator)
- Is *301 positionally consistent within admin records?

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/sign301_analysis_2026-03-19.json
"""

import json
import re
import math
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/sign301_analysis_2026-03-19.json")

TARGET_SIGN = "*301"

ADMIN_SUPPORTS = {"tablet", "nodule", "roundel", "clay vessel", "lame", "label"}
RITUAL_SUPPORTS = {"stone vessel", "metal object", "architecture", "ivory object"}

NUM_RE = re.compile(r"^\d+$|^[¼½¾⅐-⅟]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈", "|", "//"}

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "MUL+", "GRA2", "OLE2")


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_tokens(record):
    return [
        t["value"]
        for t in record.get("transliteration_tokens", [])
        if t.get("type") == "token"
    ]


def is_numeral(token):
    return bool(NUM_RE.match(token))


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_logogram(token):
    if token in KNOWN_LOGOGRAMS:
        return True
    for p in LOGOGRAM_PREFIXES:
        if token.startswith(p):
            return True
    if re.match(r"^[A-Z]{2,5}$", token) and "+" not in token and "-" not in token:
        return True
    return False


def sign_present(tokens, sign):
    """Check if the target sign appears in the token list."""
    return any(t == sign or t.startswith(sign + "+") for t in tokens)


def find_sign_positions(tokens, sign):
    """Return all indices where the target sign appears."""
    return [
        i for i, t in enumerate(tokens)
        if t == sign or t.startswith(sign + "+")
    ]


def extract_context_windows(tokens, positions, window=3):
    """
    For each occurrence position, extract the surrounding token window.
    Returns list of (left_tokens, right_tokens) excluding punct.
    """
    windows = []
    for pos in positions:
        left = [
            t for t in tokens[max(0, pos - window):pos]
            if not is_punct(t)
        ]
        right = [
            t for t in tokens[pos + 1:pos + 1 + window]
            if not is_punct(t)
        ]
        windows.append({
            "position": pos,
            "total_tokens": len(tokens),
            "relative_position": round(pos / max(len(tokens) - 1, 1), 3),
            "left_context": left,
            "right_context": right,
            "immediately_before_numeral": (
                pos + 1 < len(tokens) and is_numeral(tokens[pos + 1])
            ),
            "immediately_after_numeral": (
                pos > 0 and is_numeral(tokens[pos - 1])
            ),
            "immediately_before_logogram": (
                pos + 1 < len(tokens) and is_logogram(tokens[pos + 1])
            ),
            "immediately_after_logogram": (
                pos > 0 and is_logogram(tokens[pos - 1])
            ),
        })
    return windows


def build_cooccurrence_vector(all_windows, total_corpus_sign_counts, target_count, window=3):
    """
    Build PMI-weighted co-occurrence vector from context windows.
    PMI(target, s) = log2( P(target,s) / P(target)*P(s) )
    Returns Counter of co-occurrence partner -> PMI score.
    """
    N = sum(total_corpus_sign_counts.values())
    p_target = target_count / N if N > 0 else 0

    partner_counts = Counter()
    for ctx in all_windows:
        for tok in ctx["left_context"] + ctx["right_context"]:
            if not is_punct(tok) and not is_numeral(tok) and tok != TARGET_SIGN:
                partner_counts[tok] += 1

    pmi_scores = {}
    for partner, co_count in partner_counts.items():
        p_partner = total_corpus_sign_counts.get(partner, 0) / N if N > 0 else 0
        if p_partner <= 0 or p_target <= 0:
            continue
        p_joint = co_count / N
        pmi = math.log2(p_joint / (p_target * p_partner)) if p_joint > 0 else -999
        pmi_scores[partner] = round(pmi, 3)

    return dict(sorted(pmi_scores.items(), key=lambda x: -x[1]))


def compute_corpus_sign_counts(records):
    """Count how often each sign appears across the full corpus."""
    counts = Counter()
    for r in records:
        for t in get_tokens(r):
            if not is_punct(t) and not is_numeral(t):
                counts[t] += 1
    return counts


def compute_overlap(top_admin, top_ritual, n=20):
    """Compute overlap fraction between top-N partners in two contexts."""
    admin_set = set(list(top_admin.keys())[:n])
    ritual_set = set(list(top_ritual.keys())[:n])
    if not admin_set and not ritual_set:
        return 1.0
    overlap = len(admin_set & ritual_set)
    return round(overlap / n, 3)


def analyze_positional_consistency(all_windows_by_record):
    """Check if *301 appears at consistent positions within records."""
    rel_positions = []
    is_first = []
    is_last = []
    for rid, windows in all_windows_by_record.items():
        for w in windows:
            rel = w["relative_position"]
            total = w["total_tokens"]
            rel_positions.append(rel)
            is_first.append(rel < 0.15)
            is_last.append(rel > 0.85)
    if not rel_positions:
        return {}
    return {
        "count": len(rel_positions),
        "mean_relative_position": round(sum(rel_positions) / len(rel_positions), 3),
        "first_position_rate": round(sum(is_first) / len(is_first), 3),
        "last_position_rate": round(sum(is_last) / len(is_last), 3),
        "median_relative_position": round(sorted(rel_positions)[len(rel_positions) // 2], 3),
    }


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    corpus_sign_counts = compute_corpus_sign_counts(records)

    # Split records by register
    admin_records = [r for r in records if (r.get("support") or "").lower() in ADMIN_SUPPORTS]
    ritual_records = [r for r in records if (r.get("support") or "").lower() in RITUAL_SUPPORTS]
    other_records = [r for r in records if r not in admin_records and r not in ritual_records]

    print(f"Admin records: {len(admin_records)}, Ritual records: {len(ritual_records)}, Other: {len(other_records)}")

    # Find *301 occurrences per register
    admin_with_301 = [r for r in admin_records if sign_present(get_tokens(r), TARGET_SIGN)]
    ritual_with_301 = [r for r in ritual_records if sign_present(get_tokens(r), TARGET_SIGN)]
    other_with_301 = [r for r in other_records if sign_present(get_tokens(r), TARGET_SIGN)]

    print(f"\n*301 occurrences: admin={len(admin_with_301)}, ritual={len(ritual_with_301)}, other={len(other_with_301)}")

    # Extract all context windows for each register
    admin_windows = []
    admin_windows_by_record = {}
    for r in admin_with_301:
        tokens = get_tokens(r)
        positions = find_sign_positions(tokens, TARGET_SIGN)
        windows = extract_context_windows(tokens, positions)
        admin_windows.extend(windows)
        admin_windows_by_record[r.get("id", "")] = windows

    ritual_windows = []
    ritual_windows_by_record = {}
    for r in ritual_with_301:
        tokens = get_tokens(r)
        positions = find_sign_positions(tokens, TARGET_SIGN)
        windows = extract_context_windows(tokens, positions)
        ritual_windows.extend(windows)
        ritual_windows_by_record[r.get("id", "")] = windows

    # Count total *301 appearances
    admin_301_count = sum(len(find_sign_positions(get_tokens(r), TARGET_SIGN)) for r in admin_with_301)
    ritual_301_count = sum(len(find_sign_positions(get_tokens(r), TARGET_SIGN)) for r in ritual_with_301)
    total_301_count = corpus_sign_counts.get(TARGET_SIGN, 0)

    print(f"Total *301 token count: {total_301_count}")
    print(f"  Admin appearances: {admin_301_count}")
    print(f"  Ritual appearances: {ritual_301_count}")

    # Build PMI co-occurrence vectors
    admin_pmi = build_cooccurrence_vector(
        admin_windows, corpus_sign_counts, admin_301_count
    )
    ritual_pmi = build_cooccurrence_vector(
        ritual_windows, corpus_sign_counts, ritual_301_count
    )

    # Compute overlap
    n_overlap = 20
    overlap_fraction = compute_overlap(admin_pmi, ritual_pmi, n=n_overlap)
    print(f"\nAdmin vs. ritual top-{n_overlap} co-occurrence overlap: {overlap_fraction:.1%}")

    # H3 evaluation
    threshold = 0.30
    if admin_301_count < 3 or ritual_301_count < 3:
        h3_result = "INCONCLUSIVE — insufficient data in one register"
    elif overlap_fraction < threshold:
        h3_result = f"SUPPORTED — overlap {overlap_fraction:.1%} < {threshold:.0%} threshold"
    else:
        h3_result = f"FAILED — overlap {overlap_fraction:.1%} ≥ {threshold:.0%} threshold"

    print(f"H3 result: {h3_result}")

    # Secondary checks
    admin_pre_numeral_rate = (
        sum(1 for w in admin_windows if w["immediately_before_numeral"]) / max(len(admin_windows), 1)
    )
    admin_pre_logogram_rate = (
        sum(1 for w in admin_windows if w["immediately_before_logogram"]) / max(len(admin_windows), 1)
    )
    ritual_pre_numeral_rate = (
        sum(1 for w in ritual_windows if w["immediately_before_numeral"]) / max(len(ritual_windows), 1)
    )

    print(f"\nAdmin *301 immediately before numeral: {admin_pre_numeral_rate:.1%}")
    print(f"Admin *301 immediately before logogram: {admin_pre_logogram_rate:.1%}")
    print(f"Ritual *301 immediately before numeral: {ritual_pre_numeral_rate:.1%}")

    # Positional consistency
    admin_pos = analyze_positional_consistency(admin_windows_by_record)
    ritual_pos = analyze_positional_consistency(ritual_windows_by_record)

    print(f"\nAdmin *301 mean relative position: {admin_pos.get('mean_relative_position', 'N/A')}")
    print(f"Ritual *301 mean relative position: {ritual_pos.get('mean_relative_position', 'N/A')}")
    print(f"Admin *301 first-position rate: {admin_pos.get('first_position_rate', 'N/A')}")
    print(f"Ritual *301 first-position rate: {ritual_pos.get('first_position_rate', 'N/A')}")

    # Per-record detail for ritual (small set, fully analyzable)
    ritual_record_details = []
    for r in ritual_with_301:
        tokens = get_tokens(r)
        ritual_record_details.append({
            "id": r.get("id", ""),
            "site": r.get("site", ""),
            "support": r.get("support", ""),
            "canonical_name": r.get("canonical_name", ""),
            "tokens": tokens,
            "sign301_positions": find_sign_positions(tokens, TARGET_SIGN),
        })

    # Site distribution for admin *301 records
    admin_sites = Counter(r.get("site", "unknown") for r in admin_with_301)
    ritual_sites = Counter(r.get("site", "unknown") for r in ritual_with_301)

    # Context examples
    admin_examples = [
        {
            "record_id": r.get("id", ""),
            "site": r.get("site", ""),
            "tokens": get_tokens(r)[:20],
        }
        for r in admin_with_301[:10]
    ]

    output = {
        "analysis": "H3: Sign *301 Context Separation (Admin vs. Ritual)",
        "date": "2026-03-19",
        "target_sign": TARGET_SIGN,
        "corpus_size": len(records),
        "hypothesis_result": h3_result,
        "success_threshold": f"Overlap < {threshold:.0%}",
        "overlap_fraction": overlap_fraction,
        "register_counts": {
            "admin_records_with_301": len(admin_with_301),
            "ritual_records_with_301": len(ritual_with_301),
            "other_records_with_301": len(other_with_301),
            "admin_301_appearances": admin_301_count,
            "ritual_301_appearances": ritual_301_count,
            "total_301_corpus_count": total_301_count,
        },
        "admin_site_distribution": dict(admin_sites.most_common()),
        "ritual_site_distribution": dict(ritual_sites.most_common()),
        "admin_positional_stats": admin_pos,
        "ritual_positional_stats": ritual_pos,
        "secondary_checks": {
            "admin_immediately_before_numeral_rate": round(admin_pre_numeral_rate, 3),
            "admin_immediately_before_logogram_rate": round(admin_pre_logogram_rate, 3),
            "ritual_immediately_before_numeral_rate": round(ritual_pre_numeral_rate, 3),
            "logographic_indicator": (
                "YES — high pre-numeral rate" if admin_pre_numeral_rate >= 0.15
                else "NO — low pre-numeral rate"
            ),
        },
        "admin_pmi_top20": dict(list(admin_pmi.items())[:20]),
        "ritual_pmi_top20": dict(list(ritual_pmi.items())[:20]),
        "admin_ritual_shared_partners": list(
            set(list(admin_pmi.keys())[:20]) & set(list(ritual_pmi.keys())[:20])
        ),
        "admin_unique_partners": list(
            set(list(admin_pmi.keys())[:20]) - set(list(ritual_pmi.keys())[:20])
        ),
        "ritual_unique_partners": list(
            set(list(ritual_pmi.keys())[:20]) - set(list(admin_pmi.keys())[:20])
        ),
        "ritual_record_details": ritual_record_details,
        "admin_context_examples": admin_examples,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
