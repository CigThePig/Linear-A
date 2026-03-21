"""
H8a: Sign *304 Logogram Analysis
Linear A Decipherment Project — 2026-03-20

Hypothesis: *304 functions as a logogram appearing immediately before numerals,
in the same structural slot as GRA, VIN, OLE (commodity logograms).

Falsification: FAIL if *304 appears after numerals OR co-occurs with KU-RO/KI-RO
in >20% of cases.

Success threshold: *304 followed by numeral in ≥70% of cases AND appears at ≥2 sites

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/sign304_logogram_2026-03-20.json
"""

import json
import re
import math
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/sign304_logogram_2026-03-20.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "LUNA",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2", "GRA3")
FORMULA_TOKENS = {"KU-RO", "KI-RO", "PO-TO-KU-RO"}

NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈", "|", "·"}


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_tokens(record):
    """Return list of token values (excluding line-break markers)."""
    raw = record.get("transliteration_tokens", [])
    # Handle both list-of-dicts and list-of-strings
    result = []
    for t in raw:
        if isinstance(t, dict):
            if t.get("type") == "token":
                result.append(t["value"])
        elif isinstance(t, str):
            result.append(t)
    return result


def is_numeral(token):
    return bool(NUM_RE.match(token))


def is_logogram(token):
    if token in KNOWN_LOGOGRAMS:
        return True
    for prefix in LOGOGRAM_PREFIXES:
        if token.startswith(prefix):
            return True
    # Pure uppercase 2-4 chars
    if re.match(r"^[A-Z]{2,4}$", token) and token not in {"JA", "SA", "NA", "DA", "TA", "MA", "RA"}:
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\") or len(token) == 0


def classify_token(token):
    if is_numeral(token):
        return "numeral"
    if token in FORMULA_TOKENS:
        return "formula"
    if is_logogram(token):
        return "logogram"
    if is_punct(token):
        return "punct"
    return "syllabic"


def compute_pmi(count_ab, count_a, count_b, total):
    """Compute pointwise mutual information."""
    if count_ab == 0 or count_a == 0 or count_b == 0:
        return 0.0
    p_ab = count_ab / total
    p_a = count_a / total
    p_b = count_b / total
    return math.log2(p_ab / (p_a * p_b))


