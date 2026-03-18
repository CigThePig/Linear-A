"""
-ME Suffix Analysis and Ergative Marker Search
Attempt #4: Follow-up to Attempt #3 open questions.

Part 1: -ME suffix has 3.01x ritual enrichment — what grammatical function does it serve?
Part 2: If -JA is the absolutive/intransitive marker, the ergative marker should be
        identifiable as having an inverse profile (high KI-RO, word-final, transitive agent position).
"""

import json
from collections import Counter, defaultdict

# ── Load corpus ──────────────────────────────────────────────────────────────
records = []
with open("corpus/linear_a_llm_master.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

print(f"Loaded {len(records)} records.")

def extract_tokens(raw_tokens):
    result = []
    for t in raw_tokens:
        if isinstance(t, dict):
            result.append(t.get("value", ""))
        else:
            result.append(str(t))
    return result

LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "KU-RO", "KI-RO",
    "FIC", "FAR", "OVI", "BOS", "EQU", "SUS", "TELA", "LANA", "AROM",
    "NI", "QE", "ZE",
}
NUMERAL_PATTERNS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                    "20", "30", "40", "50", "100", "200", "300", "1000"}
RITUAL_SUPPORTS = {"stone vessel", "metal object", "architecture", "stone object"}


def is_syllabic(token: str) -> bool:
    if not token or not token.strip():
        return False
    t = token.strip()
    if t in LOGOGRAMS:
        return False
    if t in NUMERAL_PATTERNS:
        return False
    return any(c.isalpha() for c in t)


def get_suffix(token: str) -> str | None:
    parts = token.split("-")
    if len(parts) < 2:
        return None
    last = parts[-1].upper()
    if not any(c.isalpha() for c in last):
        return None
    return f"-{last}"


# ── Part 1: -ME suffix deep analysis ────────────────────────────────────────
print("\n═══════════════════════════════════════")
print("PART 1: -ME Suffix Analysis")
print("═══════════════════════════════════════")

ME_SUFFIX = "-ME"
me_tokens = []
me_records = []

for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    site = rec.get("site", "?")
    support = rec.get("support", "?")
    is_ritual = support in RITUAL_SUPPORTS
    has_kuro = "KU-RO" in tokens
    has_kiro = "KI-RO" in tokens

    syllabics = [t for t in tokens if is_syllabic(t)]

    for i, tok in enumerate(tokens):
        if not is_syllabic(tok):
            continue
        suf = get_suffix(tok)
        if suf != ME_SUFFIX:
            continue

        # What is immediately after this -ME token in the full token list?
        next_tokens = []
        for j in range(i + 1, min(i + 4, len(tokens))):
            next_tokens.append(tokens[j])

        # What is immediately before?
        prev_tokens = []
        for j in range(max(0, i - 3), i):
            prev_tokens.append(tokens[j])

        # Position in syllabic sequence
        syl_pos = syllabics.index(tok) if tok in syllabics else -1
        syl_count = len(syllabics)

        me_tokens.append({
            "token": tok,
            "site": site,
            "support": support,
            "is_ritual": is_ritual,
            "has_kuro": has_kuro,
            "has_kiro": has_kiro,
            "prev_3": prev_tokens,
            "next_3": next_tokens,
            "syl_position": syl_pos,
            "syl_total": syl_count,
            "position_type": "initial" if syl_pos == 0 else ("final" if syl_pos == syl_count - 1 else "medial"),
            "record_id": rec.get("id", "?"),
        })

print(f"Total -ME token occurrences: {len(me_tokens)}")

# Token type distribution
me_token_types = Counter(m["token"] for m in me_tokens)
print(f"\n-ME token types ({len(me_token_types)} distinct):")
for tok, count in me_token_types.most_common(15):
    print(f"  {tok}: {count}")

# Register distribution
ritual_count = sum(1 for m in me_tokens if m["is_ritual"])
admin_count = len(me_tokens) - ritual_count
print(f"\nRegister: ritual={ritual_count}, admin={admin_count}, ratio={ritual_count/max(admin_count, 1):.2f}x")

