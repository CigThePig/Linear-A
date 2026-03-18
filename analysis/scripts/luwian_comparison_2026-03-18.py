"""
Luwian Morpheme Comparison for Linear A (Strategy 4)
Control test against the Hurrian morphology results from Attempt #3.

Luwian (cuneiform and hieroglyphic) is an Anatolian Indo-European language.
This script applies the same 5-point scoring rubric used for Hurrian (Attempt #3)
to Luwian case/derivational endings, then directly compares Hurrian vs. Luwian
alignment scores for each Linear A suffix.

Reference: Melchert, H.C. (2003). The Luvian Subgroup of Anatolian.
           Yakubovich, I. (2010). Sociolinguistics of the Luvian Language.
           Payne, A. (2010). Hieroglyphic Luwian: An Introduction.
"""

import json
from collections import defaultdict, Counter

# ── Load corpus ──────────────────────────────────────────────────────────────
records = []
with open("corpus/linear_a_llm_master.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "KU-RO", "KI-RO",
    "FIC", "FAR", "OVI", "BOS", "EQU", "SUS", "TELA", "LANA", "AROM",
}

def extract_tokens(raw_tokens):
    result = []
    for t in raw_tokens:
        if isinstance(t, dict):
            result.append(t.get("value", ""))
        else:
            result.append(str(t))
    return result

def is_syllabic(token: str) -> bool:
    if not token or not token.strip():
        return False
    t = token.strip()
    if t in LOGOGRAMS:
        return False
    if t.replace(".", "").isdigit():
        return False
    return any(c.isalpha() for c in t)

# ── Load prior suffix results from Attempt #2/#3 ─────────────────────────────
try:
    with open("analysis/outputs/suffix_paradigm_results_2026-03-18.json") as f:
        prior_suffix = json.load(f)
    print("Loaded prior suffix paradigm results.")
except FileNotFoundError:
    prior_suffix = {}
    print("Prior suffix results not found — recomputing.")

# Recompute suffix statistics from corpus
suffix_stats = defaultdict(lambda: {
    "total": 0, "kuro_cooc": 0, "kiro_cooc": 0,
    "pre_logogram": 0, "word_initial": 0, "word_final": 0, "word_medial": 0,
    "sites": set(), "tokens": set(),
    "pre_numeral": 0, "ritual_count": 0
})

RITUAL_SUPPORTS = {"stone vessel", "metal object", "architecture", "stone object"}
TARGET_SUFFIXES = {"-RO", "-JA", "-RE", "-TE", "-NA", "-TI", "-ME", "-NE",
                   "-DA", "-RA", "-MA", "-SI", "-KA", "-PA", "-TA", "-SE",
                   "-MU", "-QA", "-KE", "-PI"}

def get_suffix(token: str) -> str | None:
    """Extract the last 2 characters as suffix, normalized to -XX form."""
    parts = token.split("-")
    if len(parts) < 2:
        return None
    last = parts[-1].upper()
    # Filter out tokens that are just logograms or numerals
    if not any(c.isalpha() for c in last):
        return None
    return f"-{last}"

for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    site = rec.get("site", "Unknown")
    support = rec.get("support", "")
    is_ritual = support in RITUAL_SUPPORTS

    syllabics = [t for t in tokens if is_syllabic(t)]
    has_kuro = "KU-RO" in tokens
    has_kiro = "KI-RO" in tokens

    for i, tok in enumerate(syllabics):
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

        # Position in syllabic sequence
        if i == 0:
            suffix_stats[suf]["word_initial"] += 1
        elif i == len(syllabics) - 1:
            suffix_stats[suf]["word_final"] += 1
        else:
            suffix_stats[suf]["word_medial"] += 1

        # What follows this token? (placeholder — not used further)

# Convert sets to counts for JSON serialization
suffix_summary = {}
for suf, stats in suffix_stats.items():
    total = stats["total"]
    if total == 0:
        continue
    suffix_summary[suf] = {
        "total": total,
        "site_count": len(stats["sites"]),
        "token_types": len(stats["tokens"]),
        "kuro_rate": stats["kuro_cooc"] / total,
        "kiro_rate": stats["kiro_cooc"] / total,
        "initial_rate": stats["word_initial"] / total,
        "final_rate": stats["word_final"] / total,
        "medial_rate": stats["word_medial"] / total,
        "ritual_rate": stats["ritual_count"] / total,
    }

print("Suffix stats computed for", len(suffix_summary), "suffixes")

