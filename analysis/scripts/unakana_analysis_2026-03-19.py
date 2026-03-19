#!/usr/bin/env python3
"""
U-NA-KA-NA-SI Deep Analysis + -ME Comitative/Essive Test
Linear A Decipherment Project — 2026-03-19

Purpose:
  1. Find all occurrences of U-NA-KA-NA-SI and analyze its distributional profile.
     Does it ONLY follow JA-SA-SA-RA-ME, or appear independently?
  2. Analyze sub-sequences (NA-KA, KA-NA, U-NA-KA, NA-SI) for independent occurrences.
  3. Test H3: U-NA-KA-NA-SI is a divine epithet appended to JA-SA-SA-RA-ME.
  4. Test H5 (-ME comitative): -ME tokens consistently appear between two noun-like tokens.
  5. Phonological comparison of U-NA-KA-NA-SI skeleton against Hurrian divine names.

Evidence tier: Tier 3 (Formulaic) for U-NA-KA-NA-SI; Tier 5 (Grammatical) for -ME test.
"""

import json
import re
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/unakana_analysis_2026-03-19.json"

# Support types considered ritual
RITUAL_SUPPORTS = {
    "Stone vessel", "stone vessel",
    "Metal object", "metal object",
    "Architecture", "architecture",
    "Stone", "stone",
    "Libation table", "libation table",
}

# Support types considered administrative
ADMIN_SUPPORTS = {
    "Tablet", "tablet",
    "Nodule", "nodule",
    "Roundel", "roundel",
    "Clay vessel", "clay vessel",
    "Sealing", "sealing",
}

# Known logograms and numerals
LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG", "OVI", "BOS",
    "EQU", "SUS", "CAP", "TELA", "LANA", "AES", "GRA+KU", "GRA+E",
    "GRA+PA", "GRA+SI", "GRA+TE", "OLIV+E", "OLIV+A", "OLIV+KU",
}
NUMERAL_RE = re.compile(r'^[\d/.,½⅓¼⅕]+$')
STRIP_TOKENS = {"𐄁", "↵", "\n", "", " "}


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def is_ritual(record):
    support = record.get("support", "")
    return support in RITUAL_SUPPORTS


def is_admin(record):
    support = record.get("support", "")
    return support in ADMIN_SUPPORTS


def get_token_values(rec):
    """Extract string values from token dicts."""
    raw = rec.get("transliteration_tokens", [])
    return [t.get("value", "") if isinstance(t, dict) else str(t) for t in raw]


def clean_tokens(tokens):
    """Remove structural tokens but keep sequence order."""
    return [t for t in tokens if t not in STRIP_TOKENS and t]


def classify_token(token):
    if token in LOGOGRAMS:
        return "logogram"
    if NUMERAL_RE.match(token):
        return "numeral"
    if token.startswith("*"):
        return "unknown_sign"
    return "syllabic"


# ─── U-NA-KA-NA-SI Analysis ───────────────────────────────────────────────────

TARGET = "U-NA-KA-NA-SI"
TARGET_TOKENS = ["U-NA-KA-NA-SI"]  # Single compound token in corpus

# Sub-sequences to search for independently (as single compound tokens)
# The corpus stores multi-sign words as hyphenated single tokens
SUB_SEQUENCES = {
    "U-NA-KA": ["U-NA-KA"],
    "NA-KA-NA": ["NA-KA-NA"],
    "KA-NA-SI": ["KA-NA-SI"],
    "NA-SI": ["NA-SI"],
    "U-NA": ["U-NA"],
}

# Known Hurrian divine names and epithets (phonological skeleton for comparison)
# Source: Wegner 2007 Hurrian grammar; Mitanni pantheon
HURRIAN_DIVINE_NAMES = {
    "Tessub": "T-S-B",      # Storm god
    "Sauska": "S-K-S",      # Goddess of love (Ishtar)
    "Hebat": "H-B-T",       # Queen of gods
    "Kumarbi": "K-M-R-B",  # Father of gods
    "Simigi": "S-M-G",      # Sun god
    "Kusuh": "K-S-H",       # Moon god
    "Ashtapi": "S-T-P",    # War god
    "Nubadig": "N-B-D",    # Hurrian deity
    "Nabarbi": "N-B-R",    # Hurrian goddess
}

