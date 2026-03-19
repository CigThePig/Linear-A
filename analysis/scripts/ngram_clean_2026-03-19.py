#!/usr/bin/env python3
"""
Refined N-gram Language Fingerprinting — Strategy 9 (Clean Re-run)
Linear A Decipherment Project — 2026-03-19

Purpose: Fix methodological issues from Attempt #4's ngram_fingerprint_2026-03-18.py:
  1. Strip newline/divider tokens before computing bigrams
  2. Keep *XXX unknown signs as their own tokens (not "OTHER")
  3. Build SIGN-LEVEL (not consonant-class-level) bigram transition matrices
  4. Compare against language reference profiles at sign-level resolution

Expected: Higher absolute similarity scores and better language discrimination.
Hurrian should rank higher than Proto-Semitic if the prior ranking was an artifact.

Evidence tier: Tier 1 (Structural) — n-gram similarity ≠ language identification.
"""

import json
import math
import re
from collections import defaultdict, Counter

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/ngram_clean_2026-03-19.json"

# ─── Token Classification ─────────────────────────────────────────────────────

# Structural tokens to STRIP (do not include in bigrams, do not create bigram across them)
STRIP_TOKENS = {"𐄁", "↵", "\n", "", " ", "·", "—"}

# Logograms — exclude from bigrams but do NOT create bigram across them (boundary)
LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG", "OVI", "BOS",
    "EQU", "SUS", "CAP", "TELA", "LANA", "AES", "GRA+KU", "GRA+E",
    "GRA+PA", "GRA+SI", "GRA+TE", "OLIV+E", "OLIV+A", "OLIV+KU",
}

# Numeral pattern
NUMERAL_RE = re.compile(r'^[\d/.,½⅓¼⅕]+$')


def classify_token(token):
    """Classify token as: 'syllabic', 'logogram', 'numeral', 'strip', or 'unknown_sign'."""
    if not token or token in STRIP_TOKENS:
        return "strip"
    if token in LOGOGRAMS:
        return "logogram"
    if NUMERAL_RE.match(token):
        return "numeral"
    if token.startswith("*"):
        return "unknown_sign"
    return "syllabic"


def split_compound_token(token):
    """
    Split a compound (hyphenated) token into individual signs.
    E.g., "NA-SI" -> ["NA", "SI"]
         "I-PI-NA-MA" -> ["I", "PI", "NA", "MA"]
         "JA-TA-I-*301-U-JA" -> split at hyphens, keep *XXX as single unit
    """
    if not token or "-" not in token:
        return [token] if token else []
    parts = token.split("-")
    signs = []
    for part in parts:
        if part:
            signs.append(part)
    return signs


def extract_clean_sequences(records):
    """
    Extract clean sign sequences for bigram analysis.
    - Strip structural tokens
    - Split compound (hyphenated) tokens into individual CV signs
    - Split sequence at logograms and numerals (boundary markers)
    - Keep *XXX unknown signs as their own segment labels but exclude from bigrams
    """
    sequences = []
    for rec in records:
        raw = rec.get("transliteration_tokens", [])
        tokens = [t.get("value", "") if isinstance(t, dict) else str(t) for t in raw]
        if not tokens:
            continue

        current_segment = []
        for token in tokens:
            cls = classify_token(token)
            if cls == "strip":
                continue  # Skip but don't break sequence
            elif cls in ("logogram", "numeral"):
                # Boundary: save current segment and start new one
                if current_segment:
                    sequences.append(current_segment)
                current_segment = []
            elif cls == "unknown_sign":
                # Unknown sign breaks n-gram sequence (we can't assign phonetics)
                if current_segment:
                    sequences.append(current_segment)
                current_segment = []
            elif cls == "syllabic":
                # Split compound tokens into individual signs
                signs = split_compound_token(token)
                # Filter out any embedded unknown signs (*XXX) — they break the sequence
                clean_signs = []
                for sign in signs:
                    if sign.startswith("*"):
                        if clean_signs:
                            sequences.append(clean_signs)
                        clean_signs = []
                    else:
                        clean_signs.append(sign)
                current_segment.extend(clean_signs)

        if current_segment:
            sequences.append(current_segment)

    return [s for s in sequences if len(s) >= 2]  # Need ≥2 for bigrams


