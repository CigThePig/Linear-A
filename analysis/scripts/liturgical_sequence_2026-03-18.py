"""
Liturgical Sequence Confirmation Analysis
Attempt #4 follow-up to Attempt #3.

Tests whether the proposed four-unit sequence JA-SA-SA-RA-ME → U-NA-KA-NA-SI
→ I-PI-NA-MA → SI-RU-TE appears partially or completely in single inscriptions.

Also analyzes A-TA-I-*301-WA-JA (the most frequent ritual-exclusive formula)
for context, structure, and semantic patterns.
"""

import json
from collections import Counter, defaultdict

# ── Load corpus ──────────────────────────────────────────────────────────────
records = []
with open("corpus/linear_a_llm_master.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

# Load RAG chunks for full inscription context
rag_chunks = []
try:
    with open("corpus/linear_a_rag_chunks.jsonl") as f:
        for line in f:
            rag_chunks.append(json.loads(line))
    print(f"Loaded {len(rag_chunks)} RAG chunks.")
except FileNotFoundError:
    print("RAG chunks file not found — using master corpus only.")

print(f"Loaded {len(records)} records.")

def extract_tokens(raw_tokens):
    result = []
    for t in raw_tokens:
        if isinstance(t, dict):
            result.append(t.get("value", ""))
        else:
            result.append(str(t))
    return result

# ── Target sequence elements ──────────────────────────────────────────────────
SEQ_ELEMENTS = ["JA-SA-SA-RA-ME", "U-NA-KA-NA-SI", "I-PI-NA-MA", "SI-RU-TE"]
FORMULA_ATA = "A-TA-I-*301-WA-JA"

# ── Sequence presence analysis ───────────────────────────────────────────────
print("\n── Liturgical Sequence Confirmation ──")
print(f"Target: {' → '.join(SEQ_ELEMENTS)}")

# Check each inscription for presence of sequence elements
sequence_hits = []
for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    token_str = " ".join(tokens)

    present = []
    for elem in SEQ_ELEMENTS:
        if elem in tokens:
            present.append(elem)

    if len(present) >= 2:
        # Check order: elements should appear in the correct order
        positions = {}
        for elem in present:
            idx = tokens.index(elem)
            positions[elem] = idx

        # Verify order is preserved
        ordered = [e for e in SEQ_ELEMENTS if e in positions]
        is_ordered = all(
            positions[ordered[i]] < positions[ordered[i + 1]]
            for i in range(len(ordered) - 1)
        )

        sequence_hits.append({
            "id": rec.get("id", "?"),
            "site": rec.get("site", "?"),
            "support": rec.get("support", "?"),
            "elements_present": present,
            "element_count": len(present),
            "is_ordered": is_ordered,
            "positions": {e: positions[e] for e in present},
            "full_tokens": tokens,
        })

print(f"\nInscriptions with ≥2 sequence elements: {len(sequence_hits)}")
for hit in sorted(sequence_hits, key=lambda x: -x["element_count"]):
    print(f"\n  ID: {hit['id']} | Site: {hit['site']} | Support: {hit['support']}")
    print(f"  Elements present ({hit['element_count']}/4): {hit['elements_present']}")
    print(f"  Order preserved: {hit['is_ordered']}")
    print(f"  Positions: {hit['positions']}")
    if len(hit["full_tokens"]) <= 30:
        print(f"  Full inscription: {' '.join(hit['full_tokens'])}")

# ── Gap analysis: how often do pairs appear in same inscription ───────────────
pair_counts = defaultdict(lambda: {"count": 0, "sites": set()})
for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    site = rec.get("site", "?")
    for i, elem1 in enumerate(SEQ_ELEMENTS):
        for elem2 in SEQ_ELEMENTS[i+1:]:
            if elem1 in tokens and elem2 in tokens:
                key = (elem1, elem2)
                pair_counts[key]["count"] += 1
                pair_counts[key]["sites"].add(site)

print("\n\nPair co-occurrence in single inscriptions:")
print(f"{'Pair':<50} {'Count':>7} {'Sites'}")
print("-" * 80)
for (a, b), data in pair_counts.items():
    print(f"{a} + {b}:{'':<3} {data['count']:>7} {sorted(data['sites'])}")

# ── A-TA-I-*301-WA-JA full analysis ─────────────────────────────────────────
print(f"\n── A-TA-I-*301-WA-JA Analysis ──")
ata_records = [r for r in records if FORMULA_ATA in extract_tokens(r.get("transliteration_tokens", []))]
print(f"Total occurrences: {len(ata_records)}")

# Support types
ata_supports = Counter(r.get("support", "?") for r in ata_records)
print(f"Support types: {dict(ata_supports)}")

# Sites
ata_sites = Counter(r.get("site", "?") for r in ata_records)
print(f"Sites: {dict(ata_sites)}")

# Companion tokens: what appears before and after A-TA-I-*301-WA-JA?
ata_pre_tokens = Counter()
ata_post_tokens = Counter()
ata_inscriptions = []

for rec in ata_records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    idx = tokens.index(FORMULA_ATA)

    pre_window = tokens[max(0, idx-3):idx]
    post_window = tokens[idx+1:idx+4]

    for t in pre_window:
        if t.strip():
            ata_pre_tokens[t] += 1
    for t in post_window:
        if t.strip():
            ata_post_tokens[t] += 1

    ata_inscriptions.append({
        "id": rec.get("id", "?"),
        "site": rec.get("site", "?"),
        "support": rec.get("support", "?"),
        "position_in_inscription": idx,
        "inscription_length": len(tokens),
        "pre_window": pre_window,
        "post_window": post_window,
        "position_type": "initial" if idx == 0 else ("final" if idx == len(tokens)-1 else "medial"),
    })

print(f"\nPosition distribution:")
positions = Counter(r["position_type"] for r in ata_inscriptions)
print(f"  {dict(positions)}")

print(f"\nMost common tokens BEFORE A-TA-I-*301-WA-JA:")
for tok, count in ata_pre_tokens.most_common(10):
    print(f"  {tok}: {count}")

print(f"\nMost common tokens AFTER A-TA-I-*301-WA-JA:")
for tok, count in ata_post_tokens.most_common(10):
    print(f"  {tok}: {count}")

# Full inscription listing
print(f"\nAll A-TA-I-*301-WA-JA inscriptions:")
for r in sorted(ata_inscriptions, key=lambda x: x["site"]):
    print(f"  {r['id']} [{r['site']}, {r['support']}] pos={r['position_in_inscription']} pre={r['pre_window']} post={r['post_window']}")

# ── *301 sign standalone analysis ─────────────────────────────────────────────
print(f"\n── *301 Sign Analysis ──")
sign_301_records = [
    r for r in records
    if any("*301" in t for t in extract_tokens(r.get("transliteration_tokens", [])))
]
print(f"Records containing *301 in any token: {len(sign_301_records)}")

# Tokens containing *301
tokens_with_301 = Counter()
for rec in sign_301_records:
    for t in extract_tokens(rec.get("transliteration_tokens", [])):
        if "*301" in t:
            tokens_with_301[t] += 1

print(f"\nTokens containing *301:")
for tok, count in tokens_with_301.most_common():
    print(f"  {tok}: {count}")

# What are the most common contexts for *301 standalone?
standalone_301 = [
    r for r in records
    if "*301" in extract_tokens(r.get("transliteration_tokens", []))
]
print(f"\n*301 as standalone token: {len(standalone_301)} records")
if standalone_301:
    standalone_sites = Counter(r.get("site", "?") for r in standalone_301)
    standalone_supports = Counter(r.get("support", "?") for r in standalone_301)
    print(f"Sites: {dict(standalone_sites.most_common(5))}")
    print(f"Supports: {dict(standalone_supports.most_common(5))}")

# Is *301 always initial?
init_count = 0
non_init_count = 0
for rec in sign_301_records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    for i, t in enumerate(tokens):
        if "*301" in t:
            if i == 0:
                init_count += 1
            else:
                non_init_count += 1

print(f"\n*301 position: initial={init_count}, non-initial={non_init_count}")

# ── JA-SA-SA-RA root analysis ─────────────────────────────────────────────────
# What if JA-SA-SA-RA is the root and -ME is a suffix?
# Find tokens starting with JA-SA-SA-RA to see if bare root appears
print(f"\n── JA-SA-SA-RA Root Analysis ──")
jasasara_variants = Counter()
for rec in records:
    for tok in extract_tokens(rec.get("transliteration_tokens", [])):
        if tok.startswith("JA-SA-SA-RA"):
            jasasara_variants[tok] += 1

print(f"Tokens starting with JA-SA-SA-RA:")
for tok, count in jasasara_variants.most_common():
    print(f"  {tok}: {count}")

# ── Save results ──────────────────────────────────────────────────────────────
output = {
    "sequence_target": SEQ_ELEMENTS,
    "inscriptions_with_2plus_elements": [
        {k: v for k, v in h.items() if k != "full_tokens"}  # omit raw tokens for brevity
        for h in sequence_hits
    ],
    "pair_cooccurrence": {
        f"{a}+{b}": {"count": d["count"], "sites": sorted(d["sites"])}
        for (a, b), d in pair_counts.items()
    },
    "ata_formula_analysis": {
        "total_occurrences": len(ata_records),
        "support_distribution": dict(ata_supports),
        "site_distribution": dict(ata_sites),
        "position_distribution": dict(positions),
        "most_common_pre_tokens": ata_pre_tokens.most_common(10),
        "most_common_post_tokens": ata_post_tokens.most_common(10),
        "all_occurrences": ata_inscriptions,
    },
    "sign_301_analysis": {
        "records_with_301": len(sign_301_records),
        "tokens_with_301": dict(tokens_with_301),
        "standalone_records": len(standalone_301),
        "position_initial": init_count,
        "position_non_initial": non_init_count,
    },
    "jasasara_variants": dict(jasasara_variants),
}

with open("analysis/outputs/liturgical_sequence_2026-03-18.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved: analysis/outputs/liturgical_sequence_2026-03-18.json")