# Position distribution
pos_dist = Counter(m["position_type"] for m in me_tokens)
print(f"\nPosition: {dict(pos_dist)}")

# KU-RO / KI-RO context
kuro_count = sum(1 for m in me_tokens if m["has_kuro"])
kiro_count = sum(1 for m in me_tokens if m["has_kiro"])
print(f"\nAccounting context: KU-RO co-occurrence={kuro_count} ({kuro_count/len(me_tokens):.2%}), KI-RO={kiro_count} ({kiro_count/len(me_tokens):.2%})")

# What follows -ME tokens?
next_token_types = Counter()
for m in me_tokens:
    for t in m["next_3"]:
        if t.strip():
            next_token_types[t] += 1

print(f"\nMost common tokens FOLLOWING -ME words:")
for tok, count in next_token_types.most_common(15):
    print(f"  {tok}: {count}")

# What precedes -ME tokens?
prev_token_types = Counter()
for m in me_tokens:
    for t in m["prev_3"]:
        if t.strip():
            prev_token_types[t] += 1

print(f"\nMost common tokens PRECEDING -ME words:")
for tok, count in prev_token_types.most_common(15):
    print(f"  {tok}: {count}")

# Site distribution
site_dist = Counter(m["site"] for m in me_tokens)
print(f"\nSite distribution:")
for site, count in site_dist.most_common(10):
    print(f"  {site}: {count}")

# Are -ME tokens standalone (single-syllable root + -ME)?
two_part = sum(1 for m in me_tokens if len(m["token"].split("-")) == 2)
longer = sum(1 for m in me_tokens if len(m["token"].split("-")) > 2)
print(f"\nToken structure: two-part (X-ME)={two_part}, longer (X-Y-ME)={longer}")

# Is -ME in JA-SA-SA-RA-ME a grammatical suffix (detachable) or integral?
# Test: are there any other JA-SA-SA-RA-X patterns where X ≠ ME?
print(f"\nJA-SA-SA-RA variants (is -ME the only termination?):")
jasasara_tok = Counter()
for rec in records:
    for tok in extract_tokens(rec.get("transliteration_tokens", [])):
        if tok.startswith("JA-SA-SA-RA"):
            jasasara_tok[tok] += 1
for tok, count in jasasara_tok.most_common():
    print(f"  {tok}: {count}")


# ── Part 2: Ergative Marker Search ─────────────────────────────────────────
print("\n═══════════════════════════════════════")
print("PART 2: Ergative Marker Search")
print("═══════════════════════════════════════")
print("Profile of -JA (absolutive, known):")
print("  - Zero KI-RO co-occurrence (high confidence)")
print("  - High word-initial rate (59%)")
print("  - Low accounting co-occurrence")
print("  - Ritual enrichment 2.25x")
print("\nSearching for ergative INVERSE: high KI-RO, word-FINAL, low ritual enrichment...\n")

# Compute full suffix statistics for all suffixes
TARGET_SUFFIXES = ["-RO", "-JA", "-RE", "-TE", "-NA", "-TI", "-ME", "-NE",
                   "-DA", "-RA", "-MA", "-SI", "-KA", "-PA", "-TA", "-SE",
                   "-MU", "-QA", "-KE", "-PI", "-ZA", "-KO", "-MI", "-DI"]

suffix_stats = defaultdict(lambda: {
    "total": 0, "kuro_cooc": 0, "kiro_cooc": 0,
    "initial": 0, "final": 0, "medial": 0,
    "ritual_count": 0, "admin_count": 0,
    "sites": set(), "tokens": set(),
    "pre_logogram": 0, "pre_numeral": 0,
})