# ─── Bigram Transition Matrix ─────────────────────────────────────────────────

def build_bigram_matrix(sequences):
    """Build bigram (A→B) transition probability matrix."""
    bigram_counts = defaultdict(Counter)
    unigram_counts = Counter()

    for seq in sequences:
        unigram_counts.update(seq)
        for i in range(len(seq) - 1):
            bigram_counts[seq[i]][seq[i + 1]] += 1

    # Normalize to transition probabilities
    transition_probs = {}
    for sign_a, followers in bigram_counts.items():
        total = sum(followers.values())
        transition_probs[sign_a] = {sign_b: count / total
                                    for sign_b, count in followers.items()}

    return transition_probs, unigram_counts, bigram_counts


def build_bigram_vector(transition_probs, vocabulary):
    """Build a flat bigram probability vector over a given vocabulary."""
    vector = {}
    for a in vocabulary:
        for b in vocabulary:
            key = f"{a}→{b}"
            prob = transition_probs.get(a, {}).get(b, 0.0)
            if prob > 0:
                vector[key] = prob
    return vector


def cosine_similarity(v1, v2):
    """Compute cosine similarity between two dict-based sparse vectors."""
    keys = set(v1.keys()) | set(v2.keys())
    if not keys:
        return 0.0
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in keys)
    norm1 = math.sqrt(sum(x ** 2 for x in v1.values()))
    norm2 = math.sqrt(sum(x ** 2 for x in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def kl_divergence(p, q, vocabulary):
    """KL divergence D(P||Q) for two dict-based distributions."""
    total = 0.0
    epsilon = 1e-10
    for key in vocabulary:
        p_val = p.get(key, 0.0)
        q_val = q.get(key, epsilon)
        if p_val > 0:
            total += p_val * math.log(p_val / q_val)
    return total


# ─── Reference Language Profiles ─────────────────────────────────────────────
# These are approximate sign-level CV bigram profiles derived from known texts.
# They represent the RELATIVE frequency of sign-to-sign transitions.
# Profiles use Linear B-style CV notation as the common representation layer.
# Higher values = more common transition in that language.
#
# Hurrian (Mitanni-period, Speiser 1941; Wegner 2007):
#   Characteristic: heavy agglutination, VCV patterns, suffixes -ne, -ve, -ra, -da
#   CV skeleton tends toward: CV-CV-VC with alternating stop/vowel/nasal
# Luwian (cuneiform, Melchert 2003):
#   Characteristic: IE morphology, suffixes -anza, -an, -ati, consonant clusters at morpheme boundaries
# Proto-Semitic:
#   Characteristic: CCC triconsonantal roots, VI-CCC-I patterns, heavy consonant clustering
# Etruscan:
#   Characteristic: heavy stop-initial syllables, frequent final consonants

def get_reference_profiles():
    """
    Return approximate sign-level bigram profiles for candidate languages.
    Format: {language: {sign_A→sign_B: relative_frequency}}
    These are derived from known word forms in each language.
    """

    # Hurrian (agglutinative, SOV, ergative-absolutive)
    # Key morpheme sequences from Wegner 2007 Hurrian vocabulary:
    # ti-ve-na, pu-ru-li, ta-nu-va, a-ta-a-e, e-ni-e-na (god+abs),
    # sa-ri-ri, fu-ur-ri, hu-ur-ri, ma-ni-in-ku-ub, ki-re-ni
    # Suffix sequences: -u-la, -i-ta, -ne, -ve, -ra, -da, -ni
    hurrian = {
        "A→TA": 0.08, "A→NA": 0.07, "A→NE": 0.06,
        "I→NA": 0.07, "I→TA": 0.06, "I→RE": 0.05,
        "E→NE": 0.09, "E→NA": 0.07, "E→RI": 0.05,
        "TA→NA": 0.07, "TA→I": 0.06, "TA→RE": 0.05,
        "NA→I": 0.07, "NA→TA": 0.06, "NA→KU": 0.04,
        "NE→I": 0.06, "NE→A": 0.05,
        "RI→I": 0.06, "RE→NE": 0.05, "RE→I": 0.05,
        "KU→RI": 0.05, "KU→NA": 0.04,
        "RU→RI": 0.05, "RU→I": 0.05,
        "TI→NA": 0.05, "TI→RE": 0.04,
        "MA→NI": 0.05, "NI→NA": 0.06, "NI→TA": 0.04,
        "U→LA": 0.04, "U→RA": 0.04, "U→NA": 0.05,
        "SA→RI": 0.04, "SA→NA": 0.04,
        "PA→RI": 0.03, "PA→NA": 0.03,
    }

    # Luwian (cuneiform, Indo-European agglutinative)
    # Key morpheme sequences from Melchert 2003:
    # wa-wa-la, ta-ti-na, a-ra-wa-na, pa-ra-na, ha-pa-ti,
    # za-sa-ti, a-na-ti, wa-ti-ti, ku-wa-ta
    # Suffixes: -an-za, -a-ti, -a-ta, -wa-na, -sa-za
    luwian = {
        "WA": 0.10,  # WA is very frequent in Luwian (verb stem formant)
        "A→NA": 0.08, "A→RA": 0.07, "A→TA": 0.07,
        "RA→NA": 0.08, "RA→WA": 0.06, "RA→A": 0.06,
        "NA→TA": 0.07, "NA→WA": 0.06, "NA→A": 0.05,
        "TA→I": 0.06, "TA→WA": 0.06, "TA→NA": 0.05,
        "WA→NA": 0.07, "WA→TA": 0.06, "WA→LA": 0.05,
        "AN→ZA": 0.06, "ZA→SA": 0.05,
        "PA→RA": 0.05, "PA→NA": 0.04,
        "SA→ZA": 0.05, "SA→TA": 0.04,
        "I→TA": 0.05, "I→NA": 0.05,
        "KU→WA": 0.05, "KU→NA": 0.04,
        "LA→I": 0.04, "LA→NA": 0.04,
        "TI→NA": 0.04,
    }

    # Proto-Semitic (triconsonantal root pattern CVC-CVC-CVC)
    # Key patterns: consonant-heavy, V rarely appears between two identical Cs
    # Characteristic bigrams from reconstructed Proto-Semitic roots:
    # *qatala (3-radical), *baytu, *kalbu, *malku
    # High stop-after-vowel, vowel-after-stop transitions
    proto_semitic = {
        "A→LA": 0.09, "A→KA": 0.07, "A→TA": 0.07, "A→MA": 0.06,
        "A→NA": 0.06, "A→RA": 0.06, "A→BA": 0.05,
        "LA→A": 0.08, "LA→KA": 0.06, "LA→MA": 0.05,
        "KA→LA": 0.07, "KA→TA": 0.06, "KA→NA": 0.05,
        "MA→LA": 0.07, "MA→KA": 0.06, "MA→RA": 0.05,
        "NA→A": 0.07, "NA→KA": 0.05, "NA→TA": 0.05,
        "RA→A": 0.07, "RA→KA": 0.06, "RA→MA": 0.05,
        "TA→A": 0.08, "TA→KA": 0.06, "TA→LA": 0.05,
        "I→NA": 0.05, "I→LA": 0.05,
        "U→LA": 0.06, "U→KA": 0.05,
        "SA→MA": 0.04, "DA→MA": 0.04,
        "BA→LA": 0.05, "BA→RA": 0.04,
        "QA→TA": 0.05, "QA→LA": 0.04,
    }

    # Etruscan (isolate, CV-dominant but stop-heavy)
    # Key sequences from Bonfante & Bonfante (2002):
    # mi-ni-pi, la-ri-sa, vel-tha, thes-sa, a-pa-lu-ne
    # Characteristic: heavy dental stops (TH), frequent -si, -sa endings
    etruscan = {
        "A→PA": 0.08, "A→LA": 0.07, "A→NA": 0.07, "A→RI": 0.06,
        "RI→SA": 0.08, "RI→A": 0.07, "RI→NA": 0.05,
        "LA→RI": 0.08, "LA→SA": 0.06, "LA→NA": 0.05,
        "SA→A": 0.08, "SA→NA": 0.06, "SA→RI": 0.05,
        "NA→A": 0.07, "NA→SA": 0.06, "NA→RI": 0.05,
        "MI→NA": 0.07, "MI→PI": 0.06,
        "PA→LA": 0.06, "PA→NA": 0.05,
        "TE→SA": 0.06, "TE→NA": 0.05,
        "SI→NA": 0.05, "SI→A": 0.05,
        "NI→PA": 0.05, "NI→A": 0.04,
        "E→LA": 0.05, "E→RI": 0.05,
        "VE→LA": 0.05, "VE→NA": 0.04,
    }

    return {
        "Hurrian": hurrian,
        "Luwian": luwian,
        "Proto-Semitic": proto_semitic,
        "Etruscan": etruscan,
    }


# ─── Analysis ─────────────────────────────────────────────────────────────────

def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def compute_top_bigrams(bigram_counts, top_n=30):
    """Get top bigrams by raw count."""
    all_bigrams = []
    for a, followers in bigram_counts.items():
        for b, count in followers.items():
            all_bigrams.append((f"{a}→{b}", count))
    return sorted(all_bigrams, key=lambda x: -x[1])[:top_n]


def compute_characteristic_bigrams(transition_probs, unigram_counts):
    """Find bigrams more frequent than expected by chance (PMI > 0)."""
    total = sum(unigram_counts.values())
    results = []
    for a, followers in transition_probs.items():
        p_a = unigram_counts[a] / total
        for b, p_ab in followers.items():
            p_b = unigram_counts[b] / total
            if p_a > 0 and p_b > 0:
                pmi = math.log(p_ab / p_b)  # log P(b|a) / P(b)
                results.append((f"{a}→{b}", round(pmi, 4), round(p_ab, 4)))

    return sorted(results, key=lambda x: -x[1])[:30]


def run():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"  Loaded {len(records)} records")

    print("Extracting clean sign sequences (stripping dividers, splitting at boundaries)...")
    sequences = extract_clean_sequences(records)
    total_tokens = sum(len(s) for s in sequences)
    print(f"  {len(sequences)} clean segments, {total_tokens} total syllabic tokens")

    print("Building sign-level bigram matrix...")
    transition_probs, unigram_counts, bigram_counts = build_bigram_matrix(sequences)
    vocabulary = sorted(unigram_counts.keys())
    print(f"  Vocabulary size: {len(vocabulary)} signs")
    print(f"  Bigram types: {sum(len(v) for v in bigram_counts.values())}")

    # Build Linear A bigram vector
    linear_a_vector = {}
    for a in vocabulary:
        for b, prob in transition_probs.get(a, {}).items():
            linear_a_vector[f"{a}→{b}"] = prob

    print("Comparing against reference language profiles...")
    reference_profiles = get_reference_profiles()

    language_rankings = []
    for lang_name, lang_profile in reference_profiles.items():
        sim = cosine_similarity(linear_a_vector, lang_profile)
        # Also compute overlap: how many reference bigrams appear in Linear A
        overlap_count = sum(1 for key in lang_profile if key in linear_a_vector)
        overlap_rate = overlap_count / len(lang_profile) if lang_profile else 0

        language_rankings.append({
            "language": lang_name,
            "cosine_similarity": round(sim, 6),
            "overlap_bigrams": overlap_count,
            "reference_bigrams_total": len(lang_profile),
            "overlap_rate": round(overlap_rate, 3),
        })

    language_rankings.sort(key=lambda x: -x["cosine_similarity"])

    print("\nLanguage ranking (cosine similarity):")
    for rank, item in enumerate(language_rankings, 1):
        print(f"  #{rank} {item['language']:15s}  cosine={item['cosine_similarity']:.6f}  "
              f"overlap={item['overlap_bigrams']}/{item['reference_bigrams_total']}")

    # Top bigrams
    top_bigrams = compute_top_bigrams(bigram_counts, top_n=30)
    characteristic_bigrams = compute_characteristic_bigrams(transition_probs, unigram_counts)

    # Sign-level phonotactic properties of Linear A
    vowel_signs = {"A", "E", "I", "O", "U"}
    total_bigrams = sum(sum(v.values()) for v in bigram_counts.values())

    # Vowel-following rate (syllables that follow a vowel)
    vowel_initial_bigrams = sum(
        sum(cnt for cnt in bigram_counts[a].values())
        for a in bigram_counts if a in vowel_signs
    )
    vowel_initial_rate = vowel_initial_bigrams / total_bigrams if total_bigrams else 0

    # Stop-initial signs
    stop_signs = {"KA", "KE", "KI", "KO", "KU", "PA", "PE", "PI", "PO", "PU",
                  "TA", "TE", "TI", "TO", "TU", "DA", "DE", "DI", "DO", "DU"}
    stop_initial_bigrams = sum(
        sum(cnt for cnt in bigram_counts[a].values())
        for a in bigram_counts if a in stop_signs
    )
    stop_initial_rate = stop_initial_bigrams / total_bigrams if total_bigrams else 0

    phonotactic_profile = {
        "total_bigram_tokens": total_bigrams,
        "vocabulary_size": len(vocabulary),
        "vowel_initial_bigram_rate": round(vowel_initial_rate, 4),
        "stop_initial_bigram_rate": round(stop_initial_rate, 4),
        "avg_sequence_length": round(total_tokens / len(sequences), 2) if sequences else 0,
        "top_unigrams": [(sign, count) for sign, count in unigram_counts.most_common(20)],
    }

    # Comparison with Attempt #4 results
    attempt4_ranking = [
        {"language": "Proto-Semitic", "cosine_similarity": 0.1467, "method": "class-level"},
        {"language": "Luwian", "cosine_similarity": 0.1131, "method": "class-level"},
        {"language": "Etruscan", "cosine_similarity": 0.0971, "method": "class-level"},
        {"language": "Hurrian", "cosine_similarity": 0.0860, "method": "class-level"},
    ]

    result = {
        "metadata": {
            "date": "2026-03-19",
            "strategy": "Strategy 9 — Refined N-gram Fingerprinting (sign-level)",
            "corpus_records": len(records),
            "clean_segments": len(sequences),
            "total_syllabic_tokens": total_tokens,
            "vocabulary_size": len(vocabulary),
            "improvements_over_attempt4": [
                "1. Stripped divider tokens (𐄁, ↵, \\n) before bigram computation",
                "2. Split sequences at logograms and numerals (boundary markers)",
                "3. Unknown signs (*XXX) treated as sequence boundaries, not 'OTHER' class",
                "4. Sign-level bigrams (e.g., KA→TA) instead of class-level (stop→stop)",
            ],
            "evidence_tier": "Tier 1 (Structural) — phonotactic similarity ≠ language identification",
            "note": "Reference profiles are approximations. Results are suggestive not definitive.",
        },
        "language_ranking_current": language_rankings,
        "language_ranking_attempt4_reference": attempt4_ranking,
        "interpretation": {
            "if_hurrian_rises": "Contradiction with Attempt #4 was methodological artifact; Hurrian phonotactics compatible",
            "if_proto_semitic_still_first": "Proto-Semitic phonotactic proximity may reflect genuine contact or shared areal features",
            "if_rankings_change_substantially": "Sign-level resolution reveals finer structure; class-level was too coarse",
            "if_rankings_unchanged": "Methodological fixes insufficient; language family not determinable from n-gram alone",
        },
        "linear_a_phonotactic_profile": phonotactic_profile,
        "top_bigrams_by_frequency": [
            {"bigram": b, "count": c} for b, c in top_bigrams
        ],
        "characteristic_bigrams_by_pmi": [
            {"bigram": b, "pmi": p, "prob": pr}
            for b, p, pr in characteristic_bigrams
        ],
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {OUTPUT_PATH}")
    return result


if __name__ == "__main__":
    run()
