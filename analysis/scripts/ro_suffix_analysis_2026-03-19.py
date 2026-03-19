"""
-RO Suffix Paradigm Analysis
Linear A Decipherment Project — 2026-03-19

H1: Tokens ending in -RO cluster in terminal positions within administrative records,
analogous to the confirmed behavior of KU-RO ("total"). If -RO is a productive
completive or aggregative suffix, non-KU/KI tokens ending in -RO should show the
same terminal positional bias.

Success threshold: ≥60% of -RO tokens appear at relative position ≥0.75 across ≥3 sites.

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/ro_suffix_analysis_2026-03-19.json
"""

import json
import re
import math
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/ro_suffix_analysis_2026-03-19.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "GRA2", "OLE2", "OLE3")
NUM_RE = re.compile(r"^\d+$|^[¼½¾⅐-⅟]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈", "|", "//"}

# Known -RO formulas to isolate
KNOWN_RO_FORMULAS = {"KU-RO", "KI-RO"}

ADMIN_SUPPORTS = {"tablet", "nodule", "roundel", "clay vessel", "lame", "label"}
RITUAL_SUPPORTS = {"stone vessel", "metal object", "architecture", "ivory object"}


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


def is_logogram(token):
    if token in KNOWN_LOGOGRAMS:
        return True
    for prefix in LOGOGRAM_PREFIXES:
        if token.startswith(prefix):
            return True
    if re.match(r"^[A-Z]{2,5}$", token) and "+" not in token:
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_multisyllable_word(token):
    if is_numeral(token) or is_logogram(token) or is_punct(token):
        return False
    if "-" not in token or "+" in token:
        return False
    return True


def ends_in_ro(token):
    return token.upper().endswith("-RO")


def get_content_tokens(tokens):
    """Return only meaningful (non-punct, non-numeral) tokens with their indices."""
    result = []
    for i, tok in enumerate(tokens):
        if not is_punct(tok) and not is_numeral(tok):
            result.append((i, tok))
    return result


def analyze_ro_positional(records):
    """
    For every multi-syllable token ending in -RO, compute its relative position
    within the inscription's content token sequence.
    """
    ro_data = []          # list of dicts with token info
    baseline_data = []    # same for non-RO multi-syllable tokens

    for r in records:
        raw_tokens = get_tokens(r)
        content = get_content_tokens(raw_tokens)
        n = len(content)
        if n == 0:
            continue

        site = r.get("site") or "unknown"
        support = r.get("support") or "unknown"
        record_id = r.get("id", "")

        for pos_in_content, (raw_idx, tok) in enumerate(content):
            if not is_multisyllable_word(tok):
                continue

            rel_pos = pos_in_content / max(n - 1, 1)  # 0.0 = first, 1.0 = last

            # Check if followed by a numeral (in raw token list)
            followed_by_numeral = False
            if raw_idx + 1 < len(raw_tokens):
                followed_by_numeral = is_numeral(raw_tokens[raw_idx + 1])

            # Check if followed by a logogram
            followed_by_logogram = False
            if raw_idx + 1 < len(raw_tokens):
                followed_by_logogram = is_logogram(raw_tokens[raw_idx + 1])

            entry = {
                "token": tok,
                "record_id": record_id,
                "site": site,
                "support": support,
                "relative_position": round(rel_pos, 3),
                "is_terminal": rel_pos >= 0.75,
                "is_final": pos_in_content == n - 1,
                "followed_by_numeral": followed_by_numeral,
                "followed_by_logogram": followed_by_logogram,
            }

            if ends_in_ro(tok):
                ro_data.append(entry)
            else:
                baseline_data.append(entry)

    return ro_data, baseline_data


def summarize_ro_tokens(ro_data):
    """Break down -RO tokens by formula class and compute statistics."""
    known_formulas = defaultdict(list)   # KU-RO, KI-RO
    other_ro = []

    for entry in ro_data:
        tok = entry["token"].upper()
        if tok in KNOWN_RO_FORMULAS:
            known_formulas[tok].append(entry)
        else:
            other_ro.append(entry)

    return known_formulas, other_ro


