"""
Suffix Paradigm Reconstruction Analysis
Linear A Decipherment Project — 2026-03-18

Strategy 2: Group multi-syllable tokens by word-final syllable.
Check if suffix groups cluster around specific logograms, contexts, or sites.
Compare against Hurrian case suffix inventory.

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/suffix_paradigm_results_2026-03-18.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/suffix_paradigm_results_2026-03-18.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")

NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈"}

# Hurrian case suffixes for comparison
HURRIAN_SUFFIXES = {
    "NE": "nominative plural",
    "NA": "locative / genitive (Hurrian -na)",
    "RA": "locative (Hurrian -ra)",
    "DA": "dative/directive (Hurrian -da)",
    "TE": "unknown case (Hurrian -te/di attested)",
    "RE": "possibly related to Hurrian -r(i) genitive",
    "TI": "possibly related to Hurrian -di absolutive",
    "RO": "possibly Minoan-specific (KI-RO: deficit; KU-RO: total)",
    "JA": "possibly Minoan-specific or morphological gender marker",
}


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
    if re.match(r"^[A-Z]{2,4}$", token):
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def extract_syllables(token):
    """Split a hyphenated token into individual syllables."""
    return token.split("-")


def get_final_syllable(token):
    """Return the last hyphen-separated component of a multi-syllable token."""
    parts = token.split("-")
    return parts[-1] if len(parts) > 1 else None


def is_multisyllable_word(token):
    """A token that is a multi-syllable word (not logogram, not numeral, not punct)."""
    if is_numeral(token):
        return False
    if is_logogram(token):
        return False
    if is_punct(token):
        return False
    if "-" not in token:
        return False
    # Filter out things like OLE+U or VIR+KA (logogram compounds)
    if "+" in token:
        return False
    return True


def get_cooccurring_logograms(record_tokens):
    """Return set of logograms appearing in the record."""
    logos = set()
    for tok in record_tokens:
        if tok in KNOWN_LOGOGRAMS:
            logos.add(tok)
        else:
            for prefix in LOGOGRAM_PREFIXES:
                if tok.startswith(prefix):
                    logos.add(prefix.rstrip("+"))
    return logos


def analyze_suffixes(records):
    """
    For each multi-syllable token, extract the final syllable and
    gather: count, sites, support types, co-occurring logograms.
    """
    suffix_tokens = defaultdict(list)     # suffix -> list of token values
    suffix_records = defaultdict(set)     # suffix -> set of record IDs
    suffix_sites = defaultdict(set)       # suffix -> set of sites
    suffix_supports = defaultdict(Counter)  # suffix -> Counter of support types
    suffix_logograms = defaultdict(Counter)  # suffix -> Counter of co-occurring logograms
    suffix_has_kuro = defaultdict(int)    # suffix -> count of records with KU-RO
    suffix_has_kiro = defaultdict(int)    # suffix -> count of records with KI-RO

    for r in records:
        tokens = get_tokens(r)
        logos = get_cooccurring_logograms(tokens)
        has_kuro = "KU-RO" in tokens
        has_kiro = "KI-RO" in tokens
        site = r.get("site") or "unknown"
        support = r.get("support") or "unknown"

        for tok in tokens:
            if not is_multisyllable_word(tok):
                continue
            final = get_final_syllable(tok)
            if not final:
                continue
            # Normalize: uppercase only
            final = final.upper()
            # Filter out subscript digits (e.g., PA₃ → skip)
            if any(c.isdigit() or ord(c) > 127 for c in final):
                continue

            suffix_tokens[final].append(tok)
            suffix_records[final].add(r["id"])
            suffix_sites[final].add(site)
            suffix_supports[final][support] += 1
            for logo in logos:
                suffix_logograms[final][logo] += 1
            if has_kuro:
                suffix_has_kuro[final] += 1
            if has_kiro:
                suffix_has_kiro[final] += 1

    # Build result structure
    all_suffixes = sorted(suffix_records.keys(), key=lambda s: -len(suffix_records[s]))
    result = {}
    for suffix in all_suffixes:
        token_list = suffix_tokens[suffix]
        unique_tokens = Counter(token_list)
        result[suffix] = {
            "record_count": len(suffix_records[suffix]),
            "token_occurrence_count": len(token_list),
            "site_count": len(suffix_sites[suffix]),
            "sites": sorted(suffix_sites[suffix]),
            "top_tokens": [tok for tok, _ in unique_tokens.most_common(10)],
            "support_distribution": dict(suffix_supports[suffix]),
            "top_cooccurring_logograms": [
                {"logogram": l, "cooccurrences": c}
                for l, c in suffix_logograms[suffix].most_common(8)
            ],
            "records_with_kuro": suffix_has_kuro[suffix],
            "records_with_kiro": suffix_has_kiro[suffix],
            "hurrian_parallel": HURRIAN_SUFFIXES.get(suffix, None),
        }
    return result


def analyze_suffix_pairs(records):
    """
    Look at all pairs of words in the same record that share a suffix.
    High-frequency same-suffix pairs may be paradigm members.
    """
    suffix_pair_counts = Counter()

    for r in records:
        tokens = get_tokens(r)
        words_with_suffix = {}
        for tok in tokens:
            if not is_multisyllable_word(tok):
                continue
            final = get_final_syllable(tok)
            if final and not any(c.isdigit() or ord(c) > 127 for c in final):
                words_with_suffix[tok] = final.upper()

        # For each record, count how many words share each suffix
        suffix_in_record = Counter(words_with_suffix.values())
        for suffix, cnt in suffix_in_record.items():
            if cnt >= 2:
                suffix_pair_counts[suffix] += 1

    return dict(suffix_pair_counts.most_common(20))


def compute_suffix_logogram_matrix(suffix_stats):
    """Build a clean matrix of suffix x logogram co-occurrence rates."""
    # Get top suffixes and top logograms
    top_suffixes = [
        s for s, data in sorted(suffix_stats.items(), key=lambda x: -x[1]["record_count"])
        if data["record_count"] >= 10
    ][:15]

    all_logograms = Counter()
    for data in suffix_stats.values():
        for entry in data["top_cooccurring_logograms"]:
            all_logograms[entry["logogram"]] += entry["cooccurrences"]
    top_logograms = [l for l, _ in all_logograms.most_common(10)]

    matrix = {}
    for suffix in top_suffixes:
        logo_dict = {
            entry["logogram"]: entry["cooccurrences"]
            for entry in suffix_stats[suffix]["top_cooccurring_logograms"]
        }
        matrix[suffix] = {logo: logo_dict.get(logo, 0) for logo in top_logograms}

    return matrix


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    print("Analyzing suffix distributions...")
    suffix_stats = analyze_suffixes(records)
    print(f"  Found {len(suffix_stats)} distinct final syllables")

    print("Analyzing intra-record suffix pairing...")
    suffix_pair_counts = analyze_suffix_pairs(records)

    print("Building suffix x logogram co-occurrence matrix...")
    suffix_logogram_matrix = compute_suffix_logogram_matrix(suffix_stats)

    # Summary of top suffixes
    print("\nTop 10 suffixes by record count:")
    top_10 = sorted(suffix_stats.items(), key=lambda x: -x[1]["record_count"])[:10]
    for suffix, data in top_10:
        hurrian = data.get("hurrian_parallel", "—")
        print(
            f"  -{suffix}: {data['record_count']} records, "
            f"{data['site_count']} sites, "
            f"KU-RO co-occ: {data['records_with_kuro']}, "
            f"KI-RO co-occ: {data['records_with_kiro']}, "
            f"Hurrian: {hurrian}"
        )

    # Hurrian comparison summary
    hurrian_comparison = {}
    for suffix, hurrian_meaning in HURRIAN_SUFFIXES.items():
        if suffix in suffix_stats:
            data = suffix_stats[suffix]
            hurrian_comparison[suffix] = {
                "la_suffix": f"-{suffix}",
                "hurrian_meaning": hurrian_meaning,
                "record_count": data["record_count"],
                "site_count": data["site_count"],
                "sites": data["sites"][:5],
                "top_tokens": data["top_tokens"][:5],
                "kuro_cooccurrence_rate": (
                    round(data["records_with_kuro"] / max(data["record_count"], 1), 3)
                ),
                "kiro_cooccurrence_rate": (
                    round(data["records_with_kiro"] / max(data["record_count"], 1), 3)
                ),
                "top_logograms": data["top_cooccurring_logograms"][:3],
            }

    output = {
        "corpus_size": len(records),
        "total_suffixes_found": len(suffix_stats),
        "suffix_stats": suffix_stats,
        "suffix_logogram_matrix": suffix_logogram_matrix,
        "hurrian_comparison": hurrian_comparison,
        "intra_record_suffix_pair_counts": suffix_pair_counts,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
