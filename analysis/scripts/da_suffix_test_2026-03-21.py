"""
-DA and -NE Suffix Test — H9d
Tests whether -DA suffix shows a distribution profile compatible with Hurrian
dative case marker -da, and whether -NE shows nominative plural behavior.

Compares against established profiles:
  -JA: absolutive (low KI-RO, word-initial bias, ritual-neutral)
  -RU: ergative candidate (word-terminal, moderate KI-RO, VIR co-occurrence)
  -TE: directive (20 sites, 3x ritual enrichment)
  -RE: accounting participant (highest KU-RO rate 19%)

Output: analysis/outputs/da_suffix_test_2026-03-21.json
"""

import json
from collections import defaultdict

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/da_suffix_test_2026-03-21.json"

# Previously characterized suffixes for comparison
KNOWN_SUFFIXES = {
    "-JA": {"kiro_rate": 0.0, "kuro_rate": None, "ritual_enrichment": 1.0, "word_terminal": 0.41, "vir_rate": 0.103, "sites": 17},
    "-RU": {"kiro_rate": 0.133, "kuro_rate": None, "ritual_enrichment": None, "word_terminal": 0.722, "vir_rate": 0.133, "sites": 5},
    "-TE": {"kiro_rate": None, "kuro_rate": None, "ritual_enrichment": 3.04, "word_terminal": None, "vir_rate": None, "sites": 20},
    "-RE": {"kiro_rate": None, "kuro_rate": 0.190, "ritual_enrichment": None, "word_terminal": None, "vir_rate": None, "sites": None},
}

SUFFIXES_TO_TEST = ["-DA", "-NE"]

RITUAL_SUPPORTS = {"stone vessel", "metal object", "stone object"}

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

def ends_with_suffix(token, suffix):
    """Check if token ends with the given suffix syllable."""
    suffix_syl = suffix.lstrip("-")
    parts = token.split("-")
    return len(parts) >= 2 and parts[-1] == suffix_syl

def has_vir(tokens):
    """Check if token list contains VIR or VIR compound."""
    return any("VIR" in t for t in tokens)

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
    sup = (rec.get("support") or "").lower()
    return any(x in sup for x in ["stone vessel", "metal", "stone object", "libation"])

def is_administrative(rec):
    sup = (rec.get("support") or "").lower()
    return any(x in sup for x in ["tablet", "roundel", "nodule", "clay"])

def load_corpus():
    records = []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def analyze_suffix(suffix, records, baseline_stats):
    syl = suffix.lstrip("-")
    suffix_tokens = defaultdict(list)  # token -> list of (record_id, site, position_in_seq)

    # Collect all tokens ending with this suffix and their contexts
    suffix_record_ids = set()
    suffix_sites = set()
    total_suffix_tokens = 0
    word_terminal_count = 0   # token is the last non-numeral before a numeral or end of sequence
    kiro_records = set()
    kuro_records = set()
    ritual_records = set()
    admin_records = set()
    vir_records = set()
    all_record_ids_with_suffix = set()

    sample_contexts = []

    for rec in records:
        rid = rec.get("id", "")
        site = rec.get("site", "") or "unknown"
        tokens = get_token_values(rec)
        is_ritual = is_ritual_support(rec)
        is_admin = is_administrative(rec)
        rec_has_kiro = "KI-RO" in tokens
        rec_has_kuro = "KU-RO" in tokens
        rec_has_vir = has_vir(tokens)

        found_in_rec = False
        for i, tok in enumerate(tokens):
            if not ends_with_suffix(tok, suffix):
                continue
            # Multi-sign tokens only (e.g., exclude bare syllable 'DA' if testing -DA)
            parts = tok.split("-")
            if len(parts) < 2:
                continue

            total_suffix_tokens += 1
            found_in_rec = True
            suffix_sites.add(site)

            # Word-terminal: token is followed only by numerals, other logograms, or end of sequence
            is_terminal = True
            for j in range(i + 1, len(tokens)):
                nxt = tokens[j]
                if nxt in ("𐄁", "≈", "—", "\n", "\\n"):
                    continue
                if is_numeral(nxt):
                    break
                # Check if nxt is a syllabic token (not numeral, not punctuation)
                is_terminal = False
                break
            if is_terminal:
                word_terminal_count += 1

            if len(sample_contexts) < 8:
                ctx = tokens[max(0, i-2):i+4]
                sample_contexts.append({"record": rid, "site": site, "token": tok, "context": ctx})

        if found_in_rec:
            all_record_ids_with_suffix.add(rid)
            if rec_has_kiro:
                kiro_records.add(rid)
            if rec_has_kuro:
                kuro_records.add(rid)
            if is_ritual:
                ritual_records.add(rid)
            if is_admin:
                admin_records.add(rid)
            if rec_has_vir:
                vir_records.add(rid)

    n = len(all_record_ids_with_suffix)
    if n == 0:
        return {"suffix": suffix, "error": "no tokens found"}

    kiro_rate = len(kiro_records) / n
    kuro_rate = len(kuro_records) / n
    ritual_rate = len(ritual_records) / n
    ritual_enrichment = ritual_rate / baseline_stats["ritual_rate"] if baseline_stats["ritual_rate"] > 0 else 0
    vir_rate = len(vir_records) / n
    word_terminal_rate = word_terminal_count / total_suffix_tokens if total_suffix_tokens > 0 else 0

    # Get unique suffix tokens (distinct words ending with this suffix)
    unique_tokens = set()
    for rec in records:
        for tok in get_token_values(rec):
            if ends_with_suffix(tok, suffix) and len(tok.split("-")) >= 2:
                unique_tokens.add(tok)

    print(f"\n=== Suffix {suffix} ===")
    print(f"  Records with suffix: {n}")
    print(f"  Total suffix token occurrences: {total_suffix_tokens}")
    print(f"  Unique tokens with suffix: {len(unique_tokens)}")
    print(f"  Sites: {len(suffix_sites)} — {sorted(suffix_sites)[:6]}")
    print(f"  KI-RO co-occurrence rate: {kiro_rate:.3f} (compare -JA: 0.000, -RU: 0.133)")
    print(f"  KU-RO co-occurrence rate: {kuro_rate:.3f} (compare -RE: 0.190)")
    print(f"  Ritual enrichment: {ritual_enrichment:.2f}x (compare -TE: 3.04x, -JA: 1.0x)")
    print(f"  VIR co-occurrence rate: {vir_rate:.3f} (compare -JA: 0.103, -RU: 0.133)")
    print(f"  Word-terminal rate: {word_terminal_rate:.3f} (compare -RU: 0.722, -JA: 0.41)")
    print(f"  Sample tokens: {sorted(unique_tokens)[:10]}")
    print(f"  Sample contexts:")
    for sc in sample_contexts[:5]:
        print(f"    [{sc['record']}] {sc['site']}: {sc['context']}")

    # Hurrian alignment assessment
    hurrian_dative_profile = {
        "word_terminal": "> 0.5",
        "kiro_rate": "< 0.1",
        "ritual_enrichment": "< 2.0 (dative is administrative, not ritual)",
        "vir_rate": "could vary",
        "interpretation": "Entity receiving action (dative); should appear in administrative receipts"
    }

    hurrian_plural_nominative_profile = {
        "interpretation": "-NE: nominative plural marker",
        "expected": "appears with VIR (person-plural contexts), low ritual, moderate site count"
    }

    return {
        "suffix": suffix,
        "records_with_suffix": n,
        "total_suffix_token_occurrences": total_suffix_tokens,
        "unique_token_count": len(unique_tokens),
        "unique_tokens_list": sorted(unique_tokens)[:20],
        "site_count": len(suffix_sites),
        "sites": sorted(suffix_sites),
        "kiro_rate": round(kiro_rate, 4),
        "kuro_rate": round(kuro_rate, 4),
        "ritual_rate": round(ritual_rate, 4),
        "ritual_enrichment": round(ritual_enrichment, 3),
        "vir_rate": round(vir_rate, 4),
        "word_terminal_rate": round(word_terminal_rate, 4),
        "sample_contexts": sample_contexts,
        "hurrian_profile_expected": hurrian_dative_profile if suffix == "-DA" else hurrian_plural_nominative_profile,
    }