# ── Luwian morpheme inventory ────────────────────────────────────────────────
# Based on Melchert 2003, Yakubovich 2010, Payne 2010
# Format: {morpheme_name: {form, function, expected_context, phon_class}}
LUWIAN_MORPHEMES = {
    # Nominal case endings (cuneiform Luwian)
    "nominative_sg_common": {
        "form": "-anza / -s",
        "function": "nominative singular (common gender)",
        "expected_context": "subject of sentence; agent of transitive verb; word-initial or first argument",
        "la_candidate": "-NA",  # -anza → -na (truncation of -nza to open syllable)
        "phon_similarity_candidates": {"-NA": 2, "-NE": 1.5, "-TA": 1},
    },
    "accusative_sg": {
        "form": "-an / -n",
        "function": "accusative singular (patient/object)",
        "expected_context": "direct object of transitive verb; follows verb or agent",
        "la_candidate": "-NA",
        "phon_similarity_candidates": {"-NA": 1.5, "-NE": 1},
    },
    "genitive_sg": {
        "form": "-assa / -assa",
        "function": "genitive (possession, source)",
        "expected_context": "pre-noun position; administrative source/origin",
        "la_candidate": "-SA",
        "phon_similarity_candidates": {"-SA": 2, "-SE": 1.5, "-SI": 1},
    },
    "dative_locative_sg": {
        "form": "-ati / -i",
        "function": "dative-locative (to/for/at)",
        "expected_context": "destination, recipient, location; ritual dedicatory context",
        "la_candidate": "-TI",
        "phon_similarity_candidates": {"-TI": 2, "-TE": 1.5, "-DA": 1},
    },
    "ablative_sg": {
        "form": "-ati / -adi",
        "function": "ablative (from, away from)",
        "expected_context": "source of movement, origin context",
        "la_candidate": "-DA",
        "phon_similarity_candidates": {"-DA": 2, "-TA": 1.5, "-TI": 1},
    },
    "instrumental": {
        "form": "-ati / -ti",
        "function": "instrumental (by means of)",
        "expected_context": "tool, method, accompanying noun",
        "la_candidate": "-TI",
        "phon_similarity_candidates": {"-TI": 2, "-TE": 1.5},
    },
    "nominative_pl_common": {
        "form": "-anza / -nzi",
        "function": "nominative plural (common gender)",
        "expected_context": "multiple agents; lists of items",
        "la_candidate": "-NA",
        "phon_similarity_candidates": {"-NA": 1.5, "-NE": 1.5, "-NI": 1},
    },
    "accusative_pl": {
        "form": "-anza / -nta",
        "function": "accusative plural",
        "expected_context": "multiple patients; quantity lists in accounting",
        "la_candidate": "-NA",
        "phon_similarity_candidates": {"-NA": 1, "-TA": 1.5},
    },
    # Derivational morphemes
    "agentive_suffix": {
        "form": "-ala- / -alla-",
        "function": "agentive noun (one who does X)",
        "expected_context": "personal names, occupational titles; adjacent to VIR logogram",
        "la_candidate": "-RA",
        "phon_similarity_candidates": {"-RA": 1.5, "-RE": 1.5, "-RO": 1},
    },
    "adjectival_suffix": {
        "form": "-assa- / -assi-",
        "function": "adjectival derivation (pertaining to X)",
        "expected_context": "modifying role; attribute position before head noun",
        "la_candidate": "-SI",
        "phon_similarity_candidates": {"-SI": 1.5, "-SA": 1, "-SE": 1},
    },
    "verbal_noun": {
        "form": "-amma- / -umma-",
        "function": "verbal noun / action noun",
        "expected_context": "in accounting: total of actions performed",
        "la_candidate": "-MA",
        "phon_similarity_candidates": {"-MA": 2, "-ME": 1.5, "-MU": 1},
    },
    "infinitive": {
        "form": "-una / -wana",
        "function": "infinitive / purpose clause",
        "expected_context": "formula-final position in administrative documents",
        "la_candidate": "-NA",
        "phon_similarity_candidates": {"-NA": 1.5, "-JA": 1},
    },
    "relative_pronoun": {
        "form": "-za / -zi",
        "function": "relative clause marker",
        "expected_context": "word-medial, connecting clauses",
        "la_candidate": "-ZA",
        "phon_similarity_candidates": {"-ZA": 2, "-SI": 0.5},
    },
    "divine_epithet": {
        "form": "-iya- / -ia-",
        "function": "divine epithet / adjectival from divine name",
        "expected_context": "ritual contexts; following divine name",
        "la_candidate": "-JA",
        "phon_similarity_candidates": {"-JA": 2, "-JO": 1},
    },
}

