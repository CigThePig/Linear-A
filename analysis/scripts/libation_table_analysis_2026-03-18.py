"""
Libation Table Formula Analysis
Linear A Decipherment Project — 2026-03-18

Strategy 6: Analyze the ritual register (stone vessels, metal objects, architecture)
to map structural equivalences around the cross-site anchor JA-SA-SA-RA-ME.

Key hypotheses:
- JA-SA-SA-RA-ME is a liturgical formula appearing predominantly in ritual contexts
- Tokens in the same structural slot across multiple sites are structurally equivalent
- I-PI-NA-MA SI-RU-TE is a stable ritual bigram at cult sites

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/libation_analysis_2026-03-18.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/libation_analysis_2026-03-18.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")

NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈"}

# Ritual support types
RITUAL_SUPPORTS = {"stone vessel", "metal object", "architecture", "libation table"}
# Cult sites identified in prior analysis
CULT_SITES = {"Iouktas", "Kophinas", "Troullos", "Vrysinas", "Palaikastro"}

# Anchor sequences for ritual register
RITUAL_ANCHOR_1 = "JA-SA-SA-RA-ME"
RITUAL_ANCHOR_2_BIGRAM = ("I-PI-NA-MA", "SI-RU-TE")


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_tokens(record):
    """Return list of token values (excluding line breaks)."""
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
    if re.match(r"^[A-Z]{2,4}$", token):
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_formula_candidate(token):
    if is_numeral(token):
        return False
    if is_logogram(token):
        return False
    if is_punct(token):
        return False
    if len(token) < 2:
        return False
    return True


def analyze_ritual_corpus_composition(records):
    """
    Summarize ritual vs. administrative register composition.
    """
    support_counts = Counter()
    ritual_records = []
    admin_records = []

    for r in records:
        support = (r.get("support") or "").lower().strip()
        support_counts[support] += 1
        if any(rs in support for rs in RITUAL_SUPPORTS):
            ritual_records.append(r)
        else:
            admin_records.append(r)

    ritual_sites = Counter(r.get("site") for r in ritual_records)
    return {
        "total_records": len(records),
        "ritual_count": len(ritual_records),
        "admin_count": len(admin_records),
        "support_distribution": dict(support_counts.most_common()),
        "ritual_sites": dict(ritual_sites.most_common()),
        "ritual_records": ritual_records,
    }


def analyze_anchor_formula(records, anchor_token):
    """
    For every record containing anchor_token, extract:
    - support type, site, scribe
    - full token sequence
    - context window ±5 tokens around anchor
    - positional slot (which position in the inscription)
    """
    occurrences = []
    support_dist = Counter()
    site_dist = Counter()
    pre_tokens = Counter()   # tokens immediately before anchor (non-numeral, non-logogram)
    post_tokens = Counter()  # tokens immediately after anchor
    pre_all = Counter()      # any token in the 3-window before anchor
    post_all = Counter()     # any token in the 3-window after anchor

    for r in records:
        tokens = get_tokens(r)
        for i, tok in enumerate(tokens):
            if tok == anchor_token:
                support = (r.get("support") or "").lower().strip()
                site = r.get("site") or "unknown"
                support_dist[support] += 1
                site_dist[site] += 1

                pre = tokens[max(0, i - 5):i]
                post = tokens[i + 1:min(len(tokens), i + 5)]

                # Immediate neighbors (skip numerals and logograms for structural analysis)
                formula_pre = [t for t in pre if is_formula_candidate(t)]
                formula_post = [t for t in post if is_formula_candidate(t)]

                if formula_pre:
                    pre_tokens[formula_pre[-1]] += 1  # immediately before
                if formula_post:
                    post_tokens[formula_post[0]] += 1  # immediately after

                for t in formula_pre:
                    pre_all[t] += 1
                for t in formula_post:
                    post_all[t] += 1

                occurrences.append({
                    "record_id": r["id"],
                    "site": site,
                    "support": support,
                    "scribe": r.get("scribe"),
                    "anchor_position": i,
                    "total_tokens": len(tokens),
                    "tokens_before": pre,
                    "tokens_after": post,
                })

    # Structural slot analysis: for each token in pre/post position, count how many sites it appears at
    pre_sites = defaultdict(set)
    post_sites = defaultdict(set)
    for occ in occurrences:
        formula_pre = [t for t in occ["tokens_before"] if is_formula_candidate(t)]
        formula_post = [t for t in occ["tokens_after"] if is_formula_candidate(t)]
        if formula_pre:
            pre_sites[formula_pre[-1]].add(occ["site"])
        if formula_post:
            post_sites[formula_post[0]].add(occ["site"])

    pre_multisite = {
        tok: sorted(sites) for tok, sites in pre_sites.items()
        if len(sites) >= 2
    }
    post_multisite = {
        tok: sorted(sites) for tok, sites in post_sites.items()
        if len(sites) >= 2
    }

    return {
        "anchor": anchor_token,
        "total_occurrences": len(occurrences),
        "support_distribution": dict(support_dist.most_common()),
        "site_distribution": dict(site_dist.most_common()),
        "immediate_pre_tokens": dict(pre_tokens.most_common(20)),
        "immediate_post_tokens": dict(post_tokens.most_common(20)),
        "pre_window_tokens": dict(pre_all.most_common(20)),
        "post_window_tokens": dict(post_all.most_common(20)),
        "pre_multisite_tokens": pre_multisite,  # tokens before anchor that appear at ≥2 sites
        "post_multisite_tokens": post_multisite,  # tokens after anchor that appear at ≥2 sites
        "sample_occurrences": occurrences[:20],
    }


def analyze_ritual_bigram(records, token1, token2):
    """
    For every record containing the bigram (token1 followed by token2 within 5 tokens),
    extract context and support/site distribution.
    """
    occurrences = []
    support_dist = Counter()
    site_dist = Counter()
    companion_tokens = Counter()

    for r in records:
        tokens = get_tokens(r)
        for i in range(len(tokens) - 1):
            if tokens[i] == token1:
                # Look for token2 within the next 5 positions
                for j in range(i + 1, min(i + 6, len(tokens))):
                    if tokens[j] == token2:
                        support = (r.get("support") or "").lower().strip()
                        site = r.get("site") or "unknown"
                        support_dist[support] += 1
                        site_dist[site] += 1

                        context = tokens[max(0, i - 3):min(len(tokens), j + 4)]
                        for t in context:
                            if is_formula_candidate(t) and t not in (token1, token2):
                                companion_tokens[t] += 1

                        occurrences.append({
                            "record_id": r["id"],
                            "site": site,
                            "support": support,
                            "bigram_start": i,
                            "bigram_end": j,
                            "context": context,
                        })
                        break

    return {
        "bigram": f"{token1} {token2}",
        "total_occurrences": len(occurrences),
        "support_distribution": dict(support_dist.most_common()),
        "site_distribution": dict(site_dist.most_common()),
        "companion_tokens": dict(companion_tokens.most_common(20)),
        "sample_occurrences": occurrences,
    }


def find_ritual_exclusive_tokens(records):
    """
    Find tokens that appear EXCLUSIVELY or predominantly in ritual contexts.
    Token is "ritual-exclusive" if >80% of its occurrences are on ritual support types.
    """
    token_support_counts = defaultdict(lambda: {"ritual": 0, "admin": 0})

    for r in records:
        support = (r.get("support") or "").lower().strip()
        is_ritual = any(rs in support for rs in RITUAL_SUPPORTS)
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok):
                if is_ritual:
                    token_support_counts[tok]["ritual"] += 1
                else:
                    token_support_counts[tok]["admin"] += 1

    ritual_exclusive = {}
    for tok, counts in token_support_counts.items():
        total = counts["ritual"] + counts["admin"]
        if total >= 3:
            ritual_pct = counts["ritual"] / total
            if ritual_pct >= 0.8:
                ritual_exclusive[tok] = {
                    "ritual_count": counts["ritual"],
                    "admin_count": counts["admin"],
                    "total": total,
                    "ritual_pct": round(ritual_pct, 3),
                }

    # Sort by total occurrences
    return dict(sorted(ritual_exclusive.items(), key=lambda x: -x[1]["total"]))


def find_cult_site_formulas(records):
    """
    Find formulas that appear at ≥2 of the known cult sites.
    These are likely pan-Minoan liturgical formulas.
    """
    cult_records = [r for r in records if r.get("site") in CULT_SITES]

    # Bigrams at cult sites
    bigram_cult_sites = defaultdict(set)
    bigram_counts = Counter()

    for r in cult_records:
        tokens = get_tokens(r)
        candidates = [t for t in tokens if is_formula_candidate(t)]
        for i in range(len(candidates) - 1):
            bigram = f"{candidates[i]} {candidates[i+1]}"
            bigram_counts[bigram] += 1
            bigram_cult_sites[bigram].add(r.get("site"))

    multi_cult = {
        bigram: {
            "count": bigram_counts[bigram],
            "cult_sites": sorted(bigram_cult_sites[bigram]),
            "cult_site_count": len(bigram_cult_sites[bigram]),
        }
        for bigram in bigram_counts
        if len(bigram_cult_sites[bigram]) >= 2
    }

    return dict(sorted(multi_cult.items(), key=lambda x: -x[1]["cult_site_count"]))


def compare_ritual_vs_admin_suffixes(records):
    """
    Compare suffix distributions between ritual and administrative registers.
    If certain suffixes dominate the ritual register, they may carry ritual grammatical meaning.
    """
    ritual_suffix_counts = Counter()
    admin_suffix_counts = Counter()

    for r in records:
        support = (r.get("support") or "").lower().strip()
        is_ritual = any(rs in support for rs in RITUAL_SUPPORTS)
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok) and "-" in tok:
                parts = tok.split("-")
                final_syllable = parts[-1]
                if len(final_syllable) >= 2:
                    if is_ritual:
                        ritual_suffix_counts[final_syllable] += 1
                    else:
                        admin_suffix_counts[final_syllable] += 1

    # Compute ritual enrichment score: ritual_freq / (ritual_freq + admin_freq) normalized by register size
    ritual_total = sum(ritual_suffix_counts.values()) or 1
    admin_total = sum(admin_suffix_counts.values()) or 1

    enrichment = {}
    all_suffixes = set(ritual_suffix_counts.keys()) | set(admin_suffix_counts.keys())
    for suf in all_suffixes:
        r_count = ritual_suffix_counts.get(suf, 0)
        a_count = admin_suffix_counts.get(suf, 0)
        r_rate = r_count / ritual_total
        a_rate = a_count / admin_total
        if r_count + a_count >= 5:
            ratio = r_rate / (a_rate + 1e-9)
            enrichment[suf] = {
                "ritual_count": r_count,
                "admin_count": a_count,
                "ritual_rate": round(r_rate, 4),
                "admin_rate": round(a_rate, 4),
                "ritual_enrichment_ratio": round(ratio, 3),
            }

    return dict(sorted(enrichment.items(), key=lambda x: -x[1]["ritual_enrichment_ratio"]))


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    print("\n--- Ritual corpus composition ---")
    composition = analyze_ritual_corpus_composition(records)
    print(f"  Ritual register: {composition['ritual_count']} records")
    print(f"  Administrative register: {composition['admin_count']} records")
    print(f"  Ritual sites: {dict(list(composition['ritual_sites'].items())[:10])}")

    print(f"\n--- Analyzing anchor: {RITUAL_ANCHOR_1} ---")
    anchor1_analysis = analyze_anchor_formula(records, RITUAL_ANCHOR_1)
    print(f"  Total occurrences: {anchor1_analysis['total_occurrences']}")
    print(f"  Support distribution: {anchor1_analysis['support_distribution']}")
    print(f"  Sites: {anchor1_analysis['site_distribution']}")
    print(f"  Immediate pre-tokens (multi-site): {anchor1_analysis['pre_multisite_tokens']}")
    print(f"  Immediate post-tokens (multi-site): {anchor1_analysis['post_multisite_tokens']}")

    print(f"\n--- Analyzing ritual bigram: {RITUAL_ANCHOR_2_BIGRAM[0]} {RITUAL_ANCHOR_2_BIGRAM[1]} ---")
    bigram_analysis = analyze_ritual_bigram(records, RITUAL_ANCHOR_2_BIGRAM[0], RITUAL_ANCHOR_2_BIGRAM[1])
    print(f"  Total occurrences: {bigram_analysis['total_occurrences']}")
    print(f"  Support distribution: {bigram_analysis['support_distribution']}")
    print(f"  Sites: {bigram_analysis['site_distribution']}")

    print("\n--- Finding ritual-exclusive tokens ---")
    ritual_exclusive = find_ritual_exclusive_tokens(records)
    print(f"  Found {len(ritual_exclusive)} ritual-exclusive tokens (≥80% ritual, ≥3 occ)")
    for tok, data in list(ritual_exclusive.items())[:15]:
        print(f"    {tok}: {data['ritual_count']}/{data['total']} ritual ({data['ritual_pct']:.1%})")

    print("\n--- Finding cult-site-specific formulas ---")
    cult_formulas = find_cult_site_formulas(records)
    print(f"  Bigrams appearing at ≥2 cult sites: {len(cult_formulas)}")
    for bigram, data in list(cult_formulas.items())[:10]:
        print(f"    '{bigram}': count={data['count']}, sites={data['cult_sites']}")

    print("\n--- Comparing ritual vs. administrative suffix distributions ---")
    suffix_enrichment = compare_ritual_vs_admin_suffixes(records)
    print("  Top ritual-enriched suffixes:")
    for suf, data in list(suffix_enrichment.items())[:10]:
        print(f"    -{suf}: ritual={data['ritual_count']}, admin={data['admin_count']}, ratio={data['ritual_enrichment_ratio']:.2f}x")

    output = {
        "corpus_composition": {
            k: v for k, v in composition.items() if k != "ritual_records"
        },
        "anchor_JA_SA_SA_RA_ME": anchor1_analysis,
        "bigram_IPINAMA_SIRUTE": bigram_analysis,
        "ritual_exclusive_tokens": ritual_exclusive,
        "cult_site_formulas": cult_formulas,
        "ritual_vs_admin_suffix_enrichment": suffix_enrichment,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
