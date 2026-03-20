"""
H8c: Ergative Marker Search
Linear A Decipherment Project — 2026-03-20

Hypothesis: If -JA is an absolutive suffix (Medium-High confidence), an ergative
suffix should exist with an inverse distributional profile:
- Higher KI-RO co-occurrence (deficit/agent context)
- Higher VIR co-occurrence (person marker for transacting agent)
- Lower word-initial rate (ergative subjects appear later in clause)
- Lower KU-RO co-occurrence

Hurrian prediction: Hurrian ergative is -š, which may appear as -SI or -SA
in Linear A's consonant inventory.

Falsification: INCONCLUSIVE if no suffix scores ≥3× inverse-JA baseline at ≥5 sites.

Success threshold: One suffix scores ≥3× inverse-JA baseline AND appears at ≥5 sites
AND shows complementary distribution with -JA tokens (≥60% complementarity).

Corpus: corpus/linear_a_llm_master.jsonl (1721 records)
Output: analysis/outputs/ergative_candidate_2026-03-20.json
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path("corpus/linear_a_llm_master.jsonl")
OUTPUT_PATH = Path("analysis/outputs/ergative_candidate_2026-03-20.json")

KNOWN_LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG",
    "LANA", "OVS", "BOS", "CERV", "NI", "SA", "LUNA",
}
LOGOGRAM_PREFIXES = ("GRA+", "VIN+", "OLE+", "VIR+", "CYP+", "OLE2", "OLE3", "GRA2")

NUM_RE = re.compile(r"^\d+$|^[\u00bc\u00bd\u00be\u2150-\u215f\u2153-\u2189]")
PUNCT_CHARS = {"\U0001076b", "\U00010188", "𐄁", "—", "≈", "|", "·"}


def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_tokens(record):
    raw = record.get("transliteration_tokens", [])
    result = []
    for t in raw:
        if isinstance(t, dict):
            if t.get("type") == "token":
                result.append(t["value"])
        elif isinstance(t, str):
            result.append(t)
    return result


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
    return token in PUNCT_CHARS or token.startswith("\\") or len(token) == 0


def is_syllabic(token):
    """A syllabic phonetic token (not numeral, logogram, punct)."""
    if is_numeral(token) or is_logogram(token) or is_punct(token):
        return False
    if len(token) < 2:
        return False
    return True


def extract_final_syllable(token):
    """Extract the final syllable from a hyphenated syllabic token."""
    if not is_syllabic(token):
        return None
    parts = token.split("-")
    if len(parts) < 2:
        return None  # single-syllable token; skip
    return parts[-1]


def compute_suffix_profile(suffix, records):
    """
    For all syllabic tokens ending in `suffix`, compute:
    - Total occurrences (token-level, counting per inscription)
    - Records containing the suffix
    - Sites where it appears
    - KU-RO co-occurrence rate (same record)
    - KI-RO co-occurrence rate (same record)
    - VIR co-occurrence rate (same record)
    - Word-initial rate (position 0 in token list)
    - Word-terminal rate (last syllabic token before a logogram/numeral)
    """
    records_with_suffix = []
    total_token_occurrences = 0
    sites = set()
    kuro_cooc = 0
    kiro_cooc = 0
    vir_cooc = 0
    word_initial_count = 0
    word_terminal_count = 0
    total_tokens_analyzed = 0

    for r in records:
        tokens = get_tokens(r)
        syllabic_positions = [i for i, t in enumerate(tokens) if is_syllabic(t)]

        suffix_tokens_in_record = []
        for i, tok in enumerate(tokens):
            if not is_syllabic(tok):
                continue
            final = extract_final_syllable(tok)
            if final == suffix:
                suffix_tokens_in_record.append((i, tok))
                total_token_occurrences += 1
                total_tokens_analyzed += 1

                # Word-initial: position 0 OR directly follows a punct/divider
                if i == 0:
                    word_initial_count += 1
                elif is_punct(tokens[i - 1]) if i > 0 else False:
                    word_initial_count += 1

                # Word-terminal: last syllabic before a logogram or numeral
                post = tokens[i + 1] if i + 1 < len(tokens) else None
                if post and (is_logogram(post) or is_numeral(post)):
                    word_terminal_count += 1

        if suffix_tokens_in_record:
            records_with_suffix.append(r)
            sites.add(r.get("site", "Unknown"))
            if "KU-RO" in tokens:
                kuro_cooc += 1
            if "KI-RO" in tokens:
                kiro_cooc += 1
            if "VIR" in tokens:
                vir_cooc += 1

    n = len(records_with_suffix)
    return {
        "suffix": suffix,
        "total_token_occurrences": total_token_occurrences,
        "records_with_suffix": n,
        "sites": sorted(s for s in sites if s is not None),
        "site_count": len(sites),
        "kuro_cooccurrence_rate": round(kuro_cooc / n, 3) if n else 0,
        "kiro_cooccurrence_rate": round(kiro_cooc / n, 3) if n else 0,
        "vir_cooccurrence_rate": round(vir_cooc / n, 3) if n else 0,
        "word_initial_rate": round(word_initial_count / total_token_occurrences, 3) if total_token_occurrences else 0,
        "word_terminal_rate": round(word_terminal_count / total_token_occurrences, 3) if total_token_occurrences else 0,
    }


def compute_inverse_ja_score(profile, ja_profile):
    """
    Inverse-JA score = ratio of ergative-like features to absolutive-like features.

    Ergative-like: KI-RO co-occ (high), VIR co-occ (high), word-terminal rate (high)
    Absolutive-like: KU-RO co-occ (high), word-initial rate (high)

    Score = (kiro_rate + vir_rate + terminal_rate + 1e-6) /
            (kuro_rate + initial_rate + 1e-6)

    Normalized by -JA's own ratio so that -JA scores ≈ 1.0
    """
    eps = 1e-6
    ergative_score = profile["kiro_cooccurrence_rate"] + profile["vir_cooccurrence_rate"] + profile["word_terminal_rate"] + eps
    absolutive_score = profile["kuro_cooccurrence_rate"] + profile["word_initial_rate"] + eps
    raw_score = ergative_score / absolutive_score

    ja_ergative = ja_profile["kiro_cooccurrence_rate"] + ja_profile["vir_cooccurrence_rate"] + ja_profile["word_terminal_rate"] + eps
    ja_absolutive = ja_profile["kuro_cooccurrence_rate"] + ja_profile["word_initial_rate"] + eps
    ja_raw = ja_ergative / ja_absolutive

    # Normalized: how much MORE ergative-like is this suffix than -JA?
    # -JA should score ≈ 1.0, ergative candidates should score >> 1.0
    normalized = raw_score / ja_raw if ja_raw > 0 else 0
    return round(normalized, 3)


def complementarity_test(suffix_candidate, records):
    """
    For records containing the ergative candidate suffix, what % do NOT contain -JA words?
    High complementarity (≥60%) supports ergative-absolutive split.
    """
    candidate_records = set()
    ja_records = set()

    for r in records:
        tokens = get_tokens(r)
        has_candidate = any(
            is_syllabic(t) and extract_final_syllable(t) == suffix_candidate
            for t in tokens
        )
        has_ja = any(
            is_syllabic(t) and extract_final_syllable(t) == "JA"
            for t in tokens
        )
        if has_candidate:
            candidate_records.add(r.get("id"))
        if has_ja:
            ja_records.add(r.get("id"))

    both = candidate_records & ja_records
    candidate_only = candidate_records - ja_records
    complementarity = len(candidate_only) / len(candidate_records) if candidate_records else 0
    return {
        "candidate_records": len(candidate_records),
        "ja_records": len(ja_records),
        "overlap_records": len(both),
        "candidate_only_records": len(candidate_only),
        "complementarity_rate": round(complementarity, 3),
        "complementarity_threshold_60pct_met": complementarity >= 0.60,
    }


def main():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"Loaded {len(records)} records.")

    # All candidate suffixes to test
    suffixes_to_test = [
        "JA",  # absolutive baseline
        "TE", "NA", "RE", "RO", "TI", "MI", "NE", "SI", "WA", "KA", "RA", "DA",
        "SE", "MU", "NU", "KE", "DI", "RU", "TU", "DU", "PA", "PI",
    ]

    print("Computing suffix profiles...")
    profiles = {}
    for suffix in suffixes_to_test:
        print(f"  Analyzing -{suffix}...")
        profiles[suffix] = compute_suffix_profile(suffix, records)

    ja_profile = profiles["JA"]

    print("Computing inverse-JA scores...")
    scored = []
    for suffix, profile in profiles.items():
        if profile["records_with_suffix"] < 5:
            continue  # Skip low-frequency suffixes
        inv_score = compute_inverse_ja_score(profile, ja_profile)
        scored.append({
            **profile,
            "inverse_ja_score": inv_score,
        })

    # Sort by inverse-JA score descending
    scored.sort(key=lambda x: -x["inverse_ja_score"])

    # Top candidate (excluding JA itself)
    non_ja_candidates = [s for s in scored if s["suffix"] != "JA"]
    top_candidate = non_ja_candidates[0] if non_ja_candidates else None

    # Complementarity test for top candidates
    complementarity_results = {}
    for s in non_ja_candidates[:5]:
        suf = s["suffix"]
        print(f"  Complementarity test for -{suf}...")
        complementarity_results[suf] = complementarity_test(suf, records)

    # Assessment thresholds
    if top_candidate:
        top_inv_score = top_candidate["inverse_ja_score"]
        top_site_count = top_candidate["site_count"]
        top_comp = complementarity_results.get(top_candidate["suffix"], {}).get("complementarity_rate", 0)
        passed_score = top_inv_score >= 3.0
        passed_sites = top_site_count >= 5
        passed_comp = top_comp >= 0.60
        hypothesis_supported = passed_score and passed_sites
        strong_confirmation = hypothesis_supported and passed_comp
    else:
        top_inv_score = 0
        top_site_count = 0
        top_comp = 0
        passed_score = False
        passed_sites = False
        passed_comp = False
        hypothesis_supported = False
        strong_confirmation = False

    # Hurrian prediction check: -SI or -SA should rank high
    hurrian_candidates = {"SI", "SA"}
    si_rank = next((i for i, s in enumerate(non_ja_candidates) if s["suffix"] in hurrian_candidates), None)

    results = {
        "ja_baseline_profile": ja_profile,
        "all_suffix_scores": scored,
        "top_ergative_candidate": top_candidate,
        "complementarity_tests": complementarity_results,
        "hurrian_si_sa_rank": si_rank,
        "hurrian_prediction_check": {
            "si_profile": profiles.get("SI"),
            "sa_profile": profiles.get("SA"),
            "si_rank_among_candidates": si_rank,
            "hurrian_prediction_supported": si_rank is not None and si_rank <= 3,
        },
        "hypothesis_assessment": {
            "top_candidate_suffix": top_candidate["suffix"] if top_candidate else None,
            "top_inverse_ja_score": top_inv_score,
            "threshold_score_ge_3x": passed_score,
            "threshold_site_count_ge_5": passed_sites,
            "threshold_complementarity_ge_60pct": passed_comp,
            "hypothesis_supported": hypothesis_supported,
            "strong_confirmation": strong_confirmation,
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {OUTPUT_PATH}")

    # Print summary
    print("\n=== ERGATIVE MARKER SEARCH (H8c) ===")
    print(f"\n-JA BASELINE (absolutive):")
    print(f"  Records: {ja_profile['records_with_suffix']}, Sites: {ja_profile['site_count']}")
    print(f"  KU-RO rate: {ja_profile['kuro_cooccurrence_rate']:.3f}")
    print(f"  KI-RO rate: {ja_profile['kiro_cooccurrence_rate']:.3f}")
    print(f"  VIR rate: {ja_profile['vir_cooccurrence_rate']:.3f}")
    print(f"  Word-initial rate: {ja_profile['word_initial_rate']:.3f}")
    print(f"  Word-terminal rate: {ja_profile['word_terminal_rate']:.3f}")

    print(f"\nTOP 10 SUFFIXES BY INVERSE-JA SCORE:")
    print(f"{'Suffix':<8} {'Inv-JA':>8} {'Sites':>6} {'Records':>8} {'KI-RO%':>8} {'VIR%':>7} {'Init%':>7} {'Term%':>7}")
    for s in scored[:10]:
        print(f"-{s['suffix']:<7} {s['inverse_ja_score']:>8.3f} {s['site_count']:>6} {s['records_with_suffix']:>8} "
              f"{s['kiro_cooccurrence_rate']:>8.3f} {s['vir_cooccurrence_rate']:>7.3f} "
              f"{s['word_initial_rate']:>7.3f} {s['word_terminal_rate']:>7.3f}")

    if top_candidate:
        print(f"\nTOP ERGATIVE CANDIDATE: -{top_candidate['suffix']}")
        print(f"  Inverse-JA score: {top_candidate['inverse_ja_score']:.3f} (threshold: ≥3.0)")
        print(f"  Sites: {top_candidate['sites']}")
        comp = complementarity_results.get(top_candidate["suffix"], {})
        print(f"  Complementarity with -JA: {comp.get('complementarity_rate', 0):.1%} (threshold: ≥60%)")

    hurrian_check = results["hurrian_prediction_check"]
    si_profile = hurrian_check.get("si_profile")
    sa_profile = hurrian_check.get("sa_profile")
    if si_profile:
        print(f"\nHurrian prediction (-SI): rank {si_rank}, inv-JA score: {compute_inverse_ja_score(si_profile, ja_profile):.3f}")
    if sa_profile:
        print(f"Hurrian prediction (-SA): inv-JA score: {compute_inverse_ja_score(sa_profile, ja_profile):.3f}")

    print(f"\nH8c hypothesis assessment: {results['hypothesis_assessment']}")
    verdict = hypothesis_supported
    print(f"\n{'✓ H8c SUPPORTED' if verdict else ('INCONCLUSIVE' if not passed_score else '✗ H8c FAILED')}")


if __name__ == "__main__":
    main()