# ── Scoring function (same 5-point rubric as Attempt #3 Hurrian test) ─────────
def score_alignment(la_suffix: str, morpheme: dict, suffix_stats: dict) -> dict:
    """
    Score the alignment between a Linear A suffix and a Luwian morpheme.
    Phonological similarity: 0–2
    Contextual compatibility: 0–2
    Frequency plausibility: 0–1
    Total: 0–5
    """
    result = {
        "la_suffix": la_suffix,
        "luwian_morpheme": morpheme.get("function", ""),
        "luwian_form": morpheme.get("form", ""),
        "phon_score": 0,
        "ctx_score": 0,
        "freq_score": 0,
        "total_score": 0,
        "notes": [],
    }

    if la_suffix not in suffix_stats:
        result["notes"].append(f"{la_suffix} not in corpus data")
        return result

    stats = suffix_stats[la_suffix]

    # Phonological similarity score
    phon_candidates = morpheme.get("phon_similarity_candidates", {})
    phon_score = phon_candidates.get(la_suffix, 0)
    result["phon_score"] = min(phon_score, 2)

    # Contextual compatibility score
    expected = morpheme.get("expected_context", "").lower()
    ctx_score = 0.0

    # Diagnostic: does the suffix appear in the expected positional context?
    if "subject" in expected or "agent" in expected or "initial" in expected:
        # Expect: high initial_rate
        if stats["initial_rate"] > 0.35:
            ctx_score += 1.0
        elif stats["initial_rate"] > 0.20:
            ctx_score += 0.5

    if "object" in expected or "patient" in expected or "final" in expected:
        # Expect: high final_rate or medial_rate
        if stats["final_rate"] > 0.25:
            ctx_score += 1.0
        elif stats["final_rate"] > 0.15:
            ctx_score += 0.5

    if "accounting" in expected or "total" in expected or "quantity" in expected:
        # Expect: high kuro_rate
        if stats["kuro_rate"] > 0.15:
            ctx_score += 1.0
        elif stats["kuro_rate"] > 0.08:
            ctx_score += 0.5

    if "deficit" in expected or "owed" in expected:
        if stats["kiro_rate"] > 0.10:
            ctx_score += 1.0

    if "ritual" in expected or "dedicatory" in expected or "divine" in expected:
        if stats["ritual_rate"] > 0.20:
            ctx_score += 1.0
        elif stats["ritual_rate"] > 0.10:
            ctx_score += 0.5

    if "destination" in expected or "location" in expected or "recipient" in expected:
        # These appear in non-terminal, non-initial positions
        if 0.10 < stats["medial_rate"] < 0.70:
            ctx_score += 0.5

    if "list" in expected or "multiple" in expected:
        if stats["total"] > 30:
            ctx_score += 0.5

    if "personal name" in expected or "vir" in expected.lower():
        # We can't directly test this without VIR adjacency data, give partial
        ctx_score += 0.3  # Placeholder

    result["ctx_score"] = min(ctx_score, 2.0)

    # Frequency plausibility
    total = stats["total"]
    if total > 40:
        result["freq_score"] = 1.0
    elif total > 15:
        result["freq_score"] = 0.5
    else:
        result["freq_score"] = 0.0

    result["total_score"] = result["phon_score"] + result["ctx_score"] + result["freq_score"]
    return result


# ── Run Luwian alignment scoring ──────────────────────────────────────────────
TARGET_LA_SUFFIXES = ["-RO", "-JA", "-RE", "-TE", "-NA", "-TI", "-ME",
                       "-NE", "-DA", "-RA", "-MA", "-SI", "-SE", "-MU"]

luwian_results = []
for morpheme_name, morpheme in LUWIAN_MORPHEMES.items():
    for la_suf in TARGET_LA_SUFFIXES:
        result = score_alignment(la_suf, morpheme, suffix_summary)
        result["morpheme_name"] = morpheme_name
        luwian_results.append(result)

luwian_results.sort(key=lambda x: -x["total_score"])

# High confidence: ≥ 4.0
high_conf = [r for r in luwian_results if r["total_score"] >= 4.0]
medium_conf = [r for r in luwian_results if 3.0 <= r["total_score"] < 4.0]

print(f"\nLuwian morpheme alignment results:")
print(f"  High-confidence (≥4.0): {len(high_conf)}")
print(f"  Medium-confidence (3.0–3.9): {len(medium_conf)}")