for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    site = rec.get("site", "?")
    support = rec.get("support", "?")
    is_ritual = support in RITUAL_SUPPORTS
    has_kuro = "KU-RO" in tokens
    has_kiro = "KI-RO" in tokens

    syllabics = [t for t in tokens if is_syllabic(t)]

    for i, tok in enumerate(tokens):
        if not is_syllabic(tok):
            continue
        suf = get_suffix(tok)
        if suf not in TARGET_SUFFIXES:
            continue

        suffix_stats[suf]["total"] += 1
        suffix_stats[suf]["tokens"].add(tok)
        suffix_stats[suf]["sites"].add(site)

        if has_kuro:
            suffix_stats[suf]["kuro_cooc"] += 1
        if has_kiro:
            suffix_stats[suf]["kiro_cooc"] += 1

        if is_ritual:
            suffix_stats[suf]["ritual_count"] += 1
        else:
            suffix_stats[suf]["admin_count"] += 1

        # Position in syllabic sequence
        syl_pos = syllabics.index(tok) if tok in syllabics else -1
        syl_total = len(syllabics)
        if syl_pos == 0:
            suffix_stats[suf]["initial"] += 1
        elif syl_pos == syl_total - 1:
            suffix_stats[suf]["final"] += 1
        else:
            suffix_stats[suf]["medial"] += 1

        # Does a logogram or numeral follow?
        full_idx = tokens.index(tok) if tok in tokens else -1
        if full_idx >= 0 and full_idx + 1 < len(tokens):
            next_tok = tokens[full_idx + 1]
            if next_tok in LOGOGRAMS:
                suffix_stats[suf]["pre_logogram"] += 1
            elif next_tok in NUMERAL_PATTERNS or next_tok.replace(".", "").isdigit():
                suffix_stats[suf]["pre_numeral"] += 1

# Overall ritual proportion for normalization
total_ritual_records = sum(1 for r in records if r.get("support", "") in RITUAL_SUPPORTS)
total_admin_records = len(records) - total_ritual_records

# Compute ergative score for each suffix
# Ergative profile: high KI-RO rate, high final rate, low ritual rate, high accounting context
print(f"{'Suffix':<8} {'Total':>7} {'KI-RO%':>8} {'Final%':>8} {'Initial%':>9} {'Ritual%':>9} {'Ergative Score':>15}")
print("-" * 75)

ergative_scores = {}
for suf in sorted(TARGET_SUFFIXES):
    stats = suffix_stats[suf]
    total = stats["total"]
    if total < 5:
        continue

    kiro_rate = stats["kiro_cooc"] / total
    kuro_rate = stats["kuro_cooc"] / total
    final_rate = stats["final"] / total
    initial_rate = stats["initial"] / total
    ritual_rate = stats["ritual_count"] / total

    # Ergative score: maximize KI-RO + final position, minimize ritual and initial
    # Inverse of absolutive (-JA): which has zero KI-RO, high initial, moderate ritual
    ergative_score = (
        kiro_rate * 3.0 +        # KI-RO co-occurrence is strongest signal
        final_rate * 2.0 +       # Word-final position (post-root case suffix)
        kuro_rate * 1.0 +        # General accounting (ergative agents act on objects)
        (1 - ritual_rate) * 0.5 + # Low ritual (ergative is grammatical, not sacred)
        (1 - initial_rate) * 0.5  # Low initial (ergative marks agent, usually not 1st word)
    )

    ergative_scores[suf] = {
        "total": total,
        "kiro_rate": kiro_rate,
        "kuro_rate": kuro_rate,
        "final_rate": final_rate,
        "initial_rate": initial_rate,
        "ritual_rate": ritual_rate,
        "ergative_score": ergative_score,
        "site_count": len(stats["sites"]),
    }

    print(f"{suf:<8} {total:>7} {kiro_rate:>8.3f} {final_rate:>8.3f} {initial_rate:>9.3f} {ritual_rate:>9.3f} {ergative_score:>15.3f}")

# Rank by ergative score
ranked_ergative = sorted(ergative_scores.items(), key=lambda x: -x[1]["ergative_score"])
print(f"\nTop ergative candidates (highest KI-RO + word-final + low ritual):")
for rank, (suf, scores) in enumerate(ranked_ergative[:8], 1):
    print(f"  {rank}. {suf}: ergative_score={scores['ergative_score']:.3f} | "
          f"KI-RO={scores['kiro_rate']:.3f} | final={scores['final_rate']:.3f} | "
          f"ritual={scores['ritual_rate']:.3f} | n_sites={scores['site_count']}")

