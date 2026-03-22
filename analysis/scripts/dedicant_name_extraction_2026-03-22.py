"""
Dedicant Name Extraction — Attempt #14
=======================================
Under Davis (2026) VSO model, slot-2 in the ritual formula
(A-TA-I-*301-WA-JA → slot-2 → slot-3+) is the SUBJECT — either
a human dedicant (personal name) or divine addressee (fixed element).

This script extracts slot-2 tokens from Attempt #11 output OR independently
re-extracts them, then applies personal name vs. divine name classification.

Also runs LCS consonant-skeleton matching against:
  - Bronze Age Aegean name skeletons (Minos, Ariadne, Rhadamanthos)
  - Hurrian personal name patterns
  - Minoan names preserved in Linear B Knossos texts

Output: analysis/outputs/dedicant_name_extraction_2026-03-22.json
"""

import json
from collections import Counter, defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
VSO_OUTPUT_PATH = "analysis/outputs/vso_ritual_reanalysis_2026-03-22.json"
OUTPUT_PATH = "analysis/outputs/dedicant_name_extraction_2026-03-22.json"

RITUAL_HEADER = "A-TA-I-*301-WA-JA"
RITUAL_SUPPORTS_LC = {"stone vessel", "metal object", "architecture", "stone object"}

# Known fixed ritual elements (divine names, liturgical sequences)
KNOWN_RITUAL_ELEMENTS = {
    "JA-SA-SA-RA-ME", "JA-SA-SA-RA-MA", "JA-SA-SA-RA",
    "U-NA-KA-NA-SI",
    "I-PI-NA-MA",
    "SI-RU-TE",
    "JA-DI-KI-TU",
    "A-DI-KI-TE-TE",
    "DI-KI-TE", "DI-KI",
    "TA-NA-RA-TE-U-TI-NU",
}

# Personal name suffix indicators (from Attempt #3 findings)
NAME_SUFFIXES = {"TI", "TA", "TE", "SI", "NE"}

# Reference name consonant skeletons for LCS matching
# Format: (name, language/source, consonant_list)
REFERENCE_NAMES = [
    # Bronze Age Aegean preserved names
    ("Minos", "Greek-Minoan", ["M", "N"]),
    ("Ariadne", "Greek-Minoan", ["R", "D", "N"]),
    ("Rhadamanthos", "Greek-Minoan", ["R", "D", "M", "T"]),
    ("Daedalus", "Greek-Minoan", ["D", "D", "L"]),
    ("Pasiphae", "Greek-Minoan", ["P", "S", "P"]),
    ("Malia", "Toponym", ["M", "L"]),
    ("Knossos", "Toponym", ["K", "N", "S"]),
    ("Phaistos", "Toponym", ["P", "S", "T"]),
    ("Amnisos", "Toponym", ["M", "N", "S"]),
    ("Dikte", "Toponym", ["D", "K", "T"]),
    # Hurrian personal name patterns
    ("Teshup-compound", "Hurrian", ["T", "S", "P"]),
    ("Shaushka", "Hurrian-deity", ["S", "S", "K"]),
    ("Hebat", "Hurrian-deity", ["H", "B", "T"]),
    ("Ewri", "Hurrian-title", ["W", "R"]),
    ("Tupkish", "Hurrian-name", ["T", "P", "K", "S"]),
    # Linear B non-Greek Knossos names (consonant skeletons)
    ("Minowia", "Linear-B-non-Greek", ["M", "N", "W"]),
    ("Diwia", "Linear-B", ["D", "W"]),
    ("Potnia", "Linear-B", ["P", "T", "N"]),
    ("Rawaketa", "Linear-B", ["R", "W", "K", "T"]),
    # Known Linear A proper names from prior attempts
    ("DI-KI", "Linear-A-toponym", ["D", "K"]),
    ("JA-DI-KI-TU", "Linear-A-ritual", ["D", "K", "T"]),
]

SYLLABLE_TO_CONSONANT = {
    "A": None, "E": None, "I": None, "O": None, "U": None,
    "JA": "J", "JE": "J", "JO": "J", "JU": "J",
    "WA": "W", "WE": "W", "WI": "W", "WO": "W",
    "TA": "T", "TE": "T", "TI": "T", "TO": "T", "TU": "T",
    "DA": "D", "DE": "D", "DI": "D", "DO": "D", "DU": "D",
    "NA": "N", "NE": "N", "NI": "N", "NO": "N", "NU": "N",
    "KA": "K", "KE": "K", "KI": "K", "KO": "K", "KU": "K",
    "PA": "P", "PE": "P", "PI": "P", "PO": "P", "PU": "P",
    "RA": "R", "RE": "R", "RI": "R", "RO": "R", "RU": "R",
    "SA": "S", "SE": "S", "SI": "S", "SO": "S", "SU": "S",
    "MA": "M", "ME": "M", "MI": "M", "MO": "M", "MU": "M",
    "LA": "L", "LE": "L", "LI": "L", "LO": "L", "LU": "L",
    "ZA": "Z", "ZE": "Z", "ZI": "Z", "ZO": "Z", "ZU": "Z",
    "QA": "Q", "QE": "Q", "QI": "Q", "QO": "Q",
    "RA2": "R", "RA3": "R",
}


