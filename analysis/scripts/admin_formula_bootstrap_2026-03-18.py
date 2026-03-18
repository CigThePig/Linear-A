"""
Administrative Formula Bootstrapping Analysis
Linear A Decipherment Project — 2026-03-18

Strategy 1: Use KU-RO ("total") as anchor to find other tokens appearing
in the same structural slot (before terminal numbers in accounting tablets).

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/admin_formula_results_2026-03-18.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/admin_formula_results_2026-03-18.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")

NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈"}


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
    # Pure uppercase abbreviations 2-4 chars are likely logograms
    if re.match(r"^[A-Z]{2,4}$", token):
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_formula_candidate(token):
    """A token that could be an administrative formula word (not numeral/logogram/punct)."""
    if is_numeral(token):
        return False
    if is_logogram(token):
        return False
    if is_punct(token):
        return False
    if len(token) < 2:
        return False
    return True


def analyze_kuro_context(records):
    """
    For every record containing KU-RO, extract the context window:
    - tokens immediately before KU-RO
    - token(s) after KU-RO (should be a number)
    """
    kuro_contexts = []
    for r in records:
        tokens = get_tokens(r)
        for i, tok in enumerate(tokens):
            if tok == "KU-RO":
                pre = tokens[max(0, i - 3):i]
                post = tokens[i + 1:min(len(tokens), i + 3)]
                kuro_contexts.append({
                    "record_id": r["id"],
                    "site": r.get("site"),
                    "support": r.get("support"),
                    "tokens_before": pre,
                    "kuro": tok,
                    "tokens_after": post,
                    "full_tokens": tokens,
                })
    return kuro_contexts


def analyze_kiro_context(records):
    """Same analysis for KI-RO."""
    kiro_contexts = []
    for r in records:
        tokens = get_tokens(r)
        for i, tok in enumerate(tokens):
            if tok == "KI-RO":
                pre = tokens[max(0, i - 3):i]
                post = tokens[i + 1:min(len(tokens), i + 3)]
                kiro_contexts.append({
                    "record_id": r["id"],
                    "site": r.get("site"),
                    "support": r.get("support"),
                    "tokens_before": pre,
                    "kuro": tok,
                    "tokens_after": post,
                })
    return kiro_contexts


def find_terminal_slot_tokens(records):
    """
    For all records: find the LAST numeral in the token sequence.
    Record the token immediately preceding it.
    This is the "closing formula slot".
    """
    terminal_counts = Counter()
    terminal_sites = defaultdict(set)
    terminal_records = defaultdict(list)

    for r in records:
        tokens = get_tokens(r)
        # Find last numeral position
        last_num_idx = -1
        for i in range(len(tokens) - 1, -1, -1):
            if is_numeral(tokens[i]):
                last_num_idx = i
                break
        if last_num_idx > 0:
            prev = tokens[last_num_idx - 1]
            if is_formula_candidate(prev):
                terminal_counts[prev] += 1
                site = r.get("site") or "unknown"
                terminal_sites[prev].add(site)
                if len(terminal_records[prev]) < 5:
                    terminal_records[prev].append(r["id"])

    result = {}
    for token, count in terminal_counts.most_common():
        result[token] = {
            "count": count,
            "site_count": len(terminal_sites[token]),
            "sites": sorted(terminal_sites[token]),
            "example_records": terminal_records[token],
        }
    return result


def find_opening_tokens(records):
    """Record the first non-punct token in each record."""
    opening_counts = Counter()
    opening_sites = defaultdict(set)
    opening_records = defaultdict(list)

    for r in records:
        tokens = get_tokens(r)
        for tok in tokens:
            if not is_punct(tok) and not is_numeral(tok):
                opening_counts[tok] += 1
                site = r.get("site") or "unknown"
                opening_sites[tok].add(site)
                if len(opening_records[tok]) < 3:
                    opening_records[tok].append(r["id"])
                break

    result = {}
    for token, count in opening_counts.most_common(50):
        result[token] = {
            "count": count,
            "site_count": len(opening_sites[token]),
            "sites": sorted(opening_sites[token]),
            "example_records": opening_records[token],
        }
    return result


def find_pre_logogram_tokens(records):
    """
    Identify tokens that appear immediately BEFORE a logogram.
    These are likely the "subject" or "entity name" in [entity] [logogram] [number] pattern.
    """
    pre_logo_counts = defaultdict(Counter)  # logogram -> Counter of preceding tokens
    pre_logo_sites = defaultdict(lambda: defaultdict(set))

    for r in records:
        tokens = get_tokens(r)
        for i in range(1, len(tokens)):
            if is_logogram(tokens[i]) and tokens[i] not in ("KU-RO", "KI-RO"):
                prev = tokens[i - 1]
                if is_formula_candidate(prev):
                    pre_logo_counts[tokens[i]][prev] += 1
                    site = r.get("site") or "unknown"
                    pre_logo_sites[tokens[i]][prev].add(site)

    result = {}
    for logo, counter in pre_logo_counts.items():
        result[logo] = {
            tok: {
                "count": cnt,
                "sites": sorted(pre_logo_sites[logo][tok]),
            }
            for tok, cnt in counter.most_common(20)
        }
    return result


def find_formula_pairs(records):
    """
    Look for bigrams (two consecutive formula-candidate tokens).
    Frequent bigrams that appear at multiple sites are likely multi-word formulas.
    """
    bigram_counts = Counter()
    bigram_sites = defaultdict(set)

    for r in records:
        tokens = get_tokens(r)
        candidates = [t for t in tokens if is_formula_candidate(t)]
        for i in range(len(candidates) - 1):
            bigram = f"{candidates[i]} {candidates[i+1]}"
            bigram_counts[bigram] += 1
            site = r.get("site") or "unknown"
            bigram_sites[bigram].add(site)

    result = {}
    for bigram, count in bigram_counts.most_common(50):
        if count >= 3:
            result[bigram] = {
                "count": count,
                "site_count": len(bigram_sites[bigram]),
                "sites": sorted(bigram_sites[bigram]),
            }
    return result


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    print("Analyzing KU-RO context windows...")
    kuro_contexts = analyze_kuro_context(records)
    print(f"  Found {len(kuro_contexts)} KU-RO occurrences")

    print("Analyzing KI-RO context windows...")
    kiro_contexts = analyze_kiro_context(records)
    print(f"  Found {len(kiro_contexts)} KI-RO occurrences")

    print("Finding terminal-slot tokens (closing formula candidates)...")
    terminal_slots = find_terminal_slot_tokens(records)
    print(f"  Found {len(terminal_slots)} distinct candidate tokens in terminal slot")

    print("Finding opening tokens...")
    opening_tokens = find_opening_tokens(records)

    print("Finding pre-logogram tokens (entity/subject candidates)...")
    pre_logo = find_pre_logogram_tokens(records)

    print("Finding frequent formula bigrams...")
    formula_pairs = find_formula_pairs(records)
    print(f"  Found {len(formula_pairs)} bigrams with 3+ occurrences")

    # Summary stats
    kuro_sites = {ctx["site"] for ctx in kuro_contexts if ctx["site"]}
    kiro_sites = {ctx["site"] for ctx in kiro_contexts if ctx["site"]}

    # Tokens in terminal slot with 3+ sites = strong candidates
    strong_candidates = {
        tok: data for tok, data in terminal_slots.items()
        if data["site_count"] >= 3 and data["count"] >= 5
    }
    print(f"\nStrong closing-formula candidates (3+ sites, 5+ occurrences): {len(strong_candidates)}")
    for tok, data in list(strong_candidates.items())[:15]:
        print(f"  {tok}: count={data['count']}, sites={data['site_count']}, {data['sites'][:5]}")

    output = {
        "corpus_size": len(records),
        "kuro_count": len(kuro_contexts),
        "kuro_sites": sorted(kuro_sites),
        "kiro_count": len(kiro_contexts),
        "kiro_sites": sorted(kiro_sites),
        "kuro_contexts": kuro_contexts[:20],  # sample
        "kiro_contexts": kiro_contexts[:10],  # sample
        "terminal_slot_tokens": terminal_slots,
        "strong_closing_candidates": strong_candidates,
        "opening_tokens": opening_tokens,
        "pre_logogram_tokens": pre_logo,
        "formula_bigrams": formula_pairs,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
