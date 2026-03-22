"""
PA-RE Luwian Particle Test — Attempt #12
=========================================
Tests whether PA-RE is a Luwian loanword particle (*pari* = "forth/away")
based on Nepal & Perono Cacciafoco (2024) MDPI Information 15:2:73.

Tests:
  1. PA-RE occurrence count, site distribution, support types
  2. Positional profile: inscription-initial, pre-logogram, post-numeral rates
  3. Numeral-after rate (high = logogram candidate; low = particle/function word)
  4. Site-specificity (if HT-only = not a universal particle)
  5. Context window: what co-occurs with PA-RE?
  6. Consonant skeleton [p,r] comparison with other tokens

Output: analysis/outputs/pa_re_particle_test_2026-03-22.json
"""

import json
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/pa_re_particle_test_2026-03-22.json"

TARGET_TOKEN = "PA-RE"
TARGET_SKEL = frozenset(["P", "R"])  # consonant skeleton of PA-RE / Luwian pari

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "NI",
    "*304", "*22F", "*308", "*23M", "FIG", "TELA", "LANA", "AES",
    "GRA+TE", "GRA+QE", "OLE+KI",
}

KNOWN_FORMULA_WORDS = {"KU-RO", "KI-RO", "A-DU", "PO-TO-KU-RO"}

RITUAL_SUPPORTS_LC = {"stone vessel", "metal object", "architecture", "stone object"}


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


def get_consonant_skeleton(token):
    """Extract consonant skeleton from a syllabic token: keep first consonant of each syllable."""
    SYLLABLE_CONSONANTS = {
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
    }
    parts = token.split("-")
    skeleton = []
    for p in parts:
        c = SYLLABLE_CONSONANTS.get(p.upper())
        if c:
            skeleton.append(c)
    return frozenset(skeleton)


