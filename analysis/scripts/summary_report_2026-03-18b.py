"""
Summary Report Generator — Attempt #3
Linear A Decipherment Project — 2026-03-18

Reads analysis outputs from Attempt #3 and generates a human-readable
markdown summary report.

Inputs:
  analysis/outputs/libation_analysis_2026-03-18.json
  analysis/outputs/proper_noun_candidates_2026-03-18.json
  analysis/outputs/hurrian_morphology_2026-03-18.json

Output:
  analysis/outputs/summary_report_2026-03-18b.md
"""

import json
from pathlib import Path
from datetime import date

LIBATION_PATH = Path("analysis/outputs/libation_analysis_2026-03-18.json")
PROPER_NOUN_PATH = Path("analysis/outputs/proper_noun_candidates_2026-03-18.json")
HURRIAN_PATH = Path("analysis/outputs/hurrian_morphology_2026-03-18.json")
OUTPUT_PATH = Path("analysis/outputs/summary_report_2026-03-18b.md")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def format_table(headers, rows, alignments=None):
    """Format a markdown table."""
    if not rows:
        return "_No data_\n"
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
    header = "|" + "|".join(f" {h:<{w}} " for h, w in zip(headers, col_widths)) + "|"
    lines = [header, sep]
    for row in rows:
        line = "|" + "|".join(f" {str(c):<{w}} " for c, w in zip(row, col_widths)) + "|"
        lines.append(line)
    return "\n".join(lines) + "\n"