def compute_positional_stats(entries):
    if not entries:
        return {}
    rel_positions = [e["relative_position"] for e in entries]
    terminal_count = sum(1 for e in entries if e["is_terminal"])
    final_count = sum(1 for e in entries if e["is_final"])
    followed_by_num = sum(1 for e in entries if e["followed_by_numeral"])
    return {
        "count": len(entries),
        "terminal_rate": round(terminal_count / len(entries), 3),
        "final_token_rate": round(final_count / len(entries), 3),
        "followed_by_numeral_rate": round(followed_by_num / len(entries), 3),
        "mean_relative_position": round(sum(rel_positions) / len(rel_positions), 3),
        "median_relative_position": round(
            sorted(rel_positions)[len(rel_positions) // 2], 3
        ),
    }


def group_other_ro_by_token(other_ro):
    """Group non-formula -RO tokens by their token value for frequency analysis."""
    by_token = defaultdict(list)
    for entry in other_ro:
        by_token[entry["token"].upper()].append(entry)

    result = []
    for tok, entries in sorted(by_token.items(), key=lambda x: -len(x[1])):
        sites = set(e["site"] for e in entries)
        supports = Counter(e["support"] for e in entries)
        stats = compute_positional_stats(entries)
        stats["sites"] = sorted(sites)
        stats["site_count"] = len(sites)
        stats["support_distribution"] = dict(supports)
        result.append({"token": tok, **stats})
    return result


def get_contexts(ro_data, records_by_id, window=2):
    """For each -RO token, get the surrounding inscription context."""
    contexts = {}
    for entry in ro_data:
        tok = entry["token"].upper()
        rid = entry["record_id"]
        if rid in records_by_id:
            rec_tokens = get_tokens(records_by_id[rid])
            # Find this token in the list
            try:
                idx = next(
                    i for i, t in enumerate(rec_tokens)
                    if t.upper() == tok.upper()
                )
                left = rec_tokens[max(0, idx - window):idx]
                right = rec_tokens[idx + 1:idx + 1 + window]
                if tok not in contexts:
                    contexts[tok] = []
                contexts[tok].append({
                    "left": left,
                    "right": right,
                    "record_id": rid,
                    "site": entry["site"],
                })
            except StopIteration:
                pass
    return contexts


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    records_by_id = {r.get("id", ""): r for r in records}

    print("Analyzing -RO token positions...")
    ro_data, baseline_data = analyze_ro_positional(records)
    print(f"  Found {len(ro_data)} -RO token occurrences")
    print(f"  Found {len(baseline_data)} baseline multi-syllable token occurrences")

    known_formulas, other_ro = summarize_ro_tokens(ro_data)

    # Positional stats for each group
    kuro_stats = compute_positional_stats(known_formulas.get("KU-RO", []))
    kiro_stats = compute_positional_stats(known_formulas.get("KI-RO", []))
    other_ro_stats = compute_positional_stats(other_ro)
    baseline_stats = compute_positional_stats(baseline_data)

    print(f"\nKU-RO positional stats: {kuro_stats}")
    print(f"KI-RO positional stats: {kiro_stats}")
    print(f"Other -RO positional stats: {other_ro_stats}")
    print(f"Baseline (non-RO) positional stats: terminal_rate={baseline_stats.get('terminal_rate', 'N/A')}")

    # H1 evaluation
    threshold = 0.60
    other_terminal_rate = other_ro_stats.get("terminal_rate", 0)
    baseline_terminal_rate = baseline_stats.get("terminal_rate", 0)
    other_sites = set(e["site"] for e in other_ro)

    h1_result = "INCONCLUSIVE"
    if other_ro_stats.get("count", 0) < 5:
        h1_result = "INCONCLUSIVE — insufficient non-formula -RO tokens"
    elif other_terminal_rate >= threshold and len(other_sites) >= 3:
        h1_result = "SUPPORTED"
    elif other_terminal_rate < 0.45:
        h1_result = "FAILED — terminal rate below 45%"
    else:
        h1_result = f"PARTIALLY SUPPORTED — terminal rate {other_terminal_rate:.1%}, threshold {threshold:.0%}"

    print(f"\nH1 result: {h1_result}")
    print(f"  Other -RO terminal rate: {other_terminal_rate:.1%}")
    print(f"  Baseline terminal rate: {baseline_terminal_rate:.1%}")
    print(f"  Other -RO sites: {len(other_sites)}")

    # Token-level breakdown for non-formula -RO tokens
    token_breakdown = group_other_ro_by_token(other_ro)
    print(f"\nTop non-formula -RO tokens:")
    for t in token_breakdown[:10]:
        print(
            f"  {t['token']}: {t['count']} occ, {t['site_count']} sites, "
            f"terminal_rate={t['terminal_rate']:.1%}"
        )

    # Get contexts for top tokens
    contexts = get_contexts(ro_data, records_by_id)

    # Admin vs ritual breakdown for -RO tokens
    admin_ro = [e for e in ro_data if e["support"] in ADMIN_SUPPORTS]
    ritual_ro = [e for e in ro_data if e["support"] in RITUAL_SUPPORTS]
    admin_ro_stats = compute_positional_stats(admin_ro)
    ritual_ro_stats = compute_positional_stats(ritual_ro)

    output = {
        "analysis": "H1: -RO Suffix Positional Analysis",
        "date": "2026-03-19",
        "corpus_size": len(records),
        "total_ro_occurrences": len(ro_data),
        "total_baseline_occurrences": len(baseline_data),
        "hypothesis_result": h1_result,
        "success_threshold": threshold,
        "positional_stats": {
            "KU-RO": {"count": len(known_formulas.get("KU-RO", [])), **kuro_stats},
            "KI-RO": {"count": len(known_formulas.get("KI-RO", [])), **kiro_stats},
            "other_ro_tokens": {"count": len(other_ro), **other_ro_stats},
            "baseline_non_ro": {"count": len(baseline_data), **baseline_stats},
            "admin_ro_tokens": {"count": len(admin_ro), **admin_ro_stats},
            "ritual_ro_tokens": {"count": len(ritual_ro), **ritual_ro_stats},
        },
        "other_ro_sites": sorted(other_sites),
        "other_ro_site_count": len(other_sites),
        "token_breakdown": token_breakdown[:30],
        "token_contexts": {
            tok: ctxs[:5] for tok, ctxs in contexts.items()
            if tok not in KNOWN_RO_FORMULAS
        },
        "known_formula_data": {
            formula: [
                {"token": e["token"], "site": e["site"], "relative_position": e["relative_position"]}
                for e in entries[:20]
            ]
            for formula, entries in known_formulas.items()
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