def analyze_sign304(records):
    target = "*304"

    # All records containing *304
    target_records = []
    for r in records:
        tokens = get_tokens(r)
        if target in tokens:
            target_records.append((r, tokens))

    if not target_records:
        return {"error": f"{target} not found in corpus"}

    # Per-occurrence analysis
    occurrences = []
    sites = Counter()
    support_types = Counter()
    post_token_classes = Counter()
    pre_token_classes = Counter()
    post_tokens = Counter()
    pre_tokens = Counter()
    formula_cooccurrence = 0
    kuro_cooccurrence = 0
    kiro_cooccurrence = 0

    for r, tokens in target_records:
        sites[r.get("site", "Unknown")] += 1
        support_types[r.get("support", "Unknown")] += 1
        has_kuro = "KU-RO" in tokens
        has_kiro = "KI-RO" in tokens
        if has_kuro or has_kiro:
            formula_cooccurrence += 1
        if has_kuro:
            kuro_cooccurrence += 1
        if has_kiro:
            kiro_cooccurrence += 1

        for i, tok in enumerate(tokens):
            if tok == target:
                post = tokens[i + 1] if i + 1 < len(tokens) else None
                pre = tokens[i - 1] if i > 0 else None

                post_class = classify_token(post) if post else "end"
                pre_class = classify_token(pre) if pre else "start"

                post_token_classes[post_class] += 1
                pre_token_classes[pre_class] += 1
                if post:
                    post_tokens[post] += 1
                if pre:
                    pre_tokens[pre] += 1

                occurrences.append({
                    "id": r.get("id"),
                    "site": r.get("site"),
                    "support": r.get("support"),
                    "position": i,
                    "token_count": len(tokens),
                    "pre_token": pre,
                    "post_token": post,
                    "pre_class": pre_class,
                    "post_class": post_class,
                    "has_kuro": has_kuro,
                    "has_kiro": has_kiro,
                })

    total_occ = len(occurrences)
    numeral_after_rate = post_token_classes.get("numeral", 0) / total_occ if total_occ else 0
    formula_cooccurrence_rate = formula_cooccurrence / len(target_records) if target_records else 0

    # Control: same stats for GRA, VIN, OLE
    control_stats = {}
    for control_sign in ["GRA", "VIN", "OLE"]:
        ctrl_occ = []
        ctrl_post = Counter()
        for r, tokens in [(r, get_tokens(r)) for r in records]:
            for i, tok in enumerate(tokens):
                if tok == control_sign:
                    post = tokens[i + 1] if i + 1 < len(tokens) else None
                    post_class = classify_token(post) if post else "end"
                    ctrl_post[post_class] += 1
                    ctrl_occ.append(1)
        total_ctrl = sum(ctrl_occ)
        control_stats[control_sign] = {
            "total_occurrences": total_ctrl,
            "numeral_after_rate": ctrl_post.get("numeral", 0) / total_ctrl if total_ctrl else 0,
            "post_class_distribution": dict(ctrl_post),
        }

    # PMI between *304 and known logograms.
    # Bug-fix note (2026-03-21): prior version mixed sample spaces:
    #   count_304  = total token occurrences (occurrence-level, =25)
    #   count_lgm  = sum of per-record token counts (occurrence-level)
    #   count_both = records containing both (record-level)
    #   denominator = len(records) (record-level)
    # This inconsistency distorts PMI when logograms appear multiple times per record
    # (e.g. GRA, which is very frequent). Fixed to use a fully record-level formulation:
    #   p(*304) = records containing *304 / total records
    #   p(lgm)  = records containing lgm  / total records
    #   p(*304, lgm) = records containing both / total records
    # This is the standard document-level PMI used in corpus linguistics.
    count_304_records = len(target_records)  # records containing *304 (not raw occurrences)
    pmi_with_logograms = {}
    for lgm in ["OLE", "OLIV", "GRA", "VIN", "VIR"]:
        count_lgm_records = sum(1 for r in records if lgm in get_tokens(r))
        count_both = sum(
            1 for r in records
            if target in get_tokens(r) and lgm in get_tokens(r)
        )
        pmi_with_logograms[lgm] = round(
            compute_pmi(count_both, count_304_records, count_lgm_records, len(records)), 3
        )

    # Assessment
    passed_numeral_threshold = numeral_after_rate >= 0.70
    passed_formula_threshold = formula_cooccurrence_rate <= 0.20
    passed_site_threshold = len(sites) >= 2
    hypothesis_supported = passed_numeral_threshold and passed_formula_threshold and passed_site_threshold

    return {
        "target_sign": target,
        "records_containing_304": len(target_records),
        "total_occurrences": total_occ,
        "site_distribution": dict(sites),
        "support_type_distribution": dict(support_types),
        "post_token_class_distribution": dict(post_token_classes),
        "pre_token_class_distribution": dict(pre_token_classes),
        "top_post_tokens": dict(post_tokens.most_common(10)),
        "top_pre_tokens": dict(pre_tokens.most_common(10)),
        "numeral_after_rate": round(numeral_after_rate, 3),
        "formula_cooccurrence_rate": round(formula_cooccurrence_rate, 3),
        "kuro_cooccurrence": kuro_cooccurrence,
        "kiro_cooccurrence": kiro_cooccurrence,
        "pmi_sample_space": "record_level",  # p(*304) and p(lgm) both use records-containing counts / total records
        "pmi_with_logograms": pmi_with_logograms,
        "control_logogram_stats": control_stats,
        "hypothesis_assessment": {
            "threshold_numeral_after_rate_70pct": passed_numeral_threshold,
            "threshold_formula_cooccurrence_le_20pct": passed_formula_threshold,
            "threshold_site_count_ge_2": passed_site_threshold,
            "hypothesis_supported": hypothesis_supported,
        },
        "all_occurrences": occurrences,
    }


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records.")

    print("Analyzing sign *304...")
    results = analyze_sign304(records)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {OUTPUT_PATH}")

    # Print summary
    print("\n=== SIGN *304 LOGOGRAM ANALYSIS ===")
    print(f"Records containing *304: {results.get('records_containing_304', 0)}")
    print(f"Total occurrences: {results.get('total_occurrences', 0)}")
    print(f"Site distribution: {results.get('site_distribution', {})}")
    print(f"Support types: {results.get('support_type_distribution', {})}")
    print(f"Post-token class distribution: {results.get('post_token_class_distribution', {})}")
    print(f"Numeral-after rate: {results.get('numeral_after_rate', 0):.1%} (threshold: ≥70%)")
    print(f"Formula co-occurrence rate: {results.get('formula_cooccurrence_rate', 0):.1%} (threshold: ≤20%)")
    print(f"Top post-tokens: {results.get('top_post_tokens', {})}")
    print(f"Top pre-tokens: {results.get('top_pre_tokens', {})}")
    print(f"PMI with logograms: {results.get('pmi_with_logograms', {})}")
    print("\nControl logogram numeral-after rates:")
    for lgm, stats in results.get("control_logogram_stats", {}).items():
        print(f"  {lgm}: {stats['numeral_after_rate']:.1%}")
    print(f"\nHypothesis assessment: {results.get('hypothesis_assessment', {})}")
    verdict = results.get("hypothesis_assessment", {}).get("hypothesis_supported", False)
    print(f"\n{'✓ H8a SUPPORTED' if verdict else '✗ H8a FAILED/INCONCLUSIVE'}")


if __name__ == "__main__":
    main()
