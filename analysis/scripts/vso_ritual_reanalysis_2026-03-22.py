"""
VSO Ritual Formula Reanalysis — Attempt #11
============================================
Tests whether Davis (2026) VSO word order model applies to the Linear A ritual
formula: A-TA-I-*301-WA-JA (slot-1/verb) → slot-2 token (subject/dedicant) →
JA-SA-SA-RA-ME / U-NA-KA-NA-SI / etc. (slot-3+ objects).

Key questions:
  1. Is A-TA-I-*301-WA-JA always inscription-initial? (verbal phrase test)
  2. Is slot-2 variable or fixed? (dedicant vs. divine name test)
  3. Do slot-2 tokens show personal name signatures?
  4. Are slot-3+ tokens stable liturgical elements?

Output: analysis/outputs/vso_ritual_reanalysis_2026-03-22.json
"""

import json
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/vso_ritual_reanalysis_2026-03-22.json"

RITUAL_SUPPORTS_LC = {"stone vessel", "metal object", "architecture", "stone object"}

RITUAL_HEADER = "A-TA-I-*301-WA-JA"

# Known ritual sequence elements (established from prior attempts)
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

# Known administrative formula words to exclude from name analysis
KNOWN_ADMIN_WORDS = {"KU-RO", "KI-RO", "A-DU", "PO-TO-KU-RO", "*301", "SA-RA2"}

NAME_SUFFIXES = {"TI", "TA", "TE", "SI", "NA", "JA", "NE", "TU"}


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
    if v in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "100", "1000"}:
        return True
    return False


def is_syllabic(v):
    """Returns True if token looks like a syllabic sequence (not logogram/numeral)."""
    if is_numeral(v):
        return False
    # Logograms are all-caps short words without hyphens OR known logograms
    known_logograms = {"GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "NI",
                       "FIG", "OLIV", "TELA", "LANA", "AES", "*304", "*22F", "*308", "*23M"}
    if v in known_logograms:
        return False
    # Signs starting with * are special signs
    if v.startswith("*") and "-" not in v:
        return False
    return True


def is_ritual_support(rec):
    s = rec.get("support", "").lower().strip()
    return s in RITUAL_SUPPORTS_LC


def get_final_syllable(token):
    parts = token.split("-")
    return parts[-1] if parts else ""


def get_syllable_count(token):
    return len(token.split("-"))