def main():
    records = load_corpus()
    print(f"Loaded {len(records)} records")

    total_records = len(records)
    ritual_count = sum(1 for r in records if is_ritual_support(r))
    baseline_stats = {
        "ritual_rate": ritual_count / total_records,
        "total_records": total_records,
    }

    print(f"Baseline ritual rate: {baseline_stats['ritual_rate']:.3f}")

    results = {}
    for suffix in SUFFIXES_TO_TEST:
        result = analyze_suffix(suffix, records, baseline_stats)
        results[suffix] = result

    # Comparison table
    print("\n=== COMPARISON TABLE ===")
    headers = ["Suffix", "Records", "Sites", "KI-RO%", "KU-RO%", "Ritual_x", "VIR%", "Terminal%"]
    print(f"  {'Suffix':<8} {'Records':<8} {'Sites':<6} {'KI-RO%':<8} {'KU-RO%':<8} {'Ritual_x':<10} {'VIR%':<6} {'Terminal%'}")

    # Known baselines
    baselines = [
        ("-JA",   "?", 17, "0.0",  "?",    "1.0x",  "10.3", "41.0"),
        ("-RU",   "?",  5, "13.3", "?",    "?",     "13.3", "72.2"),
        ("-TE",   "?", 20, "?",    "?",    "3.04x", "?",    "?"),
        ("-RE",   "?", "?", "?",   "19.0", "?",     "?",    "?"),
    ]
    for row in baselines:
        print(f"  {row[0]:<8} {str(row[1]):<8} {str(row[2]):<6} {row[3]:<8} {row[4]:<8} {row[5]:<10} {row[6]:<6} {row[7]}")

    for suf, res in results.items():
        if "error" in res:
            continue
        print(f"  {suf:<8} {res['records_with_suffix']:<8} {res['site_count']:<6} "
              f"{res['kiro_rate']*100:.1f}%    {res['kuro_rate']*100:.1f}%     "
              f"{res['ritual_enrichment']:.2f}x      {res['vir_rate']*100:.1f}%   "
              f"{res['word_terminal_rate']*100:.1f}%")

    output = {
        "analysis": "da_suffix_test",
        "date": "2026-03-21",
        "corpus_records": total_records,
        "baseline_ritual_rate": baseline_stats["ritual_rate"],
        "known_suffix_profiles_for_comparison": KNOWN_SUFFIXES,
        "results": results,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
