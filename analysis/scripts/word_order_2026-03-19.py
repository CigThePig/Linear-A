#!/usr/bin/env python3
"""
Word-Order Analysis for Ergative Hypothesis
Linear A Decipherment Project — 2026-03-19

Purpose: Test H4 — Linear A administrative inscriptions show SOV word order where
suffix -RE tokens (proposed active participle/agent) appear BEFORE commodity logograms,
and suffix -JA tokens (proposed absolutive) appear AFTER logograms.

Also tests: Does KI-RO appear pre- or post-logogram? Is there evidence for a
systematic relationship between suffix identity and position relative to logograms?

Evidence tier: Tier 5 (Grammatical) — Low-Medium confidence at best.
"""

import json
import re
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/word_order_2026-03-19.json"

# Commodity logograms (the pivotal elements in accounting inscriptions)
COMMODITY_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "OVI", "BOS", "EQU", "SUS", "CAP", "TELA", "LANA", "AES",
    "GRA+KU", "GRA+E", "GRA+PA", "GRA+SI", "GRA+TE",
    "OLIV+E", "OLIV+A", "OLIV+KU",
}

NUMERAL_RE = re.compile(r'^[\d/.,½⅓¼⅕]+$')
STRIP_TOKENS = {"𐄁", "↵", "\n", "", " "}

# Administrative support types
ADMIN_SUPPORTS = {
    "Tablet", "tablet",
    "Nodule", "nodule",
    "Roundel", "roundel",
    "Clay vessel", "clay vessel",
}


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def is_admin(record):
    return record.get("support", "") in ADMIN_SUPPORTS


def get_token_values(rec):
    """Extract string values from token dicts."""
    raw = rec.get("transliteration_tokens", [])
    return [t.get("value", "") if isinstance(t, dict) else str(t) for t in raw]


def clean_tokens(tokens):
    return [t for t in tokens if t not in STRIP_TOKENS and t]


def is_numeral(token):
    return bool(NUMERAL_RE.match(str(token)))


def is_logogram(token):
    return token in COMMODITY_LOGOGRAMS


def extract_suffix(token):
    """Extract the final syllable of a multi-sign token (the suffix)."""
    if not isinstance(token, str):
        return None
    parts = token.split("-")
    if len(parts) >= 2:
        return "-".join(parts[-1:])  # Last syllable
    return None


def is_syllabic(token):
    if not token or token in STRIP_TOKENS:
        return False
    if token in COMMODITY_LOGOGRAMS:
        return False
    if is_numeral(token):
        return False
    return True


def analyze_logogram_neighbors(records):
    """
    For each logogram occurrence in administrative inscriptions, record:
    - The token immediately preceding the logogram (pre-logogram slot)
    - The token immediately following the logogram (post-logogram slot)
    - The suffix of each neighboring token
    """
    pre_logogram_tokens = []
    post_logogram_tokens = []
    pre_logogram_suffixes = Counter()
    post_logogram_suffixes = Counter()

    logogram_contexts = []

    for rec in records:
        if not is_admin(rec):
            continue

        tokens = clean_tokens(get_token_values(rec))
        if not tokens:
            continue

        # Find each logogram position
        for i, token in enumerate(tokens):
            if not is_logogram(token):
                continue

            # Pre-logogram token: the syllabic token immediately before the logogram
            pre_token = None
            for j in range(i - 1, -1, -1):
                if tokens[j] in STRIP_TOKENS:
                    continue
                if is_syllabic(tokens[j]):
                    pre_token = tokens[j]
                    break
                elif is_logogram(tokens[j]) or is_numeral(tokens[j]):
                    break  # Don't cross another boundary

            # Post-logogram token: first token after the logogram (skip numerals to find next syllabic)
            post_token = None
            for j in range(i + 1, len(tokens)):
                if tokens[j] in STRIP_TOKENS:
                    continue
                if is_numeral(tokens[j]):
                    continue  # Skip numerals following the logogram
                if is_syllabic(tokens[j]):
                    post_token = tokens[j]
                    break
                elif is_logogram(tokens[j]):
                    break

            if pre_token or post_token:
                pre_suffix = extract_suffix(pre_token) if pre_token else None
                post_suffix = extract_suffix(post_token) if post_token else None

                logogram_contexts.append({
                    "record_id": rec.get("id", "?"),
                    "site": rec.get("site", "?"),
                    "logogram": token,
                    "pre_token": pre_token,
                    "pre_suffix": pre_suffix,
                    "post_token": post_token,
                    "post_suffix": post_suffix,
                })

                if pre_token:
                    pre_logogram_tokens.append(pre_token)
                    if pre_suffix:
                        pre_logogram_suffixes[pre_suffix] += 1

                if post_token:
                    post_logogram_tokens.append(post_token)
                    if post_suffix:
                        post_logogram_suffixes[post_suffix] += 1

    return logogram_contexts, pre_logogram_suffixes, post_logogram_suffixes