def load_corpus():
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_token_values(rec):
    raw = rec.get("transliteration_tokens", [])
    result = []
    for t in raw:
        if isinstance(t, dict):
            if t.get("type") == "token":
                v = t.get("value", "").strip()
                if v and v not in ("\n", "\\n", ""):
                    result.append(v)
        else:
            v = str(t).strip()
            if v and v not in ("\n", "\\n", ""):
                result.append(v)
    return result


def is_numeral(v):
    try:
        int(v); return True
    except: pass
    try:
        float(v); return True
    except: pass
    if any(c in v for c in "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉⁄") and len(v) <= 8:
        return True
    return False


def is_ritual_support(rec):
    s = rec.get("support", "").lower().strip()
    return s in RITUAL_SUPPORTS_LC


def extract_consonant_skeleton(token):
    """Extract ordered consonant list from a Linear A syllabic token."""
    parts = token.split("-")
    skeleton = []
    for p in parts:
        c = SYLLABLE_TO_CONSONANT.get(p.upper())
        if c is not None:
            skeleton.append(c)
    return skeleton


def lcs_length(a, b):
    """Compute length of longest common subsequence."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def lcs_score(token_skel, ref_skel):
    """Normalized LCS score: lcs_len / max(len_a, len_b)."""
    if not token_skel or not ref_skel:
        return 0.0
    lcs_len = lcs_length(token_skel, ref_skel)
    return lcs_len / max(len(token_skel), len(ref_skel))


def run_name_matching(token):
    """Run LCS consonant-skeleton matching for a token against reference names."""
    skel = extract_consonant_skeleton(token)
    results = []
    for ref_name, source, ref_skel in REFERENCE_NAMES:
        score = lcs_score(skel, ref_skel)
        lcs_len = lcs_length(skel, ref_skel)
        results.append({
            "reference_name": ref_name,
            "source": source,
            "token_skeleton": skel,
            "reference_skeleton": ref_skel,
            "lcs_length": lcs_len,
            "lcs_score": round(score, 3),
            "meets_threshold": lcs_len >= 2 and score >= 0.5,
        })
    results.sort(key=lambda x: -x["lcs_score"])
    return results[:10]


def main():
    records = load_corpus()

    # Re-extract slot-2 tokens independently (don't require Attempt #11 output)
    all_header_records = []
    for rec in records:
        tokens = get_token_values(rec)
        if RITUAL_HEADER in tokens:
            all_header_records.append((rec, tokens))

    slot2_tokens_raw = []
    slot2_by_inscription = []

    for rec, tokens in all_header_records:
        header_idx = tokens.index(RITUAL_HEADER)
        slot2 = None
        if header_idx + 1 < len(tokens):
            candidate = tokens[header_idx + 1]
            if not is_numeral(candidate):
                slot2 = candidate

        slot2_tokens_raw.append(slot2)
        slot2_by_inscription.append({
            "id": rec.get("id", ""),
            "site": rec.get("site", ""),
            "support": rec.get("support", ""),
            "slot2_token": slot2,
            "full_sequence": tokens,
        })

    slot2_counter = Counter(t for t in slot2_tokens_raw if t is not None)
    distinct_slot2 = len(slot2_counter)

    print(f"  Total inscriptions with {RITUAL_HEADER}: {len(all_header_records)}")
    print(f"  Slot-2 tokens extracted: {sum(slot2_counter.values())}")
    print(f"  Distinct slot-2 tokens: {distinct_slot2}")

    # For each distinct slot-2 token: compute profile
    slot2_profiles = {}

    for token, slot2_count in slot2_counter.most_common():
        # Total corpus distribution
        total_corpus_occ = 0
        total_corpus_sites = set()
        total_corpus_records = set()
        for rec in records:
            toks = get_token_values(rec)
            if token in toks:
                total_corpus_occ += 1
                total_corpus_sites.add(rec.get("site", ""))
                total_corpus_records.add(rec.get("id", ""))

        # Site distribution in slot-2 specifically
        slot2_sites = Counter(
            d["site"] for d in slot2_by_inscription if d["slot2_token"] == token
        )
        site_specificity = max(slot2_sites.values()) / sum(slot2_sites.values()) if slot2_sites else 0

        final_syllable = token.split("-")[-1] if "-" in token else token
        syllable_count = len(token.split("-"))
        has_name_suffix = final_syllable in NAME_SUFFIXES
        is_known_ritual = token in KNOWN_RITUAL_ELEMENTS

        # Personal name score
        pn_score = 0
        if total_corpus_occ <= 3:
            pn_score += 2
        elif total_corpus_occ <= 6:
            pn_score += 1
        if site_specificity >= 0.7:
            pn_score += 2
        elif site_specificity >= 0.5:
            pn_score += 1
        if 2 <= syllable_count <= 4:
            pn_score += 1
        if has_name_suffix:
            pn_score += 1
        if is_known_ritual:
            pn_score -= 3  # Fixed ritual element = not a personal name

        # Fixed/divine name criteria
        fixed_score = 0
        if total_corpus_occ >= 5:
            fixed_score += 1
        if len(total_corpus_sites) >= 3:
            fixed_score += 1
        if is_known_ritual:
            fixed_score += 3
        if site_specificity < 0.4:
            fixed_score += 1

        if pn_score >= 4:
            profile = "PERSONAL NAME (high confidence)"
        elif pn_score >= 2:
            profile = "PERSONAL NAME (medium confidence)"
        elif fixed_score >= 3:
            profile = "FIXED RITUAL ELEMENT (divine name / liturgical)"
        else:
            profile = "AMBIGUOUS"

        # Name matching for medium-high personal name candidates
        name_matches = []
        if pn_score >= 2 or is_known_ritual:
            name_matches = run_name_matching(token)

        slot2_profiles[token] = {
            "slot2_occurrences": slot2_count,
            "slot2_sites": dict(slot2_sites.most_common()),
            "site_specificity": round(site_specificity, 3),
            "total_corpus_occurrences": total_corpus_occ,
            "total_corpus_sites": sorted(list(total_corpus_sites)),
            "syllable_count": syllable_count,
            "final_syllable": final_syllable,
            "has_name_suffix": has_name_suffix,
            "is_known_ritual_element": is_known_ritual,
            "personal_name_score": pn_score,
            "fixed_element_score": fixed_score,
            "profile": profile,
            "consonant_skeleton": extract_consonant_skeleton(token),
            "top_name_matches": name_matches[:5],
        }

    # Classify slot-2 overall as variable or fixed
    variable_count = sum(1 for p in slot2_profiles.values()
                         if "PERSONAL NAME" in p["profile"] or p["personal_name_score"] >= 2)
    fixed_count = sum(1 for p in slot2_profiles.values()
                      if "FIXED" in p["profile"])

    if distinct_slot2 >= 5:
        overall_classification = "VARIABLE — multiple distinct tokens (≥5); consistent with dedicant personal names"
    elif distinct_slot2 <= 2:
        overall_classification = "FIXED — very few distinct tokens (≤2); consistent with divine name / fixed formula"
    else:
        overall_classification = f"AMBIGUOUS — {distinct_slot2} distinct tokens; requires further analysis"

    # Check for JA-DI-KI-TU specifically
    jadikitu_profile = slot2_profiles.get("JA-DI-KI-TU", None)

    output = {
        "analysis": "Attempt #14: Dedicant Name Extraction",
        "date": "2026-03-22",
        "new_information_source": (
            "Davis (2026) in Salgarella & Petrakis 'The Wor(l)ds of Linear A': "
            "VSO word order; slot-2 = subject (dedicant or divine addressee)."
        ),
        "total_inscriptions_with_header": len(all_header_records),
        "slot2_tokens_extracted": sum(slot2_counter.values()),
        "distinct_slot2_tokens": distinct_slot2,
        "overall_classification": overall_classification,
        "profiles": slot2_profiles,
        "per_inscription_breakdown": slot2_by_inscription,
        "jadikitu_analysis": {
            "appears_in_slot2": "JA-DI-KI-TU" in slot2_counter,
            "slot2_count": slot2_counter.get("JA-DI-KI-TU", 0),
            "profile": jadikitu_profile["profile"] if jadikitu_profile else "not in slot-2",
            "interpretation": (
                "JA-DI-KI-TU is in slot-2 and shows fixed-element profile → likely divine name/addressee (Diktynna)"
                if jadikitu_profile and "FIXED" in jadikitu_profile.get("profile", "")
                else (
                    "JA-DI-KI-TU is in slot-2 with variable profile → reexamine Diktynna hypothesis"
                    if jadikitu_profile and "PERSONAL" in jadikitu_profile.get("profile", "")
                    else "JA-DI-KI-TU not observed in slot-2 position in this corpus"
                )
            ),
        },
        "conclusion": {
            "slot2_variable_or_fixed": overall_classification,
            "vso_dedication_model_supported": distinct_slot2 >= 3,
            "personal_name_candidates": [
                tok for tok, prof in slot2_profiles.items()
                if "PERSONAL NAME" in prof["profile"]
            ],
            "best_name_matches": {
                tok: prof["top_name_matches"][:3]
                for tok, prof in slot2_profiles.items()
                if prof.get("top_name_matches") and prof["personal_name_score"] >= 2
            },
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nAttempt #14 (Dedicant Name Extraction) complete.")
    print(f"  Distinct slot-2 tokens: {distinct_slot2}")
    print(f"  Classification: {overall_classification}")
    print(f"  JA-DI-KI-TU in slot-2: {'YES' if 'JA-DI-KI-TU' in slot2_counter else 'NO'}")
    print(f"  Slot-2 token profiles:")
    for tok, count in slot2_counter.most_common():
        prof = slot2_profiles.get(tok, {})
        print(f"    {tok} (n={count}): {prof.get('profile', '?')}, "
              f"corpus_occ={prof.get('total_corpus_occurrences', '?')}, "
              f"site_spec={prof.get('site_specificity', '?')}")


if __name__ == "__main__":
    main()
