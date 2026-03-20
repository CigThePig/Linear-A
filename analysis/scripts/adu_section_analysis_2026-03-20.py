"""
H8b: A-DU Administrative Section Marker Analysis
H8d: PO-TO- Prefix Cross-Site Sweep
Linear A Decipherment Project — 2026-03-20

H8b Hypothesis: A-DU is an administrative section header/initiator word that
appears record-initial (≥70%) and introduces logogram+numeral accounting blocks.

H8d Hypothesis: PO-TO-KU-RO ("grand total") appears at ≥1 non-HT sites, or
remains HT-specific (downgrade confidence if HT-only).

Falsification conditions:
- H8b FAILS if A-DU is record-initial in <70% of cases OR post-A-DU tokens are
  not logogram/numeral enriched (>2x baseline rate).
- H8d FAILS if PO-TO-KU-RO appears at 0 non-HT sites.

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/adu_section_2026-03-20.json
"""

import json
import re
import math
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/adu_section_2026-03-20.json")

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
    raw = record.get("transliteration_tokens", [])
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
    if re.match(r"^[A-Z]{2,4}$", token) and token not in {"JA", "SA", "NA", "DA", "TA", "MA", "RA", "DU"}:
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


def compute_baseline_token_class_distribution(records):
    """Compute the overall distribution of token classes across all records."""
    dist = Counter()
    total = 0
    for r in records:
        for tok in get_tokens(r):
            cls = classify_token(tok)
            dist[cls] += 1
            total += 1
    return dist, total


def analyze_adu(records):
    target = "A-DU"

    # Records containing A-DU
    target_records = []
    for r in records:
        tokens = get_tokens(r)
        if target in tokens:
            target_records.append((r, tokens))

    if not target_records:
        return {"error": f"{target} not found in corpus"}

    # Baseline token class distribution
    baseline_dist, baseline_total = compute_baseline_token_class_distribution(records)
    baseline_rates = {cls: cnt / baseline_total for cls, cnt in baseline_dist.items()}

    # Per-occurrence analysis
    occurrences = []
    sites = Counter()
    support_types = Counter()
    record_initial_count = 0
    post_window_classes = Counter()  # Classes of tokens in positions +1 to +5 after A-DU
    post_window_tokens = Counter()
    logograms_following = Counter()
    kuro_cooccurrence = 0
    kiro_cooccurrence = 0

    for r, tokens in target_records:
        site = r.get("site", "Unknown")
        support = r.get("support", "Unknown")
        sites[site] += 1
        support_types[support] += 1

        has_kuro = "KU-RO" in tokens
        has_kiro = "KI-RO" in tokens
        if has_kuro:
            kuro_cooccurrence += 1
        if has_kiro:
            kiro_cooccurrence += 1

        for i, tok in enumerate(tokens):
            if tok == target:
                is_initial = (i == 0)
                if is_initial:
                    record_initial_count += 1

                # Capture 5 tokens after A-DU
                window = tokens[i + 1: i + 6]
                for wt in window:
                    cls = classify_token(wt)
                    post_window_classes[cls] += 1
                    post_window_tokens[wt] += 1
                    if cls == "logogram":
                        logograms_following[wt] += 1

                # Pre-token
                pre = tokens[i - 1] if i > 0 else None
                pre_class = classify_token(pre) if pre else "start"

                occurrences.append({
                    "id": r.get("id"),
                    "site": site,
                    "support": support,
                    "position": i,
                    "is_record_initial": is_initial,
                    "pre_token": pre,
                    "pre_class": pre_class,
                    "post_window": window,
                    "has_kuro": has_kuro,
                    "has_kiro": has_kiro,
                })

    total_occ = len(occurrences)
    record_initial_rate = record_initial_count / total_occ if total_occ else 0

    # Compute enrichment ratios for post-window
    post_total = sum(post_window_classes.values())
    enrichment = {}
    for cls in ["logogram", "numeral", "formula", "syllabic", "punct"]:
        observed = post_window_classes.get(cls, 0) / post_total if post_total else 0
        base = baseline_rates.get(cls, 0)
        enrichment[cls] = round(observed / base, 2) if base > 0 else 0

    # Non-HT sites
    non_ht_sites = {k: v for k, v in sites.items() if k != "Haghia Triada"}

    # Thresholds
    passed_initial = record_initial_rate >= 0.70
    passed_enrichment = enrichment.get("logogram", 0) > 2.0 or enrichment.get("numeral", 0) > 2.0
    passed_sites = len(non_ht_sites) >= 1  # at least 1 non-HT site
    hypothesis_supported = passed_initial and passed_enrichment and passed_sites

    return {
        "target_token": target,
        "records_containing_adu": len(target_records),
        "total_occurrences": total_occ,
        "site_distribution": dict(sites),
        "non_ht_sites": non_ht_sites,
        "support_type_distribution": dict(support_types),
        "record_initial_count": record_initial_count,
        "record_initial_rate": round(record_initial_rate, 3),
        "post_window_class_distribution": dict(post_window_classes),
        "post_window_top_tokens": dict(post_window_tokens.most_common(15)),
        "top_logograms_following": dict(logograms_following.most_common(10)),
        "kuro_cooccurrence": kuro_cooccurrence,
        "kiro_cooccurrence": kiro_cooccurrence,
        "enrichment_ratios_vs_baseline": enrichment,
        "baseline_class_rates": {k: round(v, 3) for k, v in baseline_rates.items()},
        "hypothesis_assessment": {
            "threshold_record_initial_ge_70pct": passed_initial,
            "threshold_logogram_numeral_enrichment_gt_2x": passed_enrichment,
            "threshold_non_ht_sites_ge_1": passed_sites,
            "hypothesis_supported": hypothesis_supported,
        },
        "all_occurrences": occurrences,
    }