print("\nTop 15 Luwian alignments:")
print(f"{'LA Suffix':<12} {'Luwian Form':<20} {'Function':<35} {'Score'}")
print("-" * 80)
for r in luwian_results[:15]:
    print(f"{r['la_suffix']:<12} {r['luwian_form']:<20} {r['luwian_morpheme'][:34]:<35} {r['total_score']:.1f}")

# ── Hurrian reference scores (from Attempt #3, for direct comparison) ─────────
# These are the documented high-confidence Hurrian alignments from Attempt #3
HURRIAN_TOP_SCORES = {
    "-TE": [("directive", 5.0), ("locative", 4.0)],
    "-NA": [("locative", 5.0), ("directive", 4.0)],
    "-TI": [("directive", 5.0), ("genitive", 4.0), ("ablative", 4.0)],
    "-NE": [("plural_nom", 4.5)],
    "-JA": [("absolutive", 4.0), ("locative", 4.0), ("directive", 4.0)],
    "-RE": [("genitive", 4.0)],
    "-TA": [("directive", 4.0)],
    "-RA": [("comitative", 4.0)],
}

# Best Luwian score for each suffix
luwian_best_by_suffix = {}
for r in luwian_results:
    suf = r["la_suffix"]
    if suf not in luwian_best_by_suffix or r["total_score"] > luwian_best_by_suffix[suf]["total_score"]:
        luwian_best_by_suffix[suf] = r

# Best Hurrian score for each suffix
hurrian_best_by_suffix = {}
for suf, matches in HURRIAN_TOP_SCORES.items():
    hurrian_best_by_suffix[suf] = max(score for _, score in matches)

print("\n── Direct Comparison: Hurrian vs. Luwian Best Alignment Score ──")
print(f"{'Suffix':<10} {'Hurrian Best':>14} {'Luwian Best':>12} {'Difference':>12} {'Winner'}")
print("-" * 60)

comparison_data = {}
for suf in sorted(set(list(hurrian_best_by_suffix.keys()) + list(luwian_best_by_suffix.keys()))):
    hurrian_score = hurrian_best_by_suffix.get(suf, 0)
    luwian_score = luwian_best_by_suffix.get(suf, {}).get("total_score", 0)
    diff = hurrian_score - luwian_score
    if diff > 0.3:
        winner = "Hurrian"
    elif diff < -0.3:
        winner = "Luwian"
    else:
        winner = "Tie"

    comparison_data[suf] = {
        "hurrian_best": hurrian_score,
        "luwian_best": luwian_score,
        "difference": diff,
        "winner": winner,
    }
    print(f"{suf:<10} {hurrian_score:>14.1f} {luwian_score:>12.1f} {diff:>12.1f} {winner}")

# Overall winner count
hurrian_wins = sum(1 for d in comparison_data.values() if d["winner"] == "Hurrian")
luwian_wins = sum(1 for d in comparison_data.values() if d["winner"] == "Luwian")
ties = sum(1 for d in comparison_data.values() if d["winner"] == "Tie")
print(f"\nOverall: Hurrian wins={hurrian_wins}, Luwian wins={luwian_wins}, Ties={ties}")

# ── Luwian-specific lexical comparison (Strategy 4) ──────────────────────────
# Apply Linear B phonetic values to 30 most frequent sequences and check Luwian glossary
# Key Luwian administrative vocabulary (Melchert 2003, Hawkins 2000)