def analyze_kiro_position(records):
    """Test whether KI-RO appears pre- or post-logogram."""
    kiro_positions = []
    kuro_positions = []

    for rec in records:
        if not is_admin(rec):
            continue
        tokens = clean_tokens(get_token_values(rec))

        # Find KI-RO and KU-RO positions relative to logograms
        logogram_positions = [i for i, t in enumerate(tokens) if is_logogram(t)]

        for i, token in enumerate(tokens):
            if token not in ("KI-RO", "KU-RO"):
                continue

            if not logogram_positions:
                continue

            # Find nearest logogram
            nearest_pre = max([p for p in logogram_positions if p < i], default=None)
            nearest_post = min([p for p in logogram_positions if p > i], default=None)

            position = None
            if nearest_pre is not None and nearest_post is None:
                position = "post_logogram"
            elif nearest_post is not None and nearest_pre is None:
                position = "pre_logogram"
            elif nearest_pre is not None and nearest_post is not None:
                # Closer to which?
                if i - nearest_pre <= nearest_post - i:
                    position = "post_logogram"  # Closer to preceding logogram = after it
                else:
                    position = "pre_logogram"  # Closer to next logogram = before it
            else:
                position = "no_logogram_nearby"

            entry = {
                "record_id": rec.get("id", "?"),
                "site": rec.get("site", "?"),
                "token": token,
                "position_in_inscription": i,
                "nearest_pre_logogram": nearest_pre,
                "nearest_post_logogram": nearest_post,
                "relative_position": position,
                "context": tokens[max(0, i - 2):i + 3],
            }

            if token == "KI-RO":
                kiro_positions.append(entry)
            else:
                kuro_positions.append(entry)

    return kiro_positions, kuro_positions


def build_suffix_position_matrix(logogram_contexts):
    """Build a matrix: suffix × position (pre/post logogram)."""
    matrix = defaultdict(lambda: {"pre": 0, "post": 0})

    for ctx in logogram_contexts:
        if ctx["pre_suffix"]:
            matrix[ctx["pre_suffix"]]["pre"] += 1
        if ctx["post_suffix"]:
            matrix[ctx["post_suffix"]]["post"] += 1

    return matrix


def compute_position_bias(matrix):
    """For each suffix, compute its pre/post logogram bias."""
    results = []
    for suffix, counts in matrix.items():
        pre = counts["pre"]
        post = counts["post"]
        total = pre + post
        if total < 3:
            continue
        pre_rate = pre / total
        post_rate = post / total
        results.append({
            "suffix": suffix,
            "pre_logogram_count": pre,
            "post_logogram_count": post,
            "total": total,
            "pre_rate": round(pre_rate, 3),
            "post_rate": round(post_rate, 3),
            "position_bias": "pre_dominant" if pre_rate > 0.6 else
                             "post_dominant" if post_rate > 0.6 else "neutral",
        })
    return sorted(results, key=lambda x: -x["total"])