def analyze_poto(records):
    """H8d: Cross-site sweep for all PO-TO- prefixed tokens."""
    poto_tokens = Counter()
    poto_sites = defaultdict(Counter)
    poto_support = defaultdict(Counter)
    poto_positions = defaultdict(list)

    for r in records:
        tokens = get_tokens(r)
        site = r.get("site", "Unknown")
        support = r.get("support", "Unknown")
        for i, tok in enumerate(tokens):
            if tok.startswith("PO-TO-") or tok == "PO-TO":
                poto_tokens[tok] += 1
                poto_sites[tok][site] += 1
                poto_support[tok][support] += 1
                poto_positions[tok].append({
                    "id": r.get("id"),
                    "site": site,
                    "support": support,
                    "position": i,
                    "token_count": len(tokens),
                    "pre": tokens[i - 1] if i > 0 else None,
                    "post": tokens[i + 1] if i + 1 < len(tokens) else None,
                })

    result = {}
    for tok, count in poto_tokens.items():
        site_dist = dict(poto_sites[tok])
        non_ht = {k: v for k, v in site_dist.items() if k != "Haghia Triada"}
        result[tok] = {
            "total_occurrences": count,
            "site_distribution": site_dist,
            "non_ht_occurrences": sum(non_ht.values()),
            "non_ht_sites": non_ht,
            "support_types": dict(poto_support[tok]),
            "all_occurrences": poto_positions[tok],
        }

    # H8d assessment
    poto_kuro = result.get("PO-TO-KU-RO", {})
    h8d_passed = poto_kuro.get("non_ht_occurrences", 0) >= 1

    return {
        "all_poto_tokens": result,
        "h8d_assessment": {
            "poto_kuro_found": "PO-TO-KU-RO" in result,
            "poto_kuro_non_ht_occurrences": poto_kuro.get("non_ht_occurrences", 0),
            "poto_kuro_non_ht_sites": poto_kuro.get("non_ht_sites", {}),
            "hypothesis_supported": h8d_passed,
        },
    }


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records.")

    print("Analyzing A-DU (H8b)...")
    adu_results = analyze_adu(records)

    print("Analyzing PO-TO- prefix sweep (H8d)...")
    poto_results = analyze_poto(records)

    combined = {
        "h8b_adu": adu_results,
        "h8d_poto": poto_results,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {OUTPUT_PATH}")

    # Print summary
    print("\n=== A-DU SECTION ANALYSIS (H8b) ===")
    print(f"Records containing A-DU: {adu_results.get('records_containing_adu', 0)}")
    print(f"Total occurrences: {adu_results.get('total_occurrences', 0)}")
    print(f"Site distribution: {adu_results.get('site_distribution', {})}")
    print(f"Non-HT sites: {adu_results.get('non_ht_sites', {})}")
    print(f"Record-initial rate: {adu_results.get('record_initial_rate', 0):.1%} (threshold: ≥70%)")
    print(f"Post-window class distribution: {adu_results.get('post_window_class_distribution', {})}")
    print(f"Enrichment vs baseline: {adu_results.get('enrichment_ratios_vs_baseline', {})}")
    print(f"Top post-window tokens: {adu_results.get('post_window_top_tokens', {})}")
    print(f"Top logograms following: {adu_results.get('top_logograms_following', {})}")
    print(f"H8b hypothesis assessment: {adu_results.get('hypothesis_assessment', {})}")
    verdict_b = adu_results.get("hypothesis_assessment", {}).get("hypothesis_supported", False)
    print(f"\n{'✓ H8b SUPPORTED' if verdict_b else '✗ H8b FAILED/INCONCLUSIVE'}")

    print("\n=== PO-TO- PREFIX SWEEP (H8d) ===")
    poto_all = poto_results.get("all_poto_tokens", {})
    for tok, data in poto_all.items():
        print(f"  {tok}: {data['total_occurrences']} total, sites: {data['site_distribution']}")
    print(f"H8d assessment: {poto_results.get('h8d_assessment', {})}")
    verdict_d = poto_results.get("h8d_assessment", {}).get("hypothesis_supported", False)
    print(f"\n{'✓ H8d SUPPORTED' if verdict_d else '✗ H8d FAILED'}")


if __name__ == "__main__":
    main()
