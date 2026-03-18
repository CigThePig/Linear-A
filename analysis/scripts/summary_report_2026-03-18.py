"""
Summary Report Generator
Linear A Decipherment Project — 2026-03-18

Reads both analysis output JSONs and generates a human-readable markdown report.
Output: analysis/outputs/summary_report_2026-03-18.md
"""

import json
from pathlib import Path

ADMIN_JSON = Path("analysis/outputs/admin_formula_results_2026-03-18.json")
SUFFIX_JSON = Path("analysis/outputs/suffix_paradigm_results_2026-03-18.json")
REPORT_PATH = Path("analysis/outputs/summary_report_2026-03-18.md")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def evaluate_confidence(admin_data, suffix_data):
    """
    Determine hypothesis confidence based on results:
    - HIGH: 3+ new formula tokens at 3+ sites with 10+ occurrences each
    - MEDIUM: 1-2 strong candidates, OR suffix clustering confirmed at 2+ sites
    - LOW/INCONCLUSIVE: only HT patterns, or nothing beyond known KU-RO/KI-RO
    - FAILED: no consistent signal
    """
    strong = admin_data.get("strong_closing_candidates", {})
    # Remove known formulas (KU-RO and KI-RO already known)
    new_candidates = {
        tok: data for tok, data in strong.items()
        if tok not in ("KU-RO", "KI-RO")
    }
    n_new = len(new_candidates)

    # Suffix clustering: check if top suffixes show differentiated logogram co-occurrence
    suffix_stats = suffix_data.get("suffix_stats", {})
    top_suffixes = sorted(suffix_stats.items(), key=lambda x: -x[1]["record_count"])[:6]
    differentiated_suffixes = 0
    for suffix, data in top_suffixes:
        top_logos = data.get("top_cooccurring_logograms", [])
        if top_logos and top_logos[0]["cooccurrences"] >= 5 and data["site_count"] >= 2:
            differentiated_suffixes += 1

    if n_new >= 3:
        outcome = "PARTIAL SUCCESS"
        confidence = "Medium-High"
        tier = "Tier 3 (Formulaic)"
    elif n_new >= 1 or differentiated_suffixes >= 3:
        outcome = "PARTIAL SUCCESS"
        confidence = "Medium"
        tier = "Tier 3 (Formulaic) / Tier 5 (Grammatical, preliminary)"
    elif differentiated_suffixes >= 1:
        outcome = "INCONCLUSIVE"
        confidence = "Low-Medium"
        tier = "Tier 1 (Structural) / Tier 5 (preliminary)"
    else:
        outcome = "INCONCLUSIVE"
        confidence = "Low"
        tier = "Tier 1 (Structural)"

    return outcome, confidence, tier, n_new, differentiated_suffixes


