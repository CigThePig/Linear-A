"""
Lexical Expansion via Administrative Entity Tokens
Linear A Decipherment Project — 2026-03-19

H2: The most frequent multi-sign sequences appearing immediately before commodity
logograms in accounting records are entity/category labels that can be assigned
provisional semantic roles through positional, distributional, and comparative analysis.

Success threshold: ≥5 new sequences with ≥3 occurrences, ≥2 sites, not already known.

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/lexical_expansion_2026-03-19.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/lexical_expansion_2026-03-19.json")

# All known commodity logograms (exact token matches)
COMMODITY_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI",
}
LOGOGRAM_PREFIXES = (
    "GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "MUL+",
    "GRA2", "OLE2", "OLE3", "GRA3",
)

# Known formulas to exclude from "new" candidates
KNOWN_FORMULAS = {
    "KU-RO", "KI-RO", "*23M", "A-TA-I", "JA-SA-SA-RA-ME",
    "U-NA-KA-NA-SI", "I-PI-NA-MA", "SI-RU-TE", "JA-DI-KI-TU",
    "A-DI-KI-TE", "TA-NA-RA-TE-U-TI-NU", "TA-NA-I",
}

# Admin support types
ADMIN_SUPPORTS = {"tablet", "nodule", "roundel", "clay vessel", "lame", "label"}

NUM_RE = re.compile(r"^\d+$|^[¼½¾⅐-⅟]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈", "|", "//"}

# Hurrian administrative vocabulary for cross-reference
# (phonological skeletons from Mitanni-period texts and Nuzi tablets)
HURRIAN_ADMIN_VOCAB = {
    "ewri": ("lord/king", "W-R"),
    "šen": ("brother", "Š-N"),
    "tive": ("word/matter", "T-V"),
    "ḫiari": ("field/land", "Ḫ-R"),
    "purli": ("city/town", "P-R-L"),
    "šuḫni": ("oil", "Š-Ḫ-N"),
    "kiaži": ("man/person", "K-Ž"),
    "mannu": ("who", "M-N"),
    "šimri": ("sheep", "Š-M-R"),
    "unute": ("vessel/implement", "W-N-T"),
    "tenu": ("ration/portion", "T-N"),
    "urpi": ("grain portion", "W-R-P"),
    "ḫašiḫe": ("grain type", "Ḫ-Š-Ḫ"),
    "taḫuri": ("large", "T-Ḫ-R"),
    "šukku": ("small/young", "Š-K"),
    "tilla": ("replacement/substitute", "T-L"),
    "niri": ("yoke/team", "N-R"),
    "arnu": ("penalty/fine", "W-R-N"),
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


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_commodity_logogram(token):
    if token in COMMODITY_LOGOGRAMS:
        return True
    for prefix in LOGOGRAM_PREFIXES:
        if token.startswith(prefix):
            return True
    return False


def normalize_logogram(token):
    """Get the base logogram name from a compound like GRA+WA."""
    for lg in COMMODITY_LOGOGRAMS:
        if token == lg or token.startswith(lg + "+"):
            return lg
    for prefix in LOGOGRAM_PREFIXES:
        if token.startswith(prefix):
            return prefix.rstrip("+").rstrip("23")
    return token


def is_known_formula(token):
    t = token.upper()
    for f in KNOWN_FORMULAS:
        if t == f or t.startswith(f):
            return True
    return False


def extract_pre_logogram_tokens(tokens, window=2):
    """
    Find all positions where a commodity logogram appears and extract
    the 1–2 tokens immediately before it (skipping punct/numerals).
    Returns list of (pre_token, logogram, distance) tuples.
    """
    results = []
    # Build index of non-punct, non-numeral tokens
    content_positions = [
        (i, tok) for i, tok in enumerate(tokens)
        if not is_punct(tok) and not is_numeral(tok)
    ]

    for ci, (raw_idx, tok) in enumerate(content_positions):
        if not is_commodity_logogram(tok):
            continue
        logo = normalize_logogram(tok)

        # Look back up to 2 content positions
        for dist in range(1, window + 1):
            if ci - dist < 0:
                break
            _, prev_tok = content_positions[ci - dist]
            if is_commodity_logogram(prev_tok):
                break  # Don't cross another logogram boundary
            if not is_punct(prev_tok) and not is_numeral(prev_tok):
                results.append((prev_tok, logo, dist))

    return results


def analyze_pre_logogram(records):
    """
    Aggregate pre-logogram token occurrences across all admin records.
    """
    # (pre_token, logogram, distance) -> {count, sites, records}
    combo_counts = Counter()
    combo_sites = defaultdict(set)
    combo_records = defaultdict(set)

    # Also track: pre_token -> which logograms it precedes
    pre_token_logograms = defaultdict(Counter)
    pre_token_sites = defaultdict(set)
    pre_token_counts = Counter()
    pre_token_records = defaultdict(set)
    pre_token_distance1 = Counter()  # only distance=1 (immediately adjacent)

    for r in records:
        support = (r.get("support") or "").lower()
        if support not in ADMIN_SUPPORTS:
            continue
        tokens = get_tokens(r)
        site = r.get("site") or "unknown"
        rid = r.get("id", "")

        pairs = extract_pre_logogram_tokens(tokens, window=2)
        for pre_tok, logo, dist in pairs:
            key = (pre_tok, logo, dist)
            combo_counts[key] += 1
            combo_sites[key].add(site)
            combo_records[key].add(rid)

            pre_token_logograms[pre_tok][logo] += 1
            pre_token_sites[pre_tok].add(site)
            pre_token_counts[pre_tok] += 1
            pre_token_records[pre_tok].add(rid)
            if dist == 1:
                pre_token_distance1[pre_tok] += 1

    return (
        combo_counts, combo_sites, combo_records,
        pre_token_logograms, pre_token_sites, pre_token_counts,
        pre_token_records, pre_token_distance1
    )


def compute_consonant_skeleton(token):
    """
    Approximate consonant skeleton by removing vowels from conventional
    transliteration. Used for cross-language comparison.
    """
    syllables = token.upper().split("-")
    consonants = []
    for syl in syllables:
        # Keep only consonant-like characters (not A E I O U)
        c = re.sub(r"[AEIOU]", "", syl)
        c = re.sub(r"[^A-Z]", "", c)  # strip digits/special
        if c:
            consonants.append(c)
    return "-".join(consonants) if consonants else ""


def score_hurrian_match(token, hurrian_vocab):
    """Check if token's consonant skeleton matches any Hurrian vocabulary entry."""
    skeleton = compute_consonant_skeleton(token)
    matches = []
    for hurrian_word, (meaning, hurrian_skeleton) in hurrian_vocab.items():
        # Simplistic overlap: check if main consonants present
        h_consonants = set(hurrian_skeleton.replace("-", "").replace("Ḫ", "H").replace("Š", "S").replace("Ž", "Z"))
        t_consonants = set(skeleton.replace("-", ""))
        if len(h_consonants) >= 2 and h_consonants <= t_consonants:
            matches.append({
                "hurrian_word": hurrian_word,
                "hurrian_meaning": meaning,
                "hurrian_skeleton": hurrian_skeleton,
                "la_skeleton": skeleton,
            })
    return matches


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    admin_records = [r for r in records if (r.get("support") or "").lower() in ADMIN_SUPPORTS]
    print(f"Admin records: {len(admin_records)}")

    print("Extracting pre-logogram tokens...")
    (
        combo_counts, combo_sites, combo_records,
        pre_token_logograms, pre_token_sites, pre_token_counts,
        pre_token_records, pre_token_distance1
    ) = analyze_pre_logogram(records)

    # Build candidate list: tokens with ≥3 occurrences, ≥2 sites, not known formulas
    candidates = []
    for tok, count in pre_token_counts.most_common(100):
        sites = pre_token_sites[tok]
        records_set = pre_token_records[tok]
        if count < 3:
            break
        if len(sites) < 2:
            continue
        if is_known_formula(tok):
            continue
        # Skip pure single-syllable tokens (likely grammatical particles)
        if "-" not in tok and len(tok) <= 3:
            continue

        logo_dist = dict(pre_token_logograms[tok].most_common(5))
        top_logo = pre_token_logograms[tok].most_common(1)
        logo_specificity = (
            top_logo[0][1] / sum(pre_token_logograms[tok].values())
            if top_logo else 0
        )
        dist1_count = pre_token_distance1[tok]
        hurrian_matches = score_hurrian_match(tok, HURRIAN_ADMIN_VOCAB)

        candidates.append({
            "token": tok,
            "total_occurrences": count,
            "immediate_pre_logogram_count": dist1_count,
            "site_count": len(sites),
            "sites": sorted(sites),
            "record_count": len(records_set),
            "logogram_distribution": logo_dist,
            "top_logogram": top_logo[0][0] if top_logo else None,
            "logogram_specificity": round(logo_specificity, 3),
            "consonant_skeleton": compute_consonant_skeleton(tok),
            "hurrian_vocabulary_matches": hurrian_matches,
            "semantic_role_hypothesis": (
                "commodity_modifier" if logo_specificity >= 0.7 and dist1_count >= 2
                else "general_pre_logogram" if dist1_count >= 3
                else "indirect_association"
            ),
        })

    print(f"\nFound {len(candidates)} candidate pre-logogram sequences")
    print(f"Candidates meeting ≥3 occ, ≥2 sites, not known formula:")
    for c in candidates[:15]:
        print(
            f"  {c['token']}: {c['total_occurrences']} occ, {c['site_count']} sites, "
            f"top logo: {c['top_logogram']} ({c['logogram_specificity']:.0%} specificity)"
        )

    # H2 evaluation
    qualifying = [c for c in candidates if c["total_occurrences"] >= 3 and c["site_count"] >= 2]
    h2_result = (
        "SUPPORTED" if len(qualifying) >= 5
        else f"PARTIAL — only {len(qualifying)} qualifying candidates (threshold: 5)"
        if qualifying
        else "FAILED — no qualifying candidates"
    )
    print(f"\nH2 result: {h2_result}")

    # Also: compute which admin sites contribute most logogram records
    site_logogram_counts = Counter()
    for r in admin_records:
        tokens = get_tokens(r)
        site = r.get("site") or "unknown"
        for tok in tokens:
            if is_commodity_logogram(tok):
                site_logogram_counts[site] += 1

    # Top combo pairs (for reference)
    top_combos = [
        {
            "pre_token": pre,
            "logogram": logo,
            "distance": dist,
            "count": cnt,
            "sites": sorted(combo_sites[(pre, logo, dist)]),
        }
        for (pre, logo, dist), cnt in combo_counts.most_common(50)
        if cnt >= 2
    ]

    output = {
        "analysis": "H2: Lexical Expansion via Pre-Logogram Token Mining",
        "date": "2026-03-19",
        "corpus_size": len(records),
        "admin_records_analyzed": len(admin_records),
        "hypothesis_result": h2_result,
        "success_threshold": "≥5 tokens with ≥3 occurrences, ≥2 sites, not known formulas",
        "qualifying_candidate_count": len(qualifying),
        "candidates": candidates[:50],
        "top_pre_logogram_combos": top_combos[:50],
        "site_logogram_contribution": dict(site_logogram_counts.most_common(20)),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
