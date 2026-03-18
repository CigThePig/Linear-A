"""
Proper Noun Isolation via Site-Specificity Analysis
Linear A Decipherment Project — 2026-03-18

Strategy 3: Compute site-specificity scores for all multi-syllable sign sequences
to identify proper noun candidates (place names, personal names).

Key hypotheses:
- High site-specificity (≥0.8) indicates likely proper nouns
- Site-specific tokens adjacent to VIR are likely personal names
- Some site-specific tokens will be phonologically compatible with known Aegean toponyms

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/proper_noun_candidates_2026-03-18.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/proper_noun_candidates_2026-03-18.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")
NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈"}

# Major sites to analyze
MAJOR_SITES = [
    "Haghia Triada", "Khania", "Phaistos", "Knossos", "Zakros",
    "Iouktas", "Palaikastro", "Tylissos", "Gournia", "Malia"
]

# Known Minoan/Aegean place names preserved in Greek tradition
# Stored as simplified consonant skeletons for phonological comparison
AEGEAN_TOPONYMS = {
    "Amnisos":      ["MN", "MNS"],
    "Tylissos":     ["TL", "TLS"],
    "Knossos":      ["KN", "KNS"],
    "Phaistos":     ["PS", "PST", "PT"],
    "Zakros":       ["ZK", "ZKR"],
    "Nirou":        ["NR"],
    "Palaikastro":  ["PL", "PLK"],
    "Malia":        ["ML", "MLA"],
    "Gortyn":       ["GRT", "GR"],
    "Dikte":        ["DK", "DKT"],
    "Arkhanes":     ["RK", "RKN"],
    "Iasos":        ["JS", "JAS"],
    "Minoai":       ["MN", "MIN"],
    "Haghia Triada": ["HT", "TR"],
    "Kommos":       ["KM", "KMM"],
}

# Linear B site names that may correspond to Minoan predecessors
LINEAR_B_MINOAN_NAMES = {
    "a-mi-ni-so": "Amnisos",
    "pa-i-to":    "Phaistos",
    "za-ko-ro":   "Zakros",
    "ko-no-so":   "Knossos",
    "tu-ri-so":   "Tylissos",
    "ma-ra-ti":   "Malia?",
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


def is_multisyllable(token):
    """Token must have at least 2 syllables (contain at least one hyphen)."""
    return "-" in token


def compute_site_specificity(records, min_occurrences=3):
    """
    For every multi-syllable sign sequence, compute:
    - Total occurrences
    - Per-site occurrence counts
    - Site-specificity score = max_site_count / total_count (range 0–1)
    - Primary site (where most occurrences are found)
    """
    token_total = Counter()
    token_by_site = defaultdict(Counter)

    for r in records:
        site = r.get("site") or "unknown"
        tokens = get_tokens(r)
        # Count distinct tokens per record to avoid counting repeats within one tablet
        seen_in_record = set()
        for tok in tokens:
            if is_formula_candidate(tok) and is_multisyllable(tok) and tok not in seen_in_record:
                token_total[tok] += 1
                token_by_site[tok][site] += 1
                seen_in_record.add(tok)

    results = {}
    for tok, total in token_total.items():
        if total < min_occurrences:
            continue
        site_counts = dict(token_by_site[tok])
        max_site = max(site_counts, key=site_counts.get)
        max_count = site_counts[max_site]
        specificity = max_count / total

        results[tok] = {
            "total_occurrences": total,
            "site_count": len(site_counts),
            "primary_site": max_site,
            "primary_site_count": max_count,
            "specificity_score": round(specificity, 3),
            "site_distribution": dict(sorted(site_counts.items(), key=lambda x: -x[1])),
        }

    return results


def extract_top_candidates_per_site(specificity_data, threshold=0.8, top_n=20):
    """
    For each major site, get the top-N most site-specific tokens.
    Only include tokens above the specificity threshold.
    """
    site_candidates = defaultdict(list)

    for tok, data in specificity_data.items():
        if data["specificity_score"] >= threshold:
            site_candidates[data["primary_site"]].append({
                "token": tok,
                "specificity": data["specificity_score"],
                "total": data["total_occurrences"],
                "primary_count": data["primary_site_count"],
                "all_sites": data["site_distribution"],
            })

    # Sort each site's candidates by total occurrences (prefer well-attested tokens)
    result = {}
    for site in MAJOR_SITES:
        candidates = site_candidates.get(site, [])
        candidates.sort(key=lambda x: (-x["total"], -x["specificity"]))
        result[site] = candidates[:top_n]

    return result


def get_consonant_skeleton(token):
    """
    Extract simplified consonant skeleton from a Linear A transliteration.
    Maps Linear B-style CV syllables to their consonants.
    E.g., "KU-RO" -> "KR", "I-PI-NA-MA" -> "PNM"
    """
    # Known vowel-initial syllables (consonant = none)
    VOWEL_SYLLABLES = {"A", "I", "E", "O", "U"}
    # Consonant mapping for CV syllables
    consonants = []
    for syllable in token.split("-"):
        if syllable in VOWEL_SYLLABLES:
            continue  # pure vowel syllable, no consonant
        # Take the first character as the consonant (works for most CV syllables)
        # Special cases: TA->T, DA->D, KA->K, etc.
        if len(syllable) >= 1:
            c = syllable[0]
            if c.isalpha() and c not in ("A", "E", "I", "O", "U"):
                consonants.append(c)
            elif len(syllable) >= 2 and syllable[1] not in ("A", "E", "I", "O", "U"):
                # Consonant cluster like "WA" -> W
                consonants.append(syllable[0])
    return "".join(consonants)


def check_toponym_match(token, consonant_skeleton):
    """
    Check if a Linear A token's consonant skeleton matches known Aegean toponyms.
    Uses loose matching (skeleton must contain the toponym's consonant pattern).
    Returns list of matching toponyms.
    """
    matches = []
    for toponym, patterns in AEGEAN_TOPONYMS.items():
        for pattern in patterns:
            if (pattern in consonant_skeleton or
                    consonant_skeleton in pattern or
                    (len(pattern) >= 2 and pattern[:2] == consonant_skeleton[:2])):
                matches.append({
                    "toponym": toponym,
                    "pattern": pattern,
                    "match_type": "skeleton_match",
                })
                break
    return matches


def check_linear_b_match(token):
    """
    Check if a Linear A token matches known Linear B renditions of Minoan place names.
    """
    # Normalize: lowercase, keep hyphens
    tok_lower = token.lower()
    matches = []
    for lb_form, toponym in LINEAR_B_MINOAN_NAMES.items():
        # Check if all parts of Linear B form appear in Linear A token
        lb_parts = lb_form.split("-")
        tok_parts = tok_lower.split("-")
        shared = sum(1 for p in lb_parts if p in tok_parts)
        if shared >= 2 or (len(lb_parts) <= 2 and shared >= 1 and lb_parts[0] == tok_parts[0]):
            matches.append({
                "linear_b_form": lb_form,
                "toponym": toponym,
                "shared_syllables": shared,
            })
    return matches


def find_vir_adjacent_tokens(records, site_candidates):
    """
    For each site, identify which site-specific tokens appear adjacent to VIR logogram.
    VIR-adjacent site-specific tokens are likely personal names.
    """
    # Build set of all high-specificity tokens per site
    candidate_sets = {}
    for site, candidates in site_candidates.items():
        candidate_sets[site] = {c["token"] for c in candidates}

    vir_adjacent = defaultdict(Counter)

    for r in records:
        site = r.get("site") or "unknown"
        tokens = get_tokens(r)
        for i, tok in enumerate(tokens):
            if tok == "VIR":
                # Check tokens within 2 positions
                context = tokens[max(0, i - 2):i] + tokens[i + 1:min(len(tokens), i + 3)]
                for ctx_tok in context:
                    if is_formula_candidate(ctx_tok):
                        vir_adjacent[site][ctx_tok] += 1

    # Flag which VIR-adjacent tokens are also high-specificity for that site
    result = {}
    for site in MAJOR_SITES:
        site_specific = candidate_sets.get(site, set())
        adj = {
            tok: {
                "vir_adjacency_count": count,
                "is_site_specific": tok in site_specific,
            }
            for tok, count in vir_adjacent[site].most_common(20)
        }
        if adj:
            result[site] = adj

    return result


def compute_token_support_profile(records, candidate_tokens):
    """
    For high-specificity candidate tokens, compute their support type distribution.
    Personal names appear on tablets/nodules; place names appear more broadly.
    """
    support_profiles = {}
    token_set = set(candidate_tokens)

    token_support = defaultdict(Counter)
    for r in records:
        support = (r.get("support") or "unknown").lower().strip()
        for tok in get_tokens(r):
            if tok in token_set:
                token_support[tok][support] += 1

    for tok in candidate_tokens:
        if tok in token_support:
            profile = dict(token_support[tok].most_common())
            total = sum(profile.values())
            support_profiles[tok] = {
                "total": total,
                "support_distribution": profile,
                "primary_support": max(profile, key=profile.get) if profile else "unknown",
            }

    return support_profiles


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    print("\n--- Computing site-specificity scores ---")
    specificity_data = compute_site_specificity(records, min_occurrences=3)
    print(f"  Computed specificity for {len(specificity_data)} multi-syllable tokens (min 3 occ)")

    high_specificity = {
        tok: d for tok, d in specificity_data.items()
        if d["specificity_score"] >= 0.8
    }
    print(f"  High-specificity tokens (≥0.8): {len(high_specificity)}")

    print("\n--- Extracting top candidates per major site ---")
    site_candidates = extract_top_candidates_per_site(specificity_data, threshold=0.8)
    for site in MAJOR_SITES:
        candidates = site_candidates.get(site, [])
        if candidates:
            print(f"  {site}: {len(candidates)} candidates (top: {candidates[0]['token']} @ {candidates[0]['specificity']:.2f})")

    print("\n--- Cross-referencing with Aegean toponyms ---")
    toponym_matches = {}
    all_candidates = [c["token"] for candidates in site_candidates.values() for c in candidates]
    for tok in all_candidates:
        skeleton = get_consonant_skeleton(tok)
        topo_matches = check_toponym_match(tok, skeleton)
        lb_matches = check_linear_b_match(tok)
        if topo_matches or lb_matches:
            toponym_matches[tok] = {
                "consonant_skeleton": skeleton,
                "toponym_matches": topo_matches,
                "linear_b_matches": lb_matches,
            }
            print(f"  {tok} (skeleton: {skeleton}): {[m['toponym'] for m in topo_matches]}")

    print(f"\n  Total tokens with toponym matches: {len(toponym_matches)}")

    print("\n--- Finding VIR-adjacent site-specific tokens (personal name candidates) ---")
    vir_adjacent = find_vir_adjacent_tokens(records, site_candidates)
    for site, adj in list(vir_adjacent.items())[:5]:
        specific = [(t, d) for t, d in adj.items() if d["is_site_specific"]]
        if specific:
            print(f"  {site}: {[t for t, _ in specific[:5]]} (VIR-adjacent site-specific)")

    print("\n--- Computing support profiles for high-specificity tokens ---")
    all_candidate_tokens = list(high_specificity.keys())
    support_profiles = compute_token_support_profile(records, all_candidate_tokens)

    # Summary statistics
    global_stats = {
        "total_tokens_analyzed": len(specificity_data),
        "high_specificity_count": len(high_specificity),
        "toponym_match_count": len(toponym_matches),
        "site_candidate_counts": {
            site: len(site_candidates.get(site, []))
            for site in MAJOR_SITES
        },
    }

    print(f"\n--- Summary ---")
    print(f"  Total multi-syllable tokens: {global_stats['total_tokens_analyzed']}")
    print(f"  High-specificity candidates: {global_stats['high_specificity_count']}")
    print(f"  Toponym matches: {global_stats['toponym_match_count']}")

    output = {
        "global_stats": global_stats,
        "site_candidates": {
            site: candidates
            for site, candidates in site_candidates.items()
            if candidates
        },
        "toponym_matches": toponym_matches,
        "vir_adjacent_analysis": vir_adjacent,
        "support_profiles": {
            tok: support_profiles[tok]
            for tok in list(high_specificity.keys())[:100]  # sample
            if tok in support_profiles
        },
        "all_high_specificity": dict(
            sorted(high_specificity.items(), key=lambda x: -x[1]["total_occurrences"])
        ),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