def main():
    records = load_corpus()
    total_records = len(records)
    baseline_ritual = sum(1 for r in records if is_ritual_support(r)) / total_records

    # Step 1: Find all ritual records
    ritual_records = [r for r in records if is_ritual_support(r)]

    # Step 2: Filter to records containing A-TA-I-*301-WA-JA
    header_records = []
    for rec in ritual_records:
        tokens = get_token_values(rec)
        if RITUAL_HEADER in tokens:
            header_records.append((rec, tokens))

    # Also check all records (not just ritual) for this header
    all_header_records = []
    for rec in records:
        tokens = get_token_values(rec)
        if RITUAL_HEADER in tokens:
            all_header_records.append((rec, tokens))

    # Step 3: For each header record — analyze position and extract slot-2
    header_positional_data = []
    slot2_tokens = []
    slot3plus_tokens = []

    for rec, tokens in all_header_records:
        header_idx = tokens.index(RITUAL_HEADER)
        is_initial = (header_idx == 0)

        # Extract slot-2: the token immediately after RITUAL_HEADER
        slot2 = None
        if header_idx + 1 < len(tokens):
            candidate = tokens[header_idx + 1]
            if not is_numeral(candidate):
                slot2 = candidate

        # Extract slot-3+ tokens: all remaining syllabic tokens after slot-2
        slot3_start = header_idx + 2
        slot3_tokens_this = []
        for t in tokens[slot3_start:]:
            if not is_numeral(t):
                slot3_tokens_this.append(t)

        header_positional_data.append({
            "id": rec.get("id", ""),
            "site": rec.get("site", ""),
            "support": rec.get("support", ""),
            "header_position": header_idx,
            "is_initial": is_initial,
            "slot2": slot2,
            "slot3plus": slot3_tokens_this,
            "full_tokens": tokens,
        })

        if slot2:
            slot2_tokens.append(slot2)
        slot3plus_tokens.extend(slot3_tokens_this)

    # Step 4: Compute header-initial rate
    initial_count = sum(1 for d in header_positional_data if d["is_initial"])
    header_count = len(header_positional_data)

    # Step 5: Analyze slot-2 tokens
    slot2_counter = Counter(slot2_tokens)
    slot2_distinct = len(slot2_counter)

    # For each distinct slot-2 token: compute occurrence count, site distribution
    slot2_analysis = {}
    for token, count in slot2_counter.most_common():
        sites = [d["site"] for d in header_positional_data if d["slot2"] == token]
        site_counts = Counter(sites)
        max_site_prop = max(site_counts.values()) / sum(site_counts.values()) if site_counts else 0
        final_syl = get_final_syllable(token)
        syl_count = get_syllable_count(token)

        # Compute this token's total corpus occurrences (not just slot-2)
        total_corpus_occ = 0
        total_corpus_sites = set()
        for rec in records:
            toks = get_token_values(rec)
            if token in toks:
                total_corpus_occ += 1
                total_corpus_sites.add(rec.get("site", ""))

        is_known_ritual = token in KNOWN_RITUAL_ELEMENTS
        is_known_admin = token in KNOWN_ADMIN_WORDS
        has_name_suffix = final_syl in NAME_SUFFIXES

        # Personal name profile: rare in corpus (≤3), site-specific (>0.7), 2–4 syllables
        personal_name_score = 0
        if total_corpus_occ <= 3:
            personal_name_score += 2
        elif total_corpus_occ <= 6:
            personal_name_score += 1
        if max_site_prop >= 0.7:
            personal_name_score += 2
        elif max_site_prop >= 0.5:
            personal_name_score += 1
        if 2 <= syl_count <= 4:
            personal_name_score += 1
        if has_name_suffix:
            personal_name_score += 1
        if is_known_ritual:
            personal_name_score -= 2  # known ritual element = less likely personal name

        slot2_analysis[token] = {
            "slot2_count": count,
            "slot2_sites": dict(site_counts),
            "site_specificity": round(max_site_prop, 3),
            "total_corpus_occurrences": total_corpus_occ,
            "total_corpus_sites": sorted(list(total_corpus_sites)),
            "syllable_count": syl_count,
            "final_syllable": final_syl,
            "has_name_suffix": has_name_suffix,
            "is_known_ritual_element": is_known_ritual,
            "is_known_admin_word": is_known_admin,
            "personal_name_score": personal_name_score,
            "profile": "variable/personal" if personal_name_score >= 3 else
                       ("fixed/divine" if personal_name_score <= 1 else "ambiguous"),
        }

    # Step 6: Analyze slot-3+ elements for stability
    slot3_counter = Counter(slot3plus_tokens)
    known_in_slot3 = {t: c for t, c in slot3_counter.most_common() if t in KNOWN_RITUAL_ELEMENTS}
    unknown_in_slot3 = {t: c for t, c in slot3_counter.most_common() if t not in KNOWN_RITUAL_ELEMENTS}

    # Step 7: Check complementarity — do different slot-2 tokens co-occur in same inscription?
    inscriptions_with_multiple_slot2 = []
    for d in header_positional_data:
        toks = d["full_tokens"]
        found_slot2s = [t for t in toks if t in slot2_counter]
        if len(set(found_slot2s)) > 1:
            inscriptions_with_multiple_slot2.append(d["id"])

    # Step 8: Classify outcome
    if slot2_distinct >= 5:
        slot2_classification = "VARIABLE — consistent with multiple distinct dedicants or divine names"
    elif slot2_distinct <= 2:
        slot2_classification = "FIXED — consistent with a single liturgical element (divine name or title)"
    else:
        slot2_classification = "AMBIGUOUS — 3–4 distinct tokens; could be small set of divine names or local name variants"

    output = {
        "analysis": "Attempt #11: VSO Ritual Formula Reanalysis",
        "date": "2026-03-22",
        "new_information_source": "Davis (2026) in Salgarella & Petrakis, 'The Wor(l)ds of Linear A' — VSO word order from libation formula",
        "corpus_stats": {
            "total_records": total_records,
            "ritual_records": len(ritual_records),
            "baseline_ritual_rate": round(baseline_ritual, 4),
        },
        "header_analysis": {
            "token_searched": RITUAL_HEADER,
            "total_records_containing_header": len(all_header_records),
            "ritual_context_count": len(header_records),
            "non_ritual_context_count": len(all_header_records) - len(header_records),
            "header_at_position_0_count": initial_count,
            "header_initial_rate": round(initial_count / header_count, 3) if header_count else 0,
            "vso_verb_phrase_test": (
                "SUPPORTED" if header_count > 0 and initial_count / header_count >= 0.8
                else ("INCONCLUSIVE" if header_count > 0 and initial_count / header_count >= 0.5
                      else "NOT SUPPORTED" if header_count > 0 else "INSUFFICIENT DATA")
            ),
        },
        "slot2_analysis": {
            "total_slot2_tokens_extracted": len(slot2_tokens),
            "distinct_slot2_tokens": slot2_distinct,
            "slot2_classification": slot2_classification,
            "tokens": slot2_analysis,
            "inscriptions_with_multiple_slot2_types": inscriptions_with_multiple_slot2,
        },
        "slot3plus_analysis": {
            "total_slot3plus_tokens": len(slot3plus_tokens),
            "known_ritual_elements_in_slot3plus": known_in_slot3,
            "unknown_tokens_in_slot3plus": dict(list(unknown_in_slot3.items())[:20]),
            "known_element_coverage": round(
                sum(known_in_slot3.values()) / len(slot3plus_tokens), 3
            ) if slot3plus_tokens else 0,
        },
        "per_inscription_breakdown": header_positional_data,
        "summary": {
            "header_initial_rate": round(initial_count / header_count, 3) if header_count else 0,
            "slot2_distinct_count": slot2_distinct,
            "slot2_classification": slot2_classification,
            "top_slot2_token": slot2_counter.most_common(1)[0] if slot2_counter else None,
            "vso_hypothesis_outcome": (
                "SUPPORTED" if (
                    header_count > 0 and
                    initial_count / header_count >= 0.8 and
                    slot2_distinct >= 3
                ) else "NEEDS FURTHER INVESTIGATION"
            ),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Attempt #11 complete.")
    print(f"  Records containing {RITUAL_HEADER}: {len(all_header_records)}")
    print(f"  Header-initial rate: {initial_count}/{header_count} = "
          f"{initial_count/header_count:.1%}" if header_count else "  No records found.")
    print(f"  Distinct slot-2 tokens: {slot2_distinct}")
    print(f"  Slot-2 classification: {slot2_classification}")
    if slot2_counter:
        print("  Top slot-2 tokens:")
        for tok, cnt in slot2_counter.most_common(5):
            info = slot2_analysis.get(tok, {})
            print(f"    {tok} (count={cnt}, site_spec={info.get('site_specificity', '?')}, "
                  f"profile={info.get('profile', '?')})")


if __name__ == "__main__":
    main()