# Known Minoan/Aegean place names in Linear B (phonological skeleton)
LINEAR_B_PLACE_NAMES = {
    "Amnisos": "M-N-S",     # Cretan harbor
    "Knossos": "K-N-S",     # Knossos
    "Phaistos": "P-S-T",    # Phaistos
    "Tylissos": "T-L-S",    # Tylissos
    "Dikte": "D-K-T",       # Mt Dikte
    "Ida": "I-D",           # Mt Ida
    "Zakros": "Z-K-R",      # Zakros
    "Arkhanes": "R-K-N",    # Arkhanes
    "Psykhro": "P-S-K-R",  # Psykhro cave
}


def find_sequence_occurrences(records, target_seq):
    """
    Find all inscriptions containing target_seq.
    target_seq is a list of token strings to find as consecutive tokens.
    Also catches tokens that CONTAIN the target as a substring (compound forms).
    """
    occurrences = []
    target_str = "-".join(target_seq) if len(target_seq) > 1 else target_seq[0]

    for rec in records:
        tokens = clean_tokens(get_token_values(rec))

        # First: exact token match (multi-element sequences)
        for i in range(len(tokens) - len(target_seq) + 1):
            if tokens[i:i + len(target_seq)] == target_seq:
                pre_token = tokens[i - 1] if i > 0 else None
                post_token = tokens[i + len(target_seq)] if i + len(target_seq) < len(tokens) else None
                occurrences.append({
                    "record_id": rec.get("id", "?"),
                    "site": rec.get("site", "?"),
                    "support": rec.get("support", "?"),
                    "scribe": rec.get("scribe", "?"),
                    "is_ritual": is_ritual(rec),
                    "is_admin": is_admin(rec),
                    "match_type": "exact",
                    "position_in_inscription": i,
                    "inscription_length": len(tokens),
                    "relative_position": round(i / len(tokens), 2) if tokens else 0,
                    "preceding_token": pre_token,
                    "following_token": post_token,
                    "full_context": tokens,
                })

        # Also find tokens that CONTAIN the target as substring (compound forms)
        for i, token in enumerate(tokens):
            if (target_str in token and token != target_str and
                    not any(occ["record_id"] == rec.get("id") and occ["position_in_inscription"] == i
                            for occ in occurrences)):
                pre_token = tokens[i - 1] if i > 0 else None
                post_token = tokens[i + 1] if i + 1 < len(tokens) else None
                occurrences.append({
                    "record_id": rec.get("id", "?"),
                    "site": rec.get("site", "?"),
                    "support": rec.get("support", "?"),
                    "scribe": rec.get("scribe", "?"),
                    "is_ritual": is_ritual(rec),
                    "is_admin": is_admin(rec),
                    "match_type": f"substring_in_{token}",
                    "matched_token": token,
                    "position_in_inscription": i,
                    "inscription_length": len(tokens),
                    "relative_position": round(i / len(tokens), 2) if tokens else 0,
                    "preceding_token": pre_token,
                    "following_token": post_token,
                    "full_context": tokens,
                })

    return occurrences


def check_cooccurrence_with(occurrences, target_token, window=5):
    """Check how many occurrences of U-NA-KA-NA-SI co-occur with target_token nearby."""
    co_count = 0
    details = []
    for occ in occurrences:
        context = occ["full_context"]
        pos = occ["position_in_inscription"]
        start = max(0, pos - window)
        end = min(len(context), pos + len(TARGET_TOKENS) + window)
        window_tokens = context[start:end]
        # Check for exact token or substring match
        if target_token in window_tokens or any(target_token in t for t in window_tokens):
            co_count += 1
            details.append(occ["record_id"])
    return co_count, details