# Cross-validate top candidate against non-HT sites
top_ergative_candidate = ranked_ergative[0][0] if ranked_ergative else None
if top_ergative_candidate:
    print(f"\nCross-validation of top ergative candidate: {top_ergative_candidate}")
    site_stats = defaultdict(lambda: {"kiro": 0, "total": 0})
    for rec in records:
        tokens = extract_tokens(rec.get("transliteration_tokens", []))
        site = rec.get("site", "?")
        has_kiro = "KI-RO" in tokens
        for tok in tokens:
            if is_syllabic(tok) and get_suffix(tok) == top_ergative_candidate:
                site_stats[site]["total"] += 1
                if has_kiro:
                    site_stats[site]["kiro"] += 1

    print(f"{'Site':<25} {'Total':>7} {'KI-RO%':>8}")
    for site, s in sorted(site_stats.items(), key=lambda x: -x[1]["total"]):
        kiro_pct = s["kiro"] / s["total"] if s["total"] > 0 else 0
        print(f"  {site:<23} {s['total']:>7} {kiro_pct:>8.3f}")

# ── Absolutive (-JA) vs Ergative comparison ───────────────────────────────────
print(f"\n── Absolutive (-JA) vs Top Ergative Candidate Comparison ──")
ja_stats = ergative_scores.get("-JA", {})
top_erg_stats = ergative_scores.get(top_ergative_candidate, {}) if top_ergative_candidate else {}

if ja_stats and top_erg_stats:
    print(f"\n{'Metric':<20} {'-JA (absolutive)':>18} {f'{top_ergative_candidate} (ergative?)':>20}")
    print("-" * 60)
    metrics = [("KI-RO rate", "kiro_rate"), ("KU-RO rate", "kuro_rate"),
               ("Initial rate", "initial_rate"), ("Final rate", "final_rate"),
               ("Ritual rate", "ritual_rate")]
    for label, key in metrics:
        ja_val = ja_stats.get(key, 0)
        erg_val = top_erg_stats.get(key, 0)
        print(f"{label:<20} {ja_val:>18.3f} {erg_val:>20.3f}")

# ── Save results ──────────────────────────────────────────────────────────────
output = {
    "me_suffix_analysis": {
        "total_occurrences": len(me_tokens),
        "token_types": dict(me_token_types.most_common(20)),
        "ritual_count": ritual_count,
        "admin_count": admin_count,
        "ritual_ratio": ritual_count / max(admin_count, 1),
        "position_distribution": dict(pos_dist),
        "kuro_cooccurrence": kuro_count,
        "kiro_cooccurrence": kiro_count,
        "kuro_rate": kuro_count / len(me_tokens) if me_tokens else 0,
        "kiro_rate": kiro_count / len(me_tokens) if me_tokens else 0,
        "most_common_following_tokens": next_token_types.most_common(15),
        "most_common_preceding_tokens": prev_token_types.most_common(15),
        "site_distribution": dict(site_dist.most_common()),
        "two_part_count": two_part,
        "longer_count": longer,
        "jasasara_variants": dict(jasasara_tok),
        "all_me_occurrences": me_tokens,
    },
    "ergative_search": {
        "method": "Inverse absolutive profile: high KI-RO, word-final, low ritual",
        "absolutive_reference": "-JA",
        "suffix_scores": ergative_scores,
        "ranked_candidates": [
            {"suffix": suf, **scores}
            for suf, scores in ranked_ergative[:10]
        ],
        "top_candidate": top_ergative_candidate,
        "absolutive_ja_stats": ja_stats,
        "top_ergative_stats": top_erg_stats,
    },
}

with open("analysis/outputs/me_suffix_ergative_2026-03-18.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved: analysis/outputs/me_suffix_ergative_2026-03-18.json")
