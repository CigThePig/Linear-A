# Prior Scholarship on Linear A Decipherment

This file is a reference document summarizing the scholarly landscape. It is not a hypothesis file and does not get updated with new attempts — those go in `failed_attempts.md` and `hypotheses/`. Use this for background reading and citation.

---

## The Script

**Linear A** was used in Minoan Crete and some Aegean islands from approximately 1800–1450 BCE. It was the primary administrative and religious script of Minoan palatial civilization. Linear A is the ancestor (or close relative) of Linear B, the syllabic script used to write Mycenaean Greek, which was deciphered by Michael Ventris in 1952.

The script has approximately 50–60 core syllabic signs plus a set of logograms (commodity ideograms) and numerals. The sign inventory overlaps ~60–80% with Linear B. The underlying language is entirely unknown.

---

## Key Published Resources

### Corpora and Editions

- **GORILA** (Recueil des inscriptions en linéaire A, Vols. 1–5) — Godart & Olivier, 1976–1985. The foundational scholarly corpus. The dataset in `corpus/` derives from this and related modern digital editions.
- **LinearA Explorer** — Modern digital dataset extending GORILA with site metadata, scribe attributions, and standardized transliterations. Source of the `corpus/` data in this project.
- **Chapouthier (1930)** — Early publication of Haghia Triada tablets; first systematic description.

### Decipherment Attempts

**Cyrus Gordon (1966–1997)**
- Works: *Evidence for the Minoan Language* (1966), various articles through the 1990s
- Hypothesis: Linear A represents a Northwest Semitic language (related to Phoenician/Ugaritic)
- Method: Applied Semitic lexical comparisons to conventionally transliterated Linear A sequences
- Rejection: Inconsistent phonological correspondences; too many ad hoc choices; not reproducible under strict rules
- Scholarly assessment: Rejected by mainstream Aegean linguistics

**Giulio Facchetti**
- Works: *Frammenti di diritto privato etrusco* and related articles on Etruscan-Minoan parallels
- Hypothesis: Linear A may be related to Etruscan
- Method: Lexical comparison between Linear A sequences and Etruscan vocabulary
- Rejection: Both languages are isolates; resemblances are insufficient to establish relationship without a sound-law framework
- Scholarly assessment: Not widely accepted; Etruscan hypothesis remains unproven

**Hubert La Marle**
- Works: *Linéaire A: La première écriture syllabique de Crète* (multiple volumes, 1997–2002)
- Hypothesis: Semitic reading of Linear A with novel sign-value assignments
- Method: Assigned sign values independently of Linear B conventions, then found Semitic matches
- Rejection: Methodological problems — invented sign values to fit desired outcomes; not falsifiable; specialists found the method circular
- Scholarly assessment: Rejected

**Yves Duhoux**
- Works: Numerous statistical and structural analyses (1970s–2010s)
- Contribution: Established rigorous sign frequency tables and positional distributions for Linear A
- Outcome: Structural characterization without language identification
- Value to this project: His frequency tables are baseline data; the corpus in this project extends and supersedes his sample sizes

**Fred Woudhuizen**
- Works: *The Language of the Sea Peoples* (1992) and related articles
- Hypothesis: Linear A may be related to Luwian (Anatolian Indo-European)
- Method: Compared Linear A sequences (with conventional transliterations) to Luwian vocabulary
- Status: Not consensus, but not definitively rejected; remains one of the more serious candidates
- Scholarly assessment: Minority view with some serious proponents

**Jan Best and Fred Woudhuizen (eds.)**
- *Ancient Scripts from Crete and Cyprus* (1988)
- Assembled multiple decipherment proposals; useful for understanding range of approaches tried

**Brent Davis (2014)**
- Work: *A Contribution to the Study of Linear A Sign Groups* (PhD dissertation, University of Melbourne)
- Contribution: Most rigorous modern computational structural analysis of Linear A
- Findings: Linear A is consistent with agglutinative morphology with suffixing tendencies; SOV-compatible word order; demonstrates the language is structurally unlike Greek and unlike Semitic in its morphological profile
- Value to this project: His structural findings are treated as established ground truth here; the language is agglutinative. His work did not have access to the full 1721-inscription corpus with modern metadata.

**Silvia Ferrara**
- Works: *Mycenaean Texts and Contexts* and related publications; Linear A commentary
- Contribution: Archaeological contextualization of Linear A use; analysis of script spread and tablet function
- Value: Useful background on what Linear A tablets actually recorded and the palatial economy they served

---

## Key Scholarly Consensus Points

The following points represent areas of broad (though not always unanimous) agreement among Aegean linguists:

1. **Linear A is undeciphered.** No reading has achieved scholarly consensus.
2. **The conventional transliterations** (using Linear B sound values for shared signs) are working hypotheses, not proven readings.
3. **The numeral system** is well understood (decimal, positional, with fraction signs).
4. **The logograms** for major commodities (GRA, VIN, OLE, etc.) are identified with high confidence via Linear B parallels and archaeological context.
5. **KU-RO** = "total" and **KI-RO** = "owed/deficit" are the most widely accepted functional readings.
6. **The language is very likely agglutinative** (Davis 2014; Duhoux structural analysis).
7. **Linear A predates Greek presence on Crete** and is not an early form of Greek.
8. **The language family is genuinely unknown.** Proposed candidates include: Luwian/Anatolian, Proto-Semitic, Hurrian, Etruscan, and various isolate proposals. None has won consensus.

---

## Promising Directions Not Yet Exhausted

Based on the literature review, the following angles have not been tested at scale with the modern 1721-inscription corpus:

1. **Administrative formula bootstrapping at corpus scale** — Ventris's method applied to the full dataset with modern computational tools
2. **Suffix paradigm reconstruction** — systematic grouping and semantic clustering of suffix paradigms
3. **Proper noun isolation** via site-specificity scores, cross-referenced with Linear B Knossos personal names
4. **Hurrian morphological comparison** — the most structurally compatible candidate language never rigorously tested against the full corpus
5. **Libation table register separation** — religious vs. administrative register analyzed independently

---

## Bibliography (Selected)

- Davis, B. (2014). *A Contribution to the Study of Linear A Sign Groups*. PhD dissertation, University of Melbourne.
- Duhoux, Y. (1978). *Aspects du linéaire A*. Louvain.
- Ferrara, S. (2012). *Mycenaean Texts and Contexts*. Oxford.
- Godart, L., & Olivier, J.-P. (1976–1985). *Recueil des inscriptions en linéaire A* (GORILA), Vols. 1–5. Paris: École française d'Athènes.
- Gordon, C. (1966). *Evidence for the Minoan Language*. Ventnor: Ventnor Publishers.
- La Marle, H. (1997–2002). *Linéaire A: La première écriture syllabique de Crète*. Paris: Geuthner.
- Melchert, H.C. (1993). *Cuneiform Luvian Lexicon*. Chapel Hill.
- Ventris, M., & Chadwick, J. (1953). "Evidence for Greek Dialect in the Mycenaean Archives." *Journal of Hellenic Studies* 73: 84–103.
- Woudhuizen, F. (1992). *The Language of the Sea Peoples*. Amsterdam.