LUWIAN_GLOSSARY = {
    # Luwian word: (consonant skeleton, meaning, register)
    "ALATI": ("LT", "vessel/container type", "administrative"),
    "ARAZA": ("RZ", "boundary/limit", "legal/administrative"),
    "ARMA": ("RM", "moon", "religious"),
    "ASATA": ("ST", "good", "general"),
    "ATRI": ("TR", "father", "personal title"),
    "DUWA": ("DW", "two", "numeral"),
    "HANTI": ("NT", "in front/first", "locative"),
    "ISHA": ("S", "lord/master", "title"),
    "KARI": ("KR", "to give", "verb"),
    "KUWA": ("KW", "who/which", "relative"),
    "MASANA": ("MSN", "god", "religious"),
    "MATI": ("MT", "country/land", "geographic"),
    "NIMUWANTA": ("NMW", "storm god epithet", "religious"),
    "PARI": ("PR", "for/in front of", "preposition"),
    "PATA": ("PT", "foot/step", "body part / measure"),
    "RUNTIYA": ("RNT", "stag god name", "divine name"),
    "SARA": ("SR", "above/up", "directional"),
    "TATI": ("TT", "father", "personal title"),
    "TARHU": ("TRH", "to overcome/Tarhunt storm god", "divine name"),
    "TUWA": ("TW", "to place/put", "verb"),
    "WALA": ("WL", "to die / dead", "verb"),
    "ZITI": ("ZT", "man/person", "general"),
    "ANIYA": ("NY", "to do/make", "verb"),
    "HAWA": ("HW", "wind/breath", "general"),
    "ISHA-": ("SH", "lord (prefix)", "title"),
    "IDA": ("D", "mountain? (Luwian cognate of Mt. Ida?)", "geographic"),
    "KUSSANA": ("KSN", "sheep? (vessel type?)", "commodity?"),
    "NAWI": ("NW", "new", "adjective"),
    "TAMA": ("TM", "to be/exist", "verb"),
    "WASU": ("WS", "good", "adjective"),
}

# Top Linear A multi-syllable tokens for comparison
top_la_tokens = Counter()
for rec in records:
    tokens = extract_tokens(rec.get("transliteration_tokens", []))
    for tok in tokens:
        if is_syllabic(tok) and "-" in tok:
            top_la_tokens[tok] += 1

print("\n── Luwian Lexical Comparison (Strategy 4) ──")
print("Checking top Linear A tokens against Luwian glossary by consonant skeleton:")

def get_consonant_skeleton(token: str) -> str:
    """Extract consonant skeleton from transliteration."""
    parts = token.replace("-", "").upper()
    consonants = "".join(c for c in parts if c not in "AEIOU0123456789*₂₃")
    return consonants or parts[:2]

lexical_matches = []
for tok, count in top_la_tokens.most_common(100):
    la_skeleton = get_consonant_skeleton(tok)
    for luwian_word, (luw_skeleton, meaning, register) in LUWIAN_GLOSSARY.items():
        # Check if consonant skeletons overlap
        la_s = la_skeleton.upper()
        luw_s = luw_skeleton.upper()
        # Allow partial match: at least 2 consonants in same order
        if len(la_s) >= 2 and len(luw_s) >= 2:
            # Check if luw_skeleton is a substring of la_skeleton or vice versa
            min_len = min(len(la_s), len(luw_s))
            matches_leading = la_s[:min_len] == luw_s[:min_len]
            if matches_leading and min_len >= 2:
                lexical_matches.append({
                    "la_token": tok,
                    "la_count": count,
                    "la_skeleton": la_skeleton,
                    "luwian_word": luwian_word,
                    "luwian_skeleton": luw_skeleton,
                    "luwian_meaning": meaning,
                    "luwian_register": register,
                    "skeleton_match_len": min_len,
                })

lexical_matches.sort(key=lambda x: (-x["skeleton_match_len"], -x["la_count"]))

print(f"\nTotal lexical skeleton matches found: {len(lexical_matches)}")
print(f"\nTop matches (≥2 consonant skeleton overlap):")
print(f"{'Linear A Token':<20} {'Count':>6} {'Luwian Word':<20} {'Meaning':<40} {'Skeleton Match'}")
print("-" * 100)
seen_tokens = set()
for m in lexical_matches[:20]:
    tok_key = (m["la_token"], m["luwian_word"])
    if tok_key in seen_tokens:
        continue
    seen_tokens.add(tok_key)
    print(f"{m['la_token']:<20} {m['la_count']:>6} {m['luwian_word']:<20} {m['luwian_meaning'][:39]:<40} {m['la_skeleton']}~{m['luwian_skeleton']}")

# ── Save results ──────────────────────────────────────────────────────────────
output = {
    "suffix_statistics": suffix_summary,
    "luwian_alignment_results": luwian_results,
    "high_confidence_alignments": high_conf,
    "medium_confidence_alignments": medium_conf,
    "hurrian_vs_luwian_comparison": comparison_data,
    "overall_language_preference": {
        "hurrian_wins": hurrian_wins,
        "luwian_wins": luwian_wins,
        "ties": ties,
        "preferred": "Hurrian" if hurrian_wins > luwian_wins else ("Luwian" if luwian_wins > hurrian_wins else "Tie"),
    },
    "luwian_lexical_matches": lexical_matches[:30],
}

with open("analysis/outputs/luwian_comparison_2026-03-18.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved: analysis/outputs/luwian_comparison_2026-03-18.json")