def generate_report(admin_data, suffix_data):
    outcome, confidence, tier, n_new_formula, n_diff_suffixes = evaluate_confidence(
        admin_data, suffix_data
    )

    lines = []
    lines.append("# Linear A Administrative Formula Bootstrapping — Analysis Report")
    lines.append("**Date:** 2026-03-18")
    lines.append(f"**Outcome:** {outcome}")
    lines.append(f"**Confidence:** {confidence}")
    lines.append(f"**Evidence tier reached:** {tier}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # === SECTION 1: KU-RO / KI-RO Confirmation ===
    lines.append("## 1. Anchor Token Verification")
    lines.append("")
    lines.append(f"- **KU-RO** occurrences in corpus: {admin_data['kuro_count']}")
    lines.append(f"  Sites: {', '.join(admin_data['kuro_sites'])}")
    lines.append(f"- **KI-RO** occurrences in corpus: {admin_data['kiro_count']}")
    lines.append(f"  Sites: {', '.join(admin_data['kiro_sites'])}")
    lines.append("")

    # Sample KU-RO contexts
    lines.append("### Sample KU-RO Context Windows")
    lines.append("")
    for ctx in admin_data.get("kuro_contexts", [])[:5]:
        pre = " | ".join(ctx["tokens_before"]) or "(start)"
        post = " | ".join(ctx["tokens_after"]) or "(end)"
        lines.append(f"- `{ctx['record_id']}` ({ctx['site']}): `[{pre}] **KU-RO** [{post}]`")
    lines.append("")

    # === SECTION 2: Closing Formula Candidates ===
    lines.append("## 2. Closing Formula Slot Analysis")
    lines.append("")
    lines.append(
        "Tokens appearing immediately before the last numeral in a record "
        "(the 'closing formula slot' — same structural position as KU-RO):"
    )
    lines.append("")
    lines.append("| Token | Count | Sites | Site Count |")
    lines.append("|-------|-------|-------|-----------|")

    terminal = admin_data.get("terminal_slot_tokens", {})
    shown = 0
    for tok, data in sorted(terminal.items(), key=lambda x: -x[1]["count"]):
        if shown >= 25:
            break
        sites_str = ", ".join(data["sites"][:4])
        if len(data["sites"]) > 4:
            sites_str += f" +{len(data['sites'])-4}"
        lines.append(
            f"| `{tok}` | {data['count']} | {sites_str} | {data['site_count']} |"
        )
        shown += 1
    lines.append("")

    # Strong candidates
    strong = admin_data.get("strong_closing_candidates", {})
    new_candidates = {
        tok: data for tok, data in strong.items()
        if tok not in ("KU-RO", "KI-RO")
    }
    lines.append(f"### Strong New Candidates (3+ sites, 5+ occurrences): {len(new_candidates)}")
    lines.append("")
    if new_candidates:
        for tok, data in sorted(new_candidates.items(), key=lambda x: -x[1]["count"])[:10]:
            lines.append(
                f"- **`{tok}`**: count={data['count']}, sites={data['site_count']}, "
                f"examples: {data['example_records'][:3]}"
            )
    else:
        lines.append("_No tokens beyond KU-RO/KI-RO met the 3+ sites, 5+ occurrences threshold._")
    lines.append("")

    # === SECTION 3: Formula Bigrams ===
    lines.append("## 3. Recurring Formula Bigrams")
    lines.append("")
    bigrams = admin_data.get("formula_bigrams", {})
    if bigrams:
        lines.append("| Bigram | Count | Sites |")
        lines.append("|--------|-------|-------|")
        for bigram, data in sorted(bigrams.items(), key=lambda x: -x[1]["count"])[:20]:
            sites_str = ", ".join(data["sites"][:3])
            lines.append(f"| `{bigram}` | {data['count']} | {sites_str} |")
    else:
        lines.append("_No recurring bigrams found with 3+ occurrences._")
    lines.append("")

    # === SECTION 4: Opening Formula ===
    lines.append("## 4. Opening Formula Tokens")
    lines.append("")
    lines.append("Most frequent first tokens in records (possible opening formulas):")
    lines.append("")
    lines.append("| Token | Count | Sites |")
    lines.append("|-------|-------|-------|")
    opening = admin_data.get("opening_tokens", {})
    shown = 0
    for tok, data in opening.items():
        if shown >= 15:
            break
        if data["count"] >= 3:
            sites_str = ", ".join(data["sites"][:3])
            lines.append(f"| `{tok}` | {data['count']} | {sites_str} |")
            shown += 1
    lines.append("")

    # === SECTION 5: Suffix Analysis ===
    lines.append("## 5. Suffix Paradigm Analysis")
    lines.append("")
    lines.append(f"Total distinct final syllables found: {suffix_data['total_suffixes_found']}")
    lines.append("")
    lines.append("### Top Suffixes by Record Count")
    lines.append("")
    lines.append(
        "| Suffix | Records | Sites | KU-RO co-occ | KI-RO co-occ | Top logograms | Hurrian parallel |"
    )
    lines.append(
        "|--------|---------|-------|--------------|--------------|---------------|-----------------|"
    )
    top_suffixes = sorted(
        suffix_data["suffix_stats"].items(), key=lambda x: -x[1]["record_count"]
    )[:12]
    for suffix, data in top_suffixes:
        top_logos = ", ".join(
            f"{e['logogram']}({e['cooccurrences']})"
            for e in data["top_cooccurring_logograms"][:3]
        )
        hurrian = data.get("hurrian_parallel") or "—"
        # Truncate hurrian
        hurrian = hurrian[:30] + "..." if len(hurrian) > 30 else hurrian
        lines.append(
            f"| -{suffix} | {data['record_count']} | {data['site_count']} | "
            f"{data['records_with_kuro']} | {data['records_with_kiro']} | "
            f"{top_logos} | {hurrian} |"
        )
    lines.append("")

    # === SECTION 6: Hurrian Comparison ===
    lines.append("## 6. Hurrian Morphology Comparison")
    lines.append("")
    lines.append(
        "Cross-checking Linear A top suffixes against Hurrian case inventory "
        "(Tier 5 hypothesis — Low confidence without further testing):"
    )
    lines.append("")
    hurrian = suffix_data.get("hurrian_comparison", {})
    for suffix, data in hurrian.items():
        rate_kuro = data.get("kuro_cooccurrence_rate", 0)
        rate_kiro = data.get("kiro_cooccurrence_rate", 0)
        lines.append(
            f"- **-{suffix}** ({data['record_count']} records, {data['site_count']} sites): "
            f"{data['hurrian_meaning']} | "
            f"KU-RO co-occ rate: {rate_kuro:.1%} | "
            f"KI-RO co-occ rate: {rate_kiro:.1%}"
        )
    lines.append("")

    # === SECTION 7: Interpretation ===
    lines.append("## 7. Interpretation")
    lines.append("")
    lines.append(
        "**Phrasing note:** All interpretations below use cautious language. "
        "These are working hypotheses, not decipherment claims."
    )
    lines.append("")

    if n_new_formula >= 3:
        lines.append(
            f"The positional analysis is consistent with {n_new_formula} tokens beyond KU-RO/KI-RO "
            "occupying the closing-formula slot. These may represent additional administrative terms "
            "(e.g., 'received', 'dispatched', 'assessed'). Cross-site attestation suggests these "
            "are not scribal idiosyncrasies."
        )
    elif n_new_formula >= 1:
        lines.append(
            f"The positional analysis suggests {n_new_formula} additional token(s) may occupy "
            "the closing-formula slot. Further investigation is needed to distinguish genuine "
            "formula words from coincidental positional occurrences."
        )
    else:
        lines.append(
            "The positional analysis did not identify strong new candidates in the KU-RO structural "
            "slot beyond the already-known KU-RO and KI-RO. This may reflect the sparseness of "
            "well-structured accounting tablets outside Haghia Triada, or that KU-RO/KI-RO are "
            "unusually salient formula words with few direct parallels."
        )
    lines.append("")

    if n_diff_suffixes >= 3:
        lines.append(
            "The suffix distribution shows differentiated logogram co-occurrence patterns, "
            "consistent with suffixes marking grammatical roles (case, number, or aspect). "
            "This provides preliminary Tier 5 evidence for agglutinative morphology, "
            "supporting Davis (2014)'s structural analysis."
        )
    lines.append("")

    # === SECTION 8: Confidence Summary ===
    lines.append("## 8. Confidence Rating Summary")
    lines.append("")
    lines.append(f"| Dimension | Rating | Basis |")
    lines.append(f"|-----------|--------|-------|")
    lines.append(
        f"| New closing-formula tokens | "
        f"{'Medium' if n_new_formula >= 1 else 'Low'} | "
        f"{n_new_formula} candidates found |"
    )
    lines.append(
        f"| Suffix differentiation | "
        f"{'Medium' if n_diff_suffixes >= 3 else 'Low'} | "
        f"{n_diff_suffixes}/6 top suffixes show logogram clustering |"
    )
    lines.append(
        f"| Cross-site validation | "
        f"{'Medium' if admin_data['kuro_count'] >= 30 else 'Low'} | "
        f"KU-RO at {len(admin_data['kuro_sites'])} sites |"
    )
    lines.append(f"| **Overall** | **{confidence}** | **{outcome}** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_This report was generated automatically from corpus analysis. "
        "All claims require manual review before promotion to `findings/`._"
    )

    return "\n".join(lines), outcome, confidence, tier


def main():
    print("Loading analysis outputs...")
    admin_data = load_json(ADMIN_JSON)
    suffix_data = load_json(SUFFIX_JSON)

    print("Generating summary report...")
    report_text, outcome, confidence, tier = generate_report(admin_data, suffix_data)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        f.write(report_text)

    print(f"Report written to {REPORT_PATH}")
    print(f"\n=== FINAL EVALUATION ===")
    print(f"Outcome:    {outcome}")
    print(f"Confidence: {confidence}")
    print(f"Tier:       {tier}")


if __name__ == "__main__":
    main()
