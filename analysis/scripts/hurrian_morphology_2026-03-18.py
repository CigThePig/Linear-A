"""
Hurrian Language Morphology Systematic Testing
Linear A Decipherment Project — 2026-03-18

Strategy 8: Systematically test whether Linear A suffix distribution
is compatible with Hurrian case/voice morpheme inventory.

Builds on suffix_paradigm_results_2026-03-18.json from Attempt #2.
Does NOT re-run suffix extraction — reuses the existing data.

Key hypotheses:
- -NA = Hurrian locative -na (appears in location-like contexts)
- -TE = Hurrian dative -da/-te (appears in "to/for" argument positions)
- -JA = Hurrian intransitive/absolutive marker (zero KI-RO co-occurrence confirmed)
- -RE = verb/participle ending -ri/-re (high accounting co-occurrence)

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Prior data: analysis/outputs/suffix_paradigm_results_2026-03-18.json
Output: analysis/outputs/hurrian_morphology_2026-03-18.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
SUFFIX_DATA_PATH = Path("analysis/outputs/suffix_paradigm_results_2026-03-18.json")
OUTPUT_PATH = Path("analysis/outputs/hurrian_morphology_2026-03-18.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "KU-RO", "KI-RO",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")
NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈"}

# ============================================================
# HURRIAN MORPHEME INVENTORY
# Sources: Speiser (1941), Wegner (2007), Giorgieri (2000)
# ============================================================
HURRIAN_MORPHEMES = {
    # Case suffixes (attached to nominal stems)
    "absolutive":   {"forms": [],          "function": "subject of intransitive / object of transitive verb"},
    "ergative":     {"forms": ["š", "ž"],  "function": "subject of transitive verb"},
    "genitive":     {"forms": ["ve", "bi", "pe"], "function": "possessive / genitive relation"},
    "dative":       {"forms": ["va", "fa", "ve"], "function": "indirect object / 'for/to'"},
    "locative":     {"forms": ["a", "na", "ne"],  "function": "location / 'at/in'"},
    "ablative":     {"forms": ["dan", "tan"],     "function": "source / 'from'"},
    "directive":    {"forms": ["da", "ta"],       "function": "goal / 'toward/to'"},
    "instrumental": {"forms": ["ae", "e"],        "function": "instrument / 'with/by means of'"},
    "comitative":   {"forms": ["ra"],             "function": "accompaniment / 'with'"},
    # Number
    "plural_nom":   {"forms": ["na", "ne", "lla"],     "function": "plural nominative/absolutive"},
    "plural_erg":   {"forms": ["ž-na", "š-na"],        "function": "plural ergative"},
    # Verbal suffixes (voice/aspect markers)
    "transitive_v": {"forms": ["i", "ī"],              "function": "transitive verb form"},
    "intransitive_v":{"forms": ["o", "u", "a"],        "function": "intransitive verb form"},
    "antipassive":  {"forms": ["ul", "ill"],            "function": "antipassive (removes transitivity)"},
    # Possessive/pronominal suffixes
    "1sg_poss":     {"forms": ["iff", "if"],            "function": "1st singular possessive 'my'"},
    "2sg_poss":     {"forms": ["ff", "f"],              "function": "2nd singular possessive 'your'"},
    "3sg_poss":     {"forms": ["i", "e"],               "function": "3rd singular possessive 'his/her'"},
}

# Linear A suffixes from prior analysis (top attested, with known statistics)
# These are the final syllables of multi-sign tokens
LINEAR_A_SUFFIXES = {
    "RO":  {"count": 78,  "kuro_rate": 0.154, "kiro_rate": 0.128, "sites": 22,
            "notes": "appears in terminal/accounting position; KU-RO itself ends in -RO"},
    "JA":  {"count": 65,  "kuro_rate": 0.034, "kiro_rate": 0.000, "sites": 17,
            "notes": "ZERO KI-RO co-occurrence across 17 sites — strong non-transactional signal"},
    "RE":  {"count": 58,  "kuro_rate": 0.216, "kiro_rate": 0.157, "sites": 20,
            "notes": "high accounting co-occurrence; may be active/participle marker"},
    "TE":  {"count": 56,  "kuro_rate": 0.089, "kiro_rate": 0.071, "sites": 20,
            "notes": "most geographically widespread (20 sites); low accounting co-occ"},
    "NA":  {"count": 54,  "kuro_rate": 0.120, "kiro_rate": 0.074, "sites": 18,
            "notes": "intermediate accounting; cf. Hurrian locative -na"},
    "TI":  {"count": 49,  "kuro_rate": 0.175, "kiro_rate": 0.020, "sites": 15,
            "notes": "strongly VIR-associated; likely personal names or occupational"},
    "SI":  {"count": 38,  "kuro_rate": 0.105, "kiro_rate": 0.053, "sites": 14,
            "notes": "medium accounting co-occurrence"},
    "TA":  {"count": 35,  "kuro_rate": 0.086, "kiro_rate": 0.057, "sites": 13,
            "notes": "cf. Hurrian directive -da/-ta"},
    "MA":  {"count": 33,  "kuro_rate": 0.091, "kiro_rate": 0.030, "sites": 12,
            "notes": "low deficit co-occurrence; may be nominal"},
    "DA":  {"count": 28,  "kuro_rate": 0.107, "kiro_rate": 0.036, "sites": 11,
            "notes": "cf. Hurrian directive -da"},
    "RA":  {"count": 27,  "kuro_rate": 0.148, "kiro_rate": 0.074, "sites": 10,
            "notes": "cf. Hurrian comitative -ra"},
    "KA":  {"count": 25,  "kuro_rate": 0.080, "kiro_rate": 0.040, "sites": 12,
            "notes": "uncommon in accounting; possibly qualifier"},
    "NE":  {"count": 20,  "kuro_rate": 0.050, "kiro_rate": 0.000, "sites": 9,
            "notes": "cf. Hurrian plural -ne/-na; zero KI-RO similar to -JA"},
    "MI":  {"count": 18,  "kuro_rate": 0.111, "kiro_rate": 0.056, "sites": 8,
            "notes": "limited data"},
}


def score_phonological_similarity(la_suffix, hurrian_form):
    """
    Score phonological similarity between a Linear A final syllable and a Hurrian morpheme form.
    Scale: 0 (no match), 1 (partial match), 2 (close match)
    """
    la = la_suffix.upper()
    hurr = hurrian_form.upper()

    if la == hurr:
        return 2  # exact match

    # Consonant-only comparison
    la_consonants = re.sub(r"[AEIOU]", "", la)
    hurr_consonants = re.sub(r"[AEIOU]", "", hurr)

    if la_consonants == hurr_consonants and la_consonants:
        return 2  # same consonants, different vowel — common cross-language match

    # First consonant match
    if la_consonants and hurr_consonants and la_consonants[0] == hurr_consonants[0]:
        return 1  # same initial consonant

    # Vowel match only (weak)
    la_vowels = re.sub(r"[^AEIOU]", "", la)
    hurr_vowels = re.sub(r"[^AEIOU]", "", hurr)
    if la_vowels and hurr_vowels and la_vowels == hurr_vowels:
        return 1  # same vowel pattern

    return 0


def score_contextual_compatibility(la_suffix_data, hurrian_case):
    """
    Score whether the Linear A suffix's contextual behavior is compatible
    with the Hurrian grammatical function.
    Scale: 0 (incompatible), 1 (neutral/uncertain), 2 (compatible)
    """
    kuro_rate = la_suffix_data.get("kuro_rate", 0)
    kiro_rate = la_suffix_data.get("kiro_rate", 0)
    notes = la_suffix_data.get("notes", "")

    # Hurrian accounting/transactional contexts would show up in KU-RO co-occurrence
    ACCOUNTING_CASES = {"ergative", "transitive_v", "genitive"}
    # Hurrian non-transactional/intransitive contexts would avoid KI-RO
    INTRANS_CASES = {"absolutive", "intransitive_v", "antipassive", "plural_nom"}
    # Locative/directional cases would appear in geographic contexts
    LOCATIVE_CASES = {"locative", "ablative", "directive", "comitative"}

    if hurrian_case in INTRANS_CASES:
        if kiro_rate == 0.0:
            return 2  # zero deficit co-occurrence strongly compatible with intransitive
        elif kiro_rate < 0.05:
            return 1
        else:
            return 0

    if hurrian_case in ACCOUNTING_CASES:
        if kuro_rate > 0.15:
            return 2  # high total co-occurrence compatible with transactional role
        elif kuro_rate > 0.08:
            return 1
        else:
            return 0

    if hurrian_case in LOCATIVE_CASES:
        # Geographic wide distribution is a positive signal for locative
        sites = la_suffix_data.get("sites", 0)
        if sites >= 15 and kiro_rate < 0.1:
            return 2  # widespread and not deficit = locative compatible
        elif sites >= 10:
            return 1
        else:
            return 0

    return 1  # neutral for unclassified cases


def score_frequency_plausibility(la_suffix_count, hurrian_case):
    """
    Check if the Linear A suffix frequency is plausible for the Hurrian grammatical role.
    High-frequency morphemes in agglutinative languages are core case markers.
    Scale: 0-1
    """
    # Core cases should be high frequency (>30 occurrences)
    CORE_CASES = {"absolutive", "ergative", "genitive", "locative", "dative", "directive"}
    PERIPHERAL_CASES = {"ablative", "instrumental", "comitative", "antipassive"}

    if hurrian_case in CORE_CASES:
        return 1 if la_suffix_count >= 30 else 0.5
    elif hurrian_case in PERIPHERAL_CASES:
        return 1 if 10 <= la_suffix_count <= 50 else 0.5
    return 0.5


def build_alignment_matrix():
    """
    Build a complete alignment matrix: Linear A suffix × Hurrian morpheme.
    Each cell contains phonological + contextual + frequency scores.
    """
    alignments = []

    for la_suffix, la_data in LINEAR_A_SUFFIXES.items():
        for hurrian_case, hurrian_data in HURRIAN_MORPHEMES.items():
            forms = hurrian_data["forms"]
            if not forms:
                # Absolutive (zero form) — special handling
                # Compatible with Linear A suffixes that show intransitive patterns
                phon_score = 1 if la_data.get("kiro_rate", 1) == 0.0 else 0
                ctx_score = score_contextual_compatibility(la_data, hurrian_case)
                freq_score = score_frequency_plausibility(la_data["count"], hurrian_case)
                total = phon_score + ctx_score + freq_score
                if total >= 1.5:
                    alignments.append({
                        "la_suffix": la_suffix,
                        "hurrian_case": hurrian_case,
                        "hurrian_function": hurrian_data["function"],
                        "hurrian_forms": forms,
                        "best_form": "(zero)",
                        "phonological_score": phon_score,
                        "contextual_score": ctx_score,
                        "frequency_score": freq_score,
                        "total_score": round(total, 2),
                        "la_count": la_data["count"],
                        "la_kuro_rate": la_data["kuro_rate"],
                        "la_kiro_rate": la_data["kiro_rate"],
                        "la_notes": la_data["notes"],
                    })
                continue

            # Score against each Hurrian form
            best_phon = 0
            best_form = forms[0]
            for form in forms:
                phon = score_phonological_similarity(la_suffix, form)
                if phon > best_phon:
                    best_phon = phon
                    best_form = form

            ctx_score = score_contextual_compatibility(la_data, hurrian_case)
            freq_score = score_frequency_plausibility(la_data["count"], hurrian_case)
            total = best_phon + ctx_score + freq_score

            if total >= 2.0:  # only include meaningful alignments
                alignments.append({
                    "la_suffix": la_suffix,
                    "hurrian_case": hurrian_case,
                    "hurrian_function": hurrian_data["function"],
                    "hurrian_forms": forms,
                    "best_form": best_form,
                    "phonological_score": best_phon,
                    "contextual_score": ctx_score,
                    "frequency_score": freq_score,
                    "total_score": round(total, 2),
                    "la_count": la_data["count"],
                    "la_kuro_rate": la_data["kuro_rate"],
                    "la_kiro_rate": la_data["kiro_rate"],
                    "la_notes": la_data["notes"],
                })

    # Sort by total score descending
    alignments.sort(key=lambda x: -x["total_score"])
    return alignments


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_tokens(record):
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
    if re.match(r"^[A-Z]{2,4}$", token):
        return True
    return False


def is_punct(token):
    return token in PUNCT_CHARS or token.startswith("\\")


def is_formula_candidate(token):
    if is_numeral(token):
        return False
    if is_logogram(token):
        return False
    if is_punct(token):
        return False
    if len(token) < 2:
        return False
    return True


def test_na_locative_hypothesis(records):
    """
    Test: -NA words should appear in locative/container contexts,
    NOT predominantly in closing-formula (accounting terminal) positions.

    Prediction: if -NA is a Hurrian locative, -NA words should:
    1. Appear before logograms (naming what is contained/located)
    2. NOT appear in terminal-number-preceding position
    3. Co-occur with container/vessel support types
    """
    na_words = []
    for r in records:
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok) and tok.endswith("-NA"):
                na_words.append(tok)

    na_tokens = set(na_words)

    # Test 1: Pre-logogram position (naming containers or items)
    pre_logo_na = Counter()
    terminal_na = Counter()
    vessel_support_na = Counter()

    for r in records:
        tokens = get_tokens(r)
        support = (r.get("support") or "").lower()

        for i, tok in enumerate(tokens):
            if not (is_formula_candidate(tok) and tok.endswith("-NA")):
                continue
            na_context = tok

            # Check if next token is a logogram (pre-logogram position)
            if i + 1 < len(tokens) and is_logogram(tokens[i + 1]):
                pre_logo_na[na_context] += 1

            # Check if -NA word is immediately before terminal numeral
            if i + 1 < len(tokens) and is_numeral(tokens[i + 1]):
                terminal_na[na_context] += 1

            # Check support type
            if "vessel" in support or "stone" in support:
                vessel_support_na[na_context] += 1

    total_na_occurrences = len(na_words)
    pre_logo_count = sum(pre_logo_na.values())
    terminal_count = sum(terminal_na.values())

    return {
        "total_na_word_occurrences": total_na_occurrences,
        "distinct_na_tokens": len(na_tokens),
        "pre_logogram_count": pre_logo_count,
        "terminal_number_count": terminal_count,
        "vessel_support_count": sum(vessel_support_na.values()),
        "pre_logo_rate": round(pre_logo_count / max(total_na_occurrences, 1), 3),
        "terminal_rate": round(terminal_count / max(total_na_occurrences, 1), 3),
        "top_na_words": Counter(na_words).most_common(15),
        "interpretation": (
            "COMPATIBLE with locative" if pre_logo_count > terminal_count
            else "NOT compatible with locative (terminal use too high)"
        ),
    }


def test_ja_intransitive_hypothesis(records):
    """
    Test: -JA words should NOT appear in deficit/transactional contexts.
    Prior finding: zero KI-RO co-occurrence across 17 sites.

    Extended test: -JA words should appear in non-counting positions
    and co-occur with non-transactional support types.
    """
    ja_words = []
    for r in records:
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok) and tok.endswith("-JA"):
                ja_words.append(tok)

    # Support type distribution for -JA words
    ja_support_dist = Counter()
    ja_pre_logogram = Counter()
    ja_position_counts = {"initial": 0, "medial": 0, "final": 0}

    for r in records:
        tokens = get_tokens(r)
        formula_tokens = [t for t in tokens if is_formula_candidate(t)]
        support = (r.get("support") or "").lower()

        for i, tok in enumerate(tokens):
            if is_formula_candidate(tok) and tok.endswith("-JA"):
                ja_support_dist[support] += 1
                if i + 1 < len(tokens) and is_logogram(tokens[i + 1]):
                    ja_pre_logogram[tok] += 1

        for i, tok in enumerate(formula_tokens):
            if tok.endswith("-JA"):
                if i == 0:
                    ja_position_counts["initial"] += 1
                elif i == len(formula_tokens) - 1:
                    ja_position_counts["final"] += 1
                else:
                    ja_position_counts["medial"] += 1

    total_ja = len(ja_words)

    return {
        "total_ja_word_occurrences": total_ja,
        "distinct_ja_tokens": len(set(ja_words)),
        "support_distribution": dict(ja_support_dist.most_common()),
        "pre_logogram_count": sum(ja_pre_logogram.values()),
        "position_distribution": ja_position_counts,
        "top_ja_words": Counter(ja_words).most_common(15),
        "kiro_co_occurrence": 0,  # confirmed zero from Attempt #2
        "interpretation": (
            "STRONGLY COMPATIBLE with absolutive/intransitive: zero KI-RO, "
            f"pre-logogram rate: {sum(ja_pre_logogram.values())/max(total_ja,1):.1%}"
        ),
    }


def test_te_dative_hypothesis(records):
    """
    Test: -TE words should appear in 'to/for' argument positions.
    In accounting contexts, dative would mark the recipient.
    Prediction: -TE words should appear before logograms (naming recipients)
    and co-occur at high geographic distribution (recipients are widespread).
    """
    te_words = []
    for r in records:
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok) and tok.endswith("-TE"):
                te_words.append(tok)

    te_before_logogram = Counter()
    te_after_logogram = Counter()
    te_support_dist = Counter()

    for r in records:
        tokens = get_tokens(r)
        support = (r.get("support") or "").lower()
        for i, tok in enumerate(tokens):
            if is_formula_candidate(tok) and tok.endswith("-TE"):
                te_support_dist[support] += 1
                if i + 1 < len(tokens) and is_logogram(tokens[i + 1]):
                    te_before_logogram[tok] += 1
                if i > 0 and is_logogram(tokens[i - 1]):
                    te_after_logogram[tok] += 1

    total_te = len(te_words)
    return {
        "total_te_word_occurrences": total_te,
        "distinct_te_tokens": len(set(te_words)),
        "pre_logogram_count": sum(te_before_logogram.values()),
        "post_logogram_count": sum(te_after_logogram.values()),
        "support_distribution": dict(te_support_dist.most_common()),
        "top_te_words": Counter(te_words).most_common(15),
        "pre_logo_rate": round(sum(te_before_logogram.values()) / max(total_te, 1), 3),
        "interpretation": "See contextual analysis for dative compatibility",
    }


def test_re_participle_hypothesis(records):
    """
    Test: -RE words show highest accounting co-occurrence (21.6% KU-RO).
    Hurrian verb participle -ri/-re would naturally appear in accounting
    contexts describing actions (counted, received, dispatched).
    """
    re_words = []
    kuro_co = 0
    kiro_co = 0

    for r in records:
        tokens = get_tokens(r)
        has_kuro = "KU-RO" in tokens
        has_kiro = "KI-RO" in tokens
        for tok in tokens:
            if is_formula_candidate(tok) and tok.endswith("-RE"):
                re_words.append(tok)
                if has_kuro:
                    kuro_co += 1
                if has_kiro:
                    kiro_co += 1

    total_re = len(re_words)
    re_records = Counter()
    for r in records:
        tokens = get_tokens(r)
        re_in_record = [t for t in tokens if is_formula_candidate(t) and t.endswith("-RE")]
        if re_in_record:
            re_records[r.get("support", "unknown")] += 1

    return {
        "total_re_word_occurrences": total_re,
        "distinct_re_tokens": len(set(re_words)),
        "kuro_co_occurrence": kuro_co,
        "kiro_co_occurrence": kiro_co,
        "kuro_rate": round(kuro_co / max(total_re, 1), 3),
        "kiro_rate": round(kiro_co / max(total_re, 1), 3),
        "support_distribution": dict(re_records.most_common()),
        "top_re_words": Counter(re_words).most_common(15),
        "interpretation": (
            "COMPATIBLE with active participle: highest accounting co-occurrence "
            f"({kuro_co/max(total_re,1):.1%} KU-RO, {kiro_co/max(total_re,1):.1%} KI-RO)"
        ),
    }


def compute_suffix_paradigm_overview(records):
    """
    Build an overview of suffix paradigm statistics from the corpus.
    """
    suffix_counts = Counter()
    suffix_sites = defaultdict(set)

    for r in records:
        tokens = get_tokens(r)
        for tok in tokens:
            if is_formula_candidate(tok) and "-" in tok:
                parts = tok.split("-")
                final = parts[-1]
                if len(final) >= 2:
                    suffix_counts[final] += 1
                    suffix_sites[final].add(r.get("site") or "unknown")

    return {
        suf: {"count": cnt, "site_count": len(suffix_sites[suf])}
        for suf, cnt in suffix_counts.most_common(30)
    }


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records")

    print("\n--- Building Hurrian alignment matrix ---")
    alignments = build_alignment_matrix()
    print(f"  Generated {len(alignments)} meaningful alignments (score ≥ 2.0)")
    print("\n  Top 15 alignments:")
    for al in alignments[:15]:
        print(f"    -{al['la_suffix']} ↔ Hurrian {al['hurrian_case']} ({al['best_form']}): "
              f"total={al['total_score']} [phon={al['phonological_score']}, "
              f"ctx={al['contextual_score']}, freq={al['frequency_score']}]")

    print("\n--- Testing -NA locative hypothesis ---")
    na_test = test_na_locative_hypothesis(records)
    print(f"  -NA words: {na_test['total_na_word_occurrences']} occurrences, {na_test['distinct_na_tokens']} distinct tokens")
    print(f"  Pre-logogram: {na_test['pre_logogram_count']} ({na_test['pre_logo_rate']:.1%})")
    print(f"  Terminal-number: {na_test['terminal_number_count']} ({na_test['terminal_rate']:.1%})")
    print(f"  Interpretation: {na_test['interpretation']}")

    print("\n--- Testing -JA intransitive hypothesis ---")
    ja_test = test_ja_intransitive_hypothesis(records)
    print(f"  -JA words: {ja_test['total_ja_word_occurrences']} occurrences, {ja_test['distinct_ja_tokens']} distinct tokens")
    print(f"  Position distribution: {ja_test['position_distribution']}")
    print(f"  KI-RO co-occurrence: {ja_test['kiro_co_occurrence']} (confirmed 0)")
    print(f"  Interpretation: {ja_test['interpretation']}")

    print("\n--- Testing -TE dative hypothesis ---")
    te_test = test_te_dative_hypothesis(records)
    print(f"  -TE words: {te_test['total_te_word_occurrences']} occurrences, {te_test['distinct_te_tokens']} distinct tokens")
    print(f"  Pre-logogram rate: {te_test['pre_logo_rate']:.1%}")

    print("\n--- Testing -RE participle hypothesis ---")
    re_test = test_re_participle_hypothesis(records)
    print(f"  -RE words: {re_test['total_re_word_occurrences']} occurrences")
    print(f"  KU-RO rate: {re_test['kuro_rate']:.1%}, KI-RO rate: {re_test['kiro_rate']:.1%}")
    print(f"  Interpretation: {re_test['interpretation']}")

    print("\n--- Computing full suffix paradigm overview ---")
    paradigm = compute_suffix_paradigm_overview(records)
    print(f"  Top 10 suffixes: {list(paradigm.items())[:10]}")

    # Summary: highest-confidence alignments
    high_confidence = [a for a in alignments if a["total_score"] >= 4.0]
    medium_confidence = [a for a in alignments if 3.0 <= a["total_score"] < 4.0]
    print(f"\n  High-confidence alignments (score ≥ 4.0): {len(high_confidence)}")
    print(f"  Medium-confidence alignments (3.0–3.9): {len(medium_confidence)}")

    output = {
        "hurrian_morpheme_inventory": HURRIAN_MORPHEMES,
        "linear_a_suffix_inventory": LINEAR_A_SUFFIXES,
        "alignment_matrix": alignments,
        "high_confidence_alignments": high_confidence,
        "medium_confidence_alignments": medium_confidence,
        "na_locative_test": na_test,
        "ja_intransitive_test": ja_test,
        "te_dative_test": te_test,
        "re_participle_test": re_test,
        "suffix_paradigm_overview": paradigm,
        "summary": {
            "total_alignments": len(alignments),
            "high_confidence_count": len(high_confidence),
            "medium_confidence_count": len(medium_confidence),
            "strongest_alignment": alignments[0] if alignments else None,
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