def run():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"  Loaded {len(records)} records")

    admin_records = [r for r in records if is_admin(r)]
    print(f"  Administrative records: {len(admin_records)}")

    print("\nAnalyzing logogram neighbor positions...")
    logogram_contexts, pre_suffixes, post_suffixes = analyze_logogram_neighbors(records)
    print(f"  Logogram contexts found: {len(logogram_contexts)}")
    print(f"  Distinct pre-logogram suffixes: {len(pre_suffixes)}")
    print(f"  Distinct post-logogram suffixes: {len(post_suffixes)}")

    print("\nBuilding suffix position matrix...")
    matrix = build_suffix_position_matrix(logogram_contexts)
    position_bias = compute_position_bias(matrix)

    print("\nTop suffix position biases:")
    for item in position_bias[:15]:
        print(f"  -{item['suffix']:6s}: pre={item['pre_rate']:.2f} post={item['post_rate']:.2f} "
              f"n={item['total']:3d}  bias={item['position_bias']}")

    print("\nAnalyzing KI-RO and KU-RO positions...")
    kiro_positions, kuro_positions = analyze_kiro_position(records)

    kiro_pre = sum(1 for k in kiro_positions if k["relative_position"] == "pre_logogram")
    kiro_post = sum(1 for k in kiro_positions if k["relative_position"] == "post_logogram")
    kuro_pre = sum(1 for k in kuro_positions if k["relative_position"] == "pre_logogram")
    kuro_post = sum(1 for k in kuro_positions if k["relative_position"] == "post_logogram")

    print(f"  KI-RO: pre_logogram={kiro_pre}, post_logogram={kiro_post} (n={len(kiro_positions)})")
    print(f"  KU-RO: pre_logogram={kuro_pre}, post_logogram={kuro_post} (n={len(kuro_positions)})")

    # Key suffixes of interest
    key_suffixes = ["-JA", "-RE", "-NA", "-TE", "-RO", "-ME", "-TI"]
    key_suffix_analysis = []
    for suffix_str in key_suffixes:
        suffix = suffix_str.lstrip("-")
        if suffix in matrix:
            counts = matrix[suffix]
            total = counts["pre"] + counts["post"]
            pre_rate = counts["pre"] / total if total > 0 else 0
            key_suffix_analysis.append({
                "suffix": f"-{suffix}",
                "pre_logogram": counts["pre"],
                "post_logogram": counts["post"],
                "total": total,
                "pre_rate": round(pre_rate, 3),
                "post_rate": round(1 - pre_rate, 3),
                "note": (
                    "Pre-dominant: consistent with AGENT/TOPIC before logogram (SOV ergative)"
                    if pre_rate > 0.6 else
                    "Post-dominant: consistent with ABSOLUTIVE/PATIENT after logogram"
                    if pre_rate < 0.4 else
                    "Neutral: no strong position preference"
                ),
            })
        else:
            key_suffix_analysis.append({
                "suffix": f"-{suffix}",
                "pre_logogram": 0,
                "post_logogram": 0,
                "total": 0,
                "pre_rate": None,
                "post_rate": None,
                "note": "Not found in logogram neighbor positions (n < 3)",
            })

    print("\nKey suffix position analysis:")
    for item in key_suffix_analysis:
        if item["total"] and item["total"] > 0:
            print(f"  {item['suffix']:6s}: pre={item['pre_rate']:.2f} post={item['post_rate']:.2f} "
                  f"n={item['total']:3d}")

    # H4 verdict
    ja_item = next((x for x in key_suffix_analysis if x["suffix"] == "-JA"), None)
    re_item = next((x for x in key_suffix_analysis if x["suffix"] == "-RE"), None)

    h4_verdict = "INCONCLUSIVE"
    if ja_item and re_item and ja_item["total"] >= 5 and re_item["total"] >= 5:
        ja_post = ja_item.get("post_rate", 0) or 0
        re_pre = re_item.get("pre_rate", 0) or 0
        if ja_post > 0.6 and re_pre > 0.6:
            h4_verdict = "SOV SUPPORTED — -JA post-logogram, -RE pre-logogram"
        elif ja_post > 0.5 and re_pre > 0.5:
            h4_verdict = "WEAKLY SUPPORTED — mild SOV tendency"
        else:
            h4_verdict = "NOT SUPPORTED — no clear SOV word order signal"
    elif ja_item and ja_item["total"] < 5:
        h4_verdict = "INSUFFICIENT DATA — too few logogram-neighbor occurrences"

    print(f"\nH4 verdict: {h4_verdict}")

    result = {
        "metadata": {
            "date": "2026-03-19",
            "analysis": "Word-order analysis for ergative hypothesis (H4)",
            "corpus_records": len(records),
            "admin_records": len(admin_records),
            "logogram_contexts_found": len(logogram_contexts),
            "evidence_tier": "Tier 5 (Grammatical) — Low-Medium confidence at best",
        },
        "key_suffix_position_analysis": key_suffix_analysis,
        "h4_verdict": h4_verdict,
        "kiro_kuro_position": {
            "KI-RO": {
                "total": len(kiro_positions),
                "pre_logogram": kiro_pre,
                "post_logogram": kiro_post,
                "pre_rate": round(kiro_pre / len(kiro_positions), 3) if kiro_positions else 0,
                "interpretation": (
                    "KI-RO predominantly POST-logogram — closing formula (known)"
                    if kiro_post > kiro_pre else
                    "KI-RO predominantly PRE-logogram — unexpected, possible relational word"
                    if kiro_pre > kiro_post else
                    "KI-RO distributed evenly — context-dependent"
                ),
            },
            "KU-RO": {
                "total": len(kuro_positions),
                "pre_logogram": kuro_pre,
                "post_logogram": kuro_post,
                "pre_rate": round(kuro_pre / len(kuro_positions), 3) if kuro_positions else 0,
            },
        },
        "full_suffix_position_matrix": position_bias,
        "pre_logogram_suffix_frequencies": dict(pre_suffixes.most_common(20)),
        "post_logogram_suffix_frequencies": dict(post_suffixes.most_common(20)),
        "sample_logogram_contexts": logogram_contexts[:30],
        "kiro_occurrences": kiro_positions,
        "kuro_occurrences": kuro_positions,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {OUTPUT_PATH}")
    return result


if __name__ == "__main__":
    run()