def phonological_skeleton(token_sequence):
    """Extract consonant skeleton from a token sequence (list of signs or hyphenated compound)."""
    # If token_sequence is a list with one compound hyphenated token, split it
    if len(token_sequence) == 1 and "-" in token_sequence[0]:
        token_sequence = token_sequence[0].split("-")

    # Map syllabic tokens to their onset consonant
    consonant_map = {
        "A": "", "E": "", "I": "", "O": "", "U": "",
        "NA": "N", "NE": "N", "NI": "N", "NO": "N", "NU": "N",
        "KA": "K", "KE": "K", "KI": "K", "KO": "K", "KU": "K",
        "SA": "S", "SE": "S", "SI": "S", "SO": "S", "SU": "S",
        "TA": "T", "TE": "T", "TI": "T", "TO": "T", "TU": "T",
        "DA": "D", "DE": "D", "DI": "D", "DO": "D", "DU": "D",
        "MA": "M", "ME": "M", "MI": "M", "MO": "M", "MU": "M",
        "RA": "R", "RE": "R", "RI": "R", "RO": "R", "RU": "R",
        "PA": "P", "PE": "P", "PI": "P", "PO": "P", "PU": "P",
        "JA": "J", "JE": "J", "JO": "J", "JU": "J",
        "WA": "W", "WE": "W", "WI": "W", "WO": "W",
        "ZA": "Z", "ZE": "Z", "ZO": "Z",
        "LA": "L", "LE": "L", "LI": "L", "LO": "L", "LU": "L",
    }
    skeleton = ""
    for t in token_sequence:
        c = consonant_map.get(t, "?")
        if c:
            skeleton += c
    return skeleton


# ─── -ME Comitative/Essive Analysis ──────────────────────────────────────────

def analyze_me_suffix(records):
    """Analyze positional neighbors of all -ME tokens."""
    me_occurrences = []

    for rec in records:
        tokens = clean_tokens(get_token_values(rec))
        for i, token in enumerate(tokens):
            if isinstance(token, str) and token.endswith("-ME"):
                pre_token = tokens[i - 1] if i > 0 else None
                post_token = tokens[i + 1] if i + 1 < len(tokens) else None

                pre_class = classify_token(pre_token) if pre_token else "boundary"
                post_class = classify_token(post_token) if post_token else "boundary"

                # Check for comitative pattern: syllabic → ME_token → syllabic
                is_comitative_pattern = (
                    pre_class == "syllabic" and post_class == "syllabic"
                )
                # Check for essive/topic pattern: boundary/nothing → ME_token → logogram/numeral
                is_essive_pattern = (
                    post_class in ("logogram", "numeral")
                )
                # Check for KI-RO/KU-RO nearby
                window_tokens = tokens[max(0, i - 3):min(len(tokens), i + 4)]
                has_kiro = "KI-RO" in window_tokens
                has_kuro = "KU-RO" in window_tokens

                me_occurrences.append({
                    "record_id": rec.get("id", "?"),
                    "site": rec.get("site", "?"),
                    "support": rec.get("support", "?"),
                    "is_ritual": is_ritual(rec),
                    "token": token,
                    "position": i,
                    "inscription_length": len(tokens),
                    "relative_position": round(i / len(tokens), 2) if tokens else 0,
                    "preceding_token": pre_token,
                    "preceding_class": pre_class,
                    "following_token": post_token,
                    "following_class": post_class,
                    "comitative_pattern": is_comitative_pattern,
                    "essive_pattern": is_essive_pattern,
                    "near_kiro": has_kiro,
                    "near_kuro": has_kuro,
                    "window_context": window_tokens,
                })

    return me_occurrences