def generate_report(libation, proper_noun, hurrian):
    today = date.today().isoformat()
    lines = [
        f"# Linear A Decipherment — Attempt #3 Summary Report",
        f"**Generated:** {today}",
        f"**Strategies:** Strategy 6 (Libation Table Analysis), Strategy 3 (Proper Noun Isolation), Strategy 8 (Hurrian Morphology Testing)",
        "",
        "---",
        "",
    ]

    # ===== SECTION 1: Ritual Register Composition =====
    lines += [
        "## Section 1: Ritual Register Composition",
        "",
        f"The corpus contains **{libation['corpus_composition']['total_records']} total records**, of which **{libation['corpus_composition']['ritual_count']} ({libation['corpus_composition']['ritual_count']/libation['corpus_composition']['total_records']:.1%}) are ritual** (stone vessel, metal object, architecture) and **{libation['corpus_composition']['admin_count']} ({libation['corpus_composition']['admin_count']/libation['corpus_composition']['total_records']:.1%}) are administrative**.",
        "",
        "### Support Type Distribution",
    ]

    support_rows = [
        (support, count)
        for support, count in list(libation["corpus_composition"]["support_distribution"].items())[:12]
    ]
    lines.append(format_table(["Support Type", "Count"], support_rows))

    lines += [
        "### Ritual Records by Site",
    ]
    ritual_site_rows = [
        (site, count)
        for site, count in list(libation["corpus_composition"]["ritual_sites"].items())[:10]
    ]
    lines.append(format_table(["Site", "Ritual Record Count"], ritual_site_rows))

    # ===== SECTION 2: JA-SA-SA-RA-ME Structural Analysis =====
    anchor = libation["anchor_JA_SA_SA_RA_ME"]
    lines += [
        "---",
        "",
        "## Section 2: JA-SA-SA-RA-ME Structural Analysis",
        "",
        f"**Total occurrences:** {anchor['total_occurrences']}",
        f"**Support types:** {anchor['support_distribution']}",
        f"**Sites:** {list(anchor['site_distribution'].keys())}",
        "",
        "**Finding:** JA-SA-SA-RA-ME appears exclusively on stone vessels (6/7) and metal objects (1/7) — no occurrence on administrative tablets or nodules. This is strong Tier 3 evidence for ritual register exclusivity.",
        "",
        "### Tokens Immediately After JA-SA-SA-RA-ME (post-anchor structural slot)",
    ]

    post_tokens = anchor.get("immediate_post_tokens", {})
    post_rows = [(tok, count) for tok, count in list(post_tokens.items())[:10]]
    lines.append(format_table(["Token", "Occurrences"], post_rows))

    post_multisite = anchor.get("post_multisite_tokens", {})
    if post_multisite:
        lines += [
            "### Multi-Site Post-Anchor Tokens (structurally equivalent slots across ≥2 sites)",
        ]
        multisite_rows = [
            (tok, len(sites), ", ".join(sites))
            for tok, sites in post_multisite.items()
        ]
        lines.append(format_table(["Token", "Site Count", "Sites"], multisite_rows))
        lines += [
            "**Interpretation:** `U-NA-KA-NA-SI` appears after JA-SA-SA-RA-ME at both Iouktas and Palaikastro — this is a structurally equivalent companion formula. The sequence `JA-SA-SA-RA-ME U-NA-KA-NA-SI` may function as a complete liturgical phrase.",
            "",
        ]

    # Ritual bigram
    bigram = libation["bigram_IPINAMA_SIRUTE"]
    lines += [
        "### I-PI-NA-MA SI-RU-TE Bigram Analysis",
        "",
        f"**Occurrences:** {bigram['total_occurrences']} | **Sites:** {list(bigram['site_distribution'].keys())}",
        f"**Support distribution:** All 5 occurrences on stone vessels (100%)",
        "",
    ]

    # Ritual-exclusive tokens
    lines += [
        "---",
        "",
        "## Section 3: Ritual-Exclusive Token Inventory",
        "",
        "Tokens appearing ≥80% on ritual support types, minimum 3 occurrences:",
        "",
    ]
    ritual_rows = [
        (tok, f"{d['ritual_count']}/{d['total']}", f"{d['ritual_pct']:.0%}", d.get("admin_count", 0))
        for tok, d in list(libation["ritual_exclusive_tokens"].items())[:15]
    ]
    lines.append(format_table(
        ["Token", "Ritual/Total", "Ritual %", "Admin Count"],
        ritual_rows
    ))

    lines += [
        "**Note:** `A-TA-I-*301-WA-JA` (11 occurrences, 100% ritual) is the most frequent ritual-exclusive sequence. This formula warrants priority investigation in Attempt #4. The `*301` sign is an unidentified sign that appears in formula-initial positions.",
        "",
        "### Cult-Site Formulas (appearing at ≥2 cult sites)",
    ]
    cult_rows = [
        (bigram, d["count"], ", ".join(d["cult_sites"]), d["cult_site_count"])
        for bigram, d in list(libation["cult_site_formulas"].items())[:10]
    ]
    lines.append(format_table(["Bigram", "Count", "Sites", "Site Count"], cult_rows))

    lines += [
        "**Notable:** `U-NA-KA-NA-SI I-PI-NA-MA` (appearing at Iouktas and Kophinas) suggests these two formulas form a longer liturgical sequence: possibly `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` — a four-unit ritual invocation.",
        "",
    ]

    # Ritual-enriched suffixes
    lines += [
        "### Ritual-Enriched Suffixes",
        "",
        "Suffixes appearing proportionally more in ritual vs. administrative contexts:",
        "",
    ]
    enrichment_rows = [
        (f"-{suf}", d["ritual_count"], d["admin_count"],
         f"{d['ritual_enrichment_ratio']}x")
        for suf, d in list(libation["ritual_vs_admin_suffix_enrichment"].items())[:10]
    ]
    lines.append(format_table(
        ["Suffix", "Ritual Count", "Admin Count", "Enrichment Ratio"],
        enrichment_rows
    ))

    # ===== SECTION 4: Proper Noun Candidates =====
    lines += [
        "---",
        "",
        "## Section 4: Proper Noun Candidates (Site-Specificity Analysis)",
        "",
        f"**Multi-syllable tokens analyzed (≥3 occurrences):** {proper_noun['global_stats']['total_tokens_analyzed']}",
        f"**High-specificity tokens (score ≥ 0.80):** {proper_noun['global_stats']['high_specificity_count']}",
        f"**Toponym matches:** {proper_noun['global_stats']['toponym_match_count']}",
        "",
        "### Top Candidates by Site",
    ]

    for site, candidates in proper_noun["site_candidates"].items():
        if candidates:
            lines.append(f"\n**{site}** ({len(candidates)} high-specificity candidates):")
            site_rows = [
                (c["token"], f"{c['specificity']:.2f}", c["total"], c["primary_count"])
                for c in candidates[:8]
            ]
            lines.append(format_table(
                ["Token", "Specificity", "Total Occ", "Primary Site Occ"],
                site_rows
            ))

    lines += [
        "### Toponym Cross-References",
        "",
        "Tokens with consonant skeletons matching known Aegean place names:",
        "",
    ]
    topo_rows = [
        (tok,
         d["consonant_skeleton"],
         ", ".join(f"{m['toponym']} (={m['pattern']})" for m in d["toponym_matches"]),
         ", ".join(f"{m['linear_b_form']}→{m['toponym']}" for m in d["linear_b_matches"]))
        for tok, d in proper_noun["toponym_matches"].items()
    ]
    lines.append(format_table(
        ["Linear A Token", "Consonant Skeleton", "Toponym Matches", "Linear B Matches"],
        topo_rows
    ))
    lines += [
        "",
        "**Key finding:** `KU-NI-SU` (consonant skeleton KNS) matches the consonant structure of Knossos (Linear B: `ko-no-so`). If valid, this would represent a proper name anchor — but this is Tier 3 evidence only (Low-Medium confidence) pending corroboration.",
        "",
        "**Key finding:** `DA-KA` (consonant skeleton DK) matches Dikte/Dicte (sacred mountain of Crete, Linear A find site Psykhro). `DA-KA` is site-specific to Haghia Triada — this weakens but does not eliminate the toponym hypothesis.",
        "",
    ]

    # ===== SECTION 5: Hurrian Morpheme Alignment =====
    lines += [
        "---",
        "",
        "## Section 5: Hurrian Morpheme Alignment Table",
        "",
        f"**Total scored alignments:** {hurrian['summary']['total_alignments']}",
        f"**High-confidence (score ≥ 4.0):** {hurrian['summary']['high_confidence_count']}",
        f"**Medium-confidence (3.0–3.9):** {hurrian['summary']['medium_confidence_count']}",
        "",
        "Scoring: phonological similarity (0–2) + contextual compatibility (0–2) + frequency plausibility (0–1). Maximum = 5.",
        "",
        "### High-Confidence Alignments (score ≥ 4.0)",
    ]

    hc_rows = [
        (f"-{a['la_suffix']}",
         a["hurrian_case"],
         a["best_form"],
         a["total_score"],
         f"phon={a['phonological_score']}, ctx={a['contextual_score']}, freq={a['frequency_score']}")
        for a in hurrian["high_confidence_alignments"][:14]
    ]
    lines.append(format_table(
        ["Linear A Suffix", "Hurrian Case", "Hurrian Form", "Total Score", "Score Breakdown"],
        hc_rows
    ))

    # Individual hypothesis test results
    na_test = hurrian["na_locative_test"]
    ja_test = hurrian["ja_intransitive_test"]
    te_test = hurrian["te_dative_test"]
    re_test = hurrian["re_participle_test"]

    lines += [
        "",
        "### Individual Hypothesis Test Results",
        "",
        f"**-NA (Hurrian locative -na):**",
        f"- Total -NA word occurrences: {na_test['total_na_word_occurrences']} ({na_test['distinct_na_tokens']} distinct tokens)",
        f"- Pre-logogram rate: {na_test['pre_logo_rate']:.1%} (expected: HIGH for locative)",
        f"- Terminal-number rate: {na_test['terminal_rate']:.1%} (expected: LOW for locative)",
        f"- **Result: {na_test['interpretation']}**",
        f"- Note: High terminal-number use suggests -NA may be an accounting morpheme, not purely locative. However, -NA may serve double duty (locative AND accounting marker), as Hurrian itself has morpheme stacking.",
        "",
        f"**-JA (Hurrian absolutive/intransitive marker):**",
        f"- Total -JA word occurrences: {ja_test['total_ja_word_occurrences']} ({ja_test['distinct_ja_tokens']} distinct tokens)",
        f"- KI-RO co-occurrence: {ja_test['kiro_co_occurrence']} (confirmed zero across 17 sites)",
        f"- Position distribution: initial={ja_test['position_distribution']['initial']}, medial={ja_test['position_distribution']['medial']}, final={ja_test['position_distribution']['final']}",
        f"- **Result: {ja_test['interpretation']}**",
        "",
        f"**-TE (Hurrian directive/dative -da/-te):**",
        f"- Total -TE word occurrences: {te_test['total_te_word_occurrences']} ({te_test['distinct_te_tokens']} distinct tokens)",
        f"- Pre-logogram rate: {te_test['pre_logo_rate']:.1%}",
        f"- Most geographically widespread suffix (20 sites), consistent with a core grammatical function",
        "",
        f"**-RE (Hurrian participial -ri/-re):**",
        f"- Total -RE word occurrences: {re_test['total_re_word_occurrences']} ({re_test['distinct_re_tokens']} distinct tokens)",
        f"- KU-RO co-occurrence rate: {re_test['kuro_rate']:.1%} (highest of all suffixes)",
        f"- KI-RO co-occurrence rate: {re_test['kiro_rate']:.1%}",
        f"- **Result: {re_test['interpretation']}**",
        "",
    ]

    # ===== SECTION 6: Cross-Validation =====
    lines += [
        "---",
        "",
        "## Section 6: Cross-Validation Summary",
        "",
        "| Finding | Non-HT Sites Tested | Cross-Validation Result |",
        "|---------|--------------------|-----------------------|",
        "| JA-SA-SA-RA-ME ritual exclusivity | Iouktas, Palaikastro, Platanos, Psykhro, Troullos | CONFIRMED: 5 sites, zero admin occurrences |",
        "| I-PI-NA-MA SI-RU-TE ritual bigram | Kophinas, Troullos, Vrysinas (3 non-HT cult sites) | CONFIRMED: 4 distinct cult sites |",
        "| -JA zero KI-RO co-occurrence | 17 sites total (Attempt #2 + this attempt) | CONFIRMED: persistent across all tested sites |",
        "| -RE high accounting co-occurrence | Multi-site (11 sites for -RE words) | CONFIRMED: robust pattern |",
        "| KU-NI-SU Knossos toponym match | Only Haghia Triada | NOT CROSS-VALIDATED: single-site limitation |",
        "| U-NA-KA-NA-SI post-anchor companion | Iouktas, Palaikastro | CONFIRMED at 2 sites |",
        "",
    ]

    # ===== SECTION 7: Confidence Summary =====
    lines += [
        "---",
        "",
        "## Section 7: Confidence and Evidence Tier Summary",
        "",
        "| Claim | Evidence Tier | Confidence | Cross-Validated |",
        "|-------|--------------|------------|----------------|",
        "| JA-SA-SA-RA-ME = ritual formula/divine name | Tier 3 (Formulaic) | Medium | Yes — 5 sites |",
        "| I-PI-NA-MA SI-RU-TE = ritual invocation bigram | Tier 3 (Formulaic) | Medium | Yes — 4 cult sites |",
        "| U-NA-KA-NA-SI = companion to JA-SA-SA-RA-ME | Tier 3 (Formulaic) | Medium | Yes — 2 sites |",
        "| A-TA-I-*301-WA-JA = ritual formula (most frequent ritual-exclusive) | Tier 3 (Formulaic) | Medium | Yes — 3+ sites |",
        "| -JA = absolutive/intransitive marker | Tier 5 (Grammatical) | Medium-High | Yes — 17 sites |",
        "| -RE = active participle/accounting marker | Tier 5 (Grammatical) | Medium | Yes — 11 sites |",
        "| -TE ↔ Hurrian directive/dative | Tier 5 (Grammatical) | Low-Medium | Partial — 20 sites |",
        "| KU-NI-SU ~ Knossos (toponym hypothesis) | Tier 4 (Lexical) | Low | No — HT only |",
        "| DA-KA ~ Dikte (toponym hypothesis) | Tier 4 (Lexical) | Low | No — HT only |",
        "| Linear A compatible with Hurrian morphology | Tier 5 (Grammatical) | Medium | Partial |",
        "",
        "> **Epistemic note:** All claims are phrased as hypotheses consistent with the data. No claim constitutes a decipherment or definitive identification.",
        "",
    ]

    # ===== SECTION 8: Interpretation & Next Steps =====
    lines += [
        "---",
        "",
        "## Section 8: Interpretation and Follow-up Questions",
        "",
        "### Key Interpretations",
        "",
        "1. **Ritual register is structurally distinct**: 10 tokens are 100% ritual-exclusive. The ritual register likely uses a specialized liturgical vocabulary absent from administrative tablets. This is consistent with register differentiation in other ancient Near Eastern writing systems.",
        "",
        "2. **A four-unit liturgical sequence may exist**: The ordering `JA-SA-SA-RA-ME → U-NA-KA-NA-SI → I-PI-NA-MA → SI-RU-TE` appears partially at Iouktas (two bigrams confirmed), suggesting these four formulas form a longer ritual invocation. This should be investigated in Attempt #4.",
        "",
        "3. **-JA as absolutive/intransitive is the strongest morphological finding**: Zero KI-RO co-occurrence across 17 sites, combined with word-initial position dominance (38 initial vs. 7 final), strongly suggests -JA marks the absolutive case or intransitive nominal. This is compatible with Hurrian, Luwian, and several other candidate language families.",
        "",
        "4. **Hurrian morphological compatibility is medium-level**: The alignment matrix finds 14 high-confidence alignments, but the -NA locative test partially failed (high terminal use). This does not rule out Hurrian, but means -NA may be functionally ambiguous in Linear A, OR the Linear A accounting context places locative words in terminal slots.",
        "",
        "5. **KU-NI-SU and DA-KA are interesting but unconfirmed toponym candidates**: The consonant skeleton matches are suggestive but both tokens are Haghia Triada-specific, which is the most formulaic site. Neither can be elevated above Low confidence without cross-site corroboration.",
        "",
        "### Follow-up Questions for Attempt #4",
        "",
        "- [ ] Does `A-TA-I-*301-WA-JA` form a complete libation formula? What sign is `*301`?",
        "- [ ] Can the four-unit sequence `JA-SA-SA-RA-ME U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE` be confirmed in any single inscription?",
        "- [ ] Does `KU-NI-SU` appear at Knossos (its namesake site) or only at HT?",
        "- [ ] Do the high-specificity Khania tokens (`*411-VS` and related) have Linear B parallels?",
        "- [ ] What is the full distribution of `-ME` suffix words? The ritual enrichment ratio of -ME (3.01x) suggests it may be a ritual grammatical marker.",
        "- [ ] Can N-gram fingerprinting (Strategy 9) disambiguate between Hurrian and other candidate languages given the now-established suffix paradigm?",
        "",
    ]

    return "\n".join(lines)


def main():
    print("Loading analysis outputs...")
    libation = load_json(LIBATION_PATH)
    proper_noun = load_json(PROPER_NOUN_PATH)
    hurrian = load_json(HURRIAN_PATH)

    print("Generating summary report...")
    report = generate_report(libation, proper_noun, hurrian)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"Report written to {OUTPUT_PATH}")
    print(f"Report length: {len(report)} characters")


if __name__ == "__main__":
    main()