def main():
    records = load_corpus()
    total_records = len(records)
    baseline_ritual = sum(1 for r in records if is_ritual_support(r)) / total_records

    # Step 1: Find all PA-RE occurrences (standalone and in compounds)
    # Standalone: exact match "PA-RE"
    # In compound: token contains "-PA-RE" or "PA-RE-" or starts/ends with it

    standalone_records = []    # records with standalone PA-RE token
    compound_records = []      # records with PA-RE as sub-sequence in longer token
    compound_tokens = []       # the compound tokens themselves

    for rec in records:
        tokens = get_token_values(rec)
        has_standalone = TARGET_TOKEN in tokens
        has_compound = any(
            TARGET_TOKEN in t and t != TARGET_TOKEN
            for t in tokens
        )
        if has_standalone:
            standalone_records.append((rec, tokens))
        if has_compound:
            for t in tokens:
                if TARGET_TOKEN in t and t != TARGET_TOKEN:
                    compound_tokens.append(t)
            compound_records.append((rec, tokens))

    # Step 2: Positional analysis for standalone PA-RE
    if not standalone_records:
        print("PA-RE standalone: 0 occurrences in corpus.")
        output = {
            "analysis": "Attempt #12: PA-RE Luwian Particle Test",
            "date": "2026-03-22",
            "new_information_source": "Nepal & Perono Cacciafoco (2024) MDPI Information 15:2:73",
            "target_token": TARGET_TOKEN,
            "standalone_occurrences": 0,
            "compound_tokens": list(set(compound_tokens)),
            "conclusion": {
                "hypothesis_status": "INSUFFICIENT DATA",
                "reason": "PA-RE appears 0 times as standalone token",
                "compound_token_count": len(set(compound_tokens)),
            }
        }
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        return

    # Positional stats
    site_counter = Counter()
    support_counter = Counter()
    position_stats = {
        "record_initial": 0,      # PA-RE at position 0
        "pre_logogram": 0,        # PA-RE followed by a logogram
        "post_numeral": 0,        # PA-RE preceded by a numeral
        "numeral_after": 0,       # PA-RE followed by a numeral
        "total_token_occurrences": 0,
        "kuro_cooccurrence": 0,
        "kiro_cooccurrence": 0,
    }
    context_before = Counter()
    context_after = Counter()
    record_list = []

    for rec, tokens in standalone_records:
        site = rec.get("site", "unknown")
        support = rec.get("support", "unknown")
        site_counter[site] += 1
        support_counter[support] += 1

        if "KU-RO" in tokens:
            position_stats["kuro_cooccurrence"] += 1
        if "KI-RO" in tokens:
            position_stats["kiro_cooccurrence"] += 1

        for i, t in enumerate(tokens):
            if t == TARGET_TOKEN:
                position_stats["total_token_occurrences"] += 1

                if i == 0:
                    position_stats["record_initial"] += 1

                # Token before
                prev_tok = tokens[i - 1] if i > 0 else "<START>"
                context_before[prev_tok] += 1
                if is_numeral(prev_tok):
                    position_stats["post_numeral"] += 1

                # Token after
                next_tok = tokens[i + 1] if i + 1 < len(tokens) else "<END>"
                context_after[next_tok] += 1
                if is_numeral(next_tok):
                    position_stats["numeral_after"] += 1
                if next_tok in KNOWN_LOGOGRAMS:
                    position_stats["pre_logogram"] += 1

        record_list.append({
            "id": rec.get("id", ""),
            "site": site,
            "support": support,
            "tokens": tokens,
        })

    n_recs = len(standalone_records)
    n_toks = position_stats["total_token_occurrences"]

    site_specificity = max(site_counter.values()) / sum(site_counter.values()) if site_counter else 0
    dominant_site = site_counter.most_common(1)[0][0] if site_counter else "N/A"
    numeral_after_rate = position_stats["numeral_after"] / n_toks if n_toks else 0
    record_initial_rate = position_stats["record_initial"] / n_toks if n_toks else 0
    pre_logogram_rate = position_stats["pre_logogram"] / n_toks if n_toks else 0
    ritual_count = sum(1 for rec, _ in standalone_records if is_ritual_support(rec))
    ritual_enrichment = (ritual_count / n_recs) / baseline_ritual if baseline_ritual else None

    # Step 3: Evaluate particle hypothesis
    particle_criteria = {
        "site_count": len(site_counter),
        "site_specificity": round(site_specificity, 3),
        "site_confined": site_specificity > 0.8,
        "numeral_after_rate": round(numeral_after_rate, 3),
        "logogram_profile": numeral_after_rate > 0.6,
        "record_initial_rate": round(record_initial_rate, 3),
        "pre_logogram_rate": round(pre_logogram_rate, 3),
        "particle_profile": (
            not (site_specificity > 0.8) and         # multi-site
            numeral_after_rate < 0.6 and              # not a logogram
            record_initial_rate > 0.1                 # some initial enrichment
        ),
    }

    # Hypothesis assessment
    if n_recs < 3:
        hyp_status = "INSUFFICIENT DATA (< 3 records)"
    elif particle_criteria["site_confined"]:
        hyp_status = "NOT SUPPORTED — PA-RE is site-confined (cannot be universal particle)"
    elif particle_criteria["logogram_profile"]:
        hyp_status = "NOT SUPPORTED — PA-RE shows logogram profile (high numeral-after rate)"
    elif particle_criteria["particle_profile"]:
        hyp_status = "SUPPORTED — PA-RE matches particle/function word profile"
    else:
        hyp_status = "INCONCLUSIVE — meets some but not all particle criteria"

    # Step 4: Consonant skeleton [P,R] comparison — find other tokens with same skeleton
    all_tokens_counter = Counter()
    for rec in records:
        for t in get_token_values(rec):
            all_tokens_counter[t] += 1

    pr_skeleton_tokens = {}
    for tok, cnt in all_tokens_counter.items():
        if "-" in tok:  # only syllabic tokens
            skel = get_consonant_skeleton(tok)
            if skel == TARGET_SKEL:
                pr_skeleton_tokens[tok] = cnt

    output = {
        "analysis": "Attempt #12: PA-RE Luwian Particle Test",
        "date": "2026-03-22",
        "new_information_source": "Nepal & Perono Cacciafoco (2024) MDPI Information 15:2:73",
        "target_token": TARGET_TOKEN,
        "standalone_record_count": n_recs,
        "standalone_token_occurrences": n_toks,
        "site_distribution": dict(site_counter.most_common()),
        "support_distribution": dict(support_counter.most_common()),
        "ritual_enrichment": round(ritual_enrichment, 2) if ritual_enrichment else None,
        "positional_stats": {
            "record_initial_rate": round(record_initial_rate, 3),
            "numeral_after_rate": round(numeral_after_rate, 3),
            "pre_logogram_rate": round(pre_logogram_rate, 3),
            "post_numeral_rate": round(position_stats["post_numeral"] / n_toks, 3) if n_toks else 0,
            "kuro_cooccurrence_rate": round(position_stats["kuro_cooccurrence"] / n_recs, 3),
            "kiro_cooccurrence_rate": round(position_stats["kiro_cooccurrence"] / n_recs, 3),
        },
        "context_before_top10": dict(context_before.most_common(10)),
        "context_after_top10": dict(context_after.most_common(10)),
        "particle_criteria": particle_criteria,
        "compound_tokens_containing_pa_re": dict(Counter(compound_tokens).most_common()),
        "tokens_with_pr_consonant_skeleton": dict(sorted(pr_skeleton_tokens.items(),
                                                          key=lambda x: -x[1])[:20]),
        "record_details": record_list,
        "conclusion": {
            "hypothesis_status": hyp_status,
            "site_count": len(site_counter),
            "dominant_site": dominant_site,
            "numeral_after_rate": round(numeral_after_rate, 3),
            "record_initial_rate": round(record_initial_rate, 3),
            "luwian_pari_match_assessment": (
                "Possible loanword" if hyp_status.startswith("SUPPORTED") else
                "Not supported by positional distribution"
            ),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Attempt #12 (PA-RE) complete.")
    print(f"  Standalone PA-RE records: {n_recs} across {len(site_counter)} sites")
    print(f"  Token occurrences: {n_toks}")
    print(f"  Site distribution: {dict(site_counter.most_common(5))}")
    print(f"  Numeral-after rate: {numeral_after_rate:.1%}")
    print(f"  Record-initial rate: {record_initial_rate:.1%}")
    print(f"  Pre-logogram rate: {pre_logogram_rate:.1%}")
    print(f"  Site-confined (>80% one site): {particle_criteria['site_confined']}")
    print(f"  Hypothesis: {hyp_status}")


if __name__ == "__main__":
    main()