def summarize_me_analysis(me_occurrences):
    """Summarize -ME suffix analysis for H5."""
    total = len(me_occurrences)
    if total == 0:
        return {"total": 0, "note": "No -ME tokens found"}

    comitative = sum(1 for o in me_occurrences if o["comitative_pattern"])
    essive = sum(1 for o in me_occurrences if o["essive_pattern"])
    ritual = sum(1 for o in me_occurrences if o["is_ritual"])
    near_kiro = sum(1 for o in me_occurrences if o["near_kiro"])
    near_kuro = sum(1 for o in me_occurrences if o["near_kuro"])

    pre_class_dist = Counter(o["preceding_class"] for o in me_occurrences)
    post_class_dist = Counter(o["following_class"] for o in me_occurrences)

    token_types = Counter(o["token"] for o in me_occurrences)

    return {
        "total_occurrences": total,
        "token_types": dict(token_types.most_common()),
        "ritual_count": ritual,
        "ritual_rate": round(ritual / total, 3),
        "comitative_pattern_count": comitative,
        "comitative_pattern_rate": round(comitative / total, 3),
        "essive_pattern_count": essive,
        "essive_pattern_rate": round(essive / total, 3),
        "near_kiro_count": near_kiro,
        "near_kuro_count": near_kuro,
        "preceding_token_class_distribution": dict(pre_class_dist),
        "following_token_class_distribution": dict(post_class_dist),
        "h5_verdict": (
            "COMITATIVE SUPPORTED" if comitative / total > 0.5 else
            "ESSIVE SUPPORTED" if essive / total > 0.4 else
            "INCONCLUSIVE — no dominant pattern"
        ),
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def run():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"  Loaded {len(records)} records")

    # ── U-NA-KA-NA-SI Analysis ──
    print("\nSearching for U-NA-KA-NA-SI occurrences...")
    unakana_occs = find_sequence_occurrences(records, TARGET_TOKENS)
    print(f"  Found {len(unakana_occs)} exact occurrences")

    sites = Counter(o["site"] for o in unakana_occs)
    supports = Counter(o["support"] for o in unakana_occs)
    ritual_count = sum(1 for o in unakana_occs if o["is_ritual"])

    # Check co-occurrence with JA-SA-SA-RA-ME
    co_with_jassarame, jassarame_records = check_cooccurrence_with(unakana_occs, "JA-SA-SA-RA-ME")
    print(f"  Co-occurrences with JA-SA-SA-RA-ME: {co_with_jassarame}/{len(unakana_occs)}")

    # Check co-occurrence with A-TA-I-*301-WA-JA (ritual header)
    co_with_atai, atai_records = check_cooccurrence_with(unakana_occs, "A-TA-I-*301-WA-JA")

    # Sub-sequence analysis
    print("\nSearching for sub-sequences...")
    sub_seq_results = {}
    for name, seq in SUB_SEQUENCES.items():
        occs = find_sequence_occurrences(records, seq)
        ritual_sub = sum(1 for o in occs if o["is_ritual"])
        sites_sub = Counter(o["site"] for o in occs)
        sub_seq_results[name] = {
            "count": len(occs),
            "ritual_count": ritual_sub,
            "ritual_rate": round(ritual_sub / len(occs), 3) if occs else 0,
            "sites": dict(sites_sub.most_common()),
        }
        print(f"  {name}: {len(occs)} occurrences ({ritual_sub} ritual), "
              f"sites: {dict(sites_sub.most_common(3))}")

    # Phonological skeleton analysis
    skeleton = phonological_skeleton(TARGET_TOKENS)
    print(f"\nU-NA-KA-NA-SI phonological skeleton: {skeleton}")

    # Compare against Hurrian divine names
    hurrian_comparisons = []
    for name, h_skeleton in HURRIAN_DIVINE_NAMES.items():
        # Simple overlap score
        overlap = sum(1 for c in skeleton if c in h_skeleton)
        hurrian_comparisons.append({
            "name": name,
            "skeleton": h_skeleton,
            "overlap_chars": overlap,
            "note": f"LA skeleton={skeleton}, Hurrian skeleton={h_skeleton}",
        })

    # Compare against place names
    place_comparisons = []
    for name, p_skeleton in LINEAR_B_PLACE_NAMES.items():
        overlap = sum(1 for c in skeleton if c in p_skeleton)
        place_comparisons.append({
            "name": name,
            "skeleton": p_skeleton,
            "overlap_chars": overlap,
            "note": f"LA skeleton={skeleton}, Place name skeleton={p_skeleton}",
        })

    # ── -ME Analysis ──
    print("\nAnalyzing -ME suffix tokens...")
    me_occurrences = analyze_me_suffix(records)
    me_summary = summarize_me_analysis(me_occurrences)
    print(f"  Total -ME tokens: {me_summary['total_occurrences']}")
    print(f"  Comitative pattern rate: {me_summary['comitative_pattern_rate']:.2%}")
    print(f"  Essive pattern rate: {me_summary['essive_pattern_rate']:.2%}")
    print(f"  H5 verdict: {me_summary['h5_verdict']}")

    # Build result
    result = {
        "metadata": {
            "date": "2026-03-19",
            "analyses": [
                "U-NA-KA-NA-SI occurrence analysis (H3)",
                "Sub-sequence independence test (H3)",
                "Phonological skeleton comparison vs Hurrian/place names (H3)",
                "-ME comitative/essive neighbor test (H5)",
            ],
            "corpus_records": len(records),
        },
        "unakana_analysis": {
            "target": TARGET,
            "total_occurrences": len(unakana_occs),
            "ritual_count": ritual_count,
            "ritual_rate": round(ritual_count / len(unakana_occs), 3) if unakana_occs else 0,
            "sites": dict(sites.most_common()),
            "support_types": dict(supports.most_common()),
            "co_occurrence_with_JA-SA-SA-RA-ME": {
                "count": co_with_jassarame,
                "total": len(unakana_occs),
                "rate": round(co_with_jassarame / len(unakana_occs), 3) if unakana_occs else 0,
                "records": jassarame_records,
            },
            "co_occurrence_with_A-TA-I-*301-WA-JA": {
                "count": co_with_atai,
                "total": len(unakana_occs),
                "rate": round(co_with_atai / len(unakana_occs), 3) if unakana_occs else 0,
            },
            "individual_occurrences": [
                {k: v for k, v in occ.items() if k != "full_context"}
                for occ in unakana_occs
            ],
            "phonological_skeleton": skeleton,
            "hurrian_divine_name_comparisons": sorted(
                hurrian_comparisons, key=lambda x: -x["overlap_chars"]
            ),
            "minoan_place_name_comparisons": sorted(
                place_comparisons, key=lambda x: -x["overlap_chars"]
            ),
            "h3_verdict": (
                "DIVINE EPITHET SUPPORTED — exclusively follows JA-SA-SA-RA-ME"
                if len(unakana_occs) > 0 and co_with_jassarame == len(unakana_occs)
                else "INDEPENDENT OCCURRENCES FOUND — not exclusively dependent on JA-SA-SA-RA-ME"
                if len(unakana_occs) > 0
                else "INSUFFICIENT DATA"
            ),
        },
        "sub_sequence_analysis": sub_seq_results,
        "me_suffix_analysis": {
            "summary": me_summary,
            "individual_occurrences": me_occurrences,
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {OUTPUT_PATH}")

    print("\n=== U-NA-KA-NA-SI SUMMARY ===")
    print(f"  Total occurrences: {len(unakana_occs)}")
    print(f"  Sites: {dict(sites.most_common())}")
    print(f"  Ritual: {ritual_count}/{len(unakana_occs)}")
    print(f"  Co-occurs with JA-SA-SA-RA-ME: {co_with_jassarame}/{len(unakana_occs)}")
    print(f"  H3 verdict: {result['unakana_analysis']['h3_verdict']}")

    print("\n=== -ME SUFFIX SUMMARY ===")
    print(f"  Total: {me_summary['total_occurrences']}")
    print(f"  Ritual rate: {me_summary['ritual_rate']:.2%}")
    print(f"  Comitative pattern: {me_summary['comitative_pattern_rate']:.2%}")
    print(f"  H5 verdict: {me_summary['h5_verdict']}")

    return result


if __name__ == "__main__":
    run()
