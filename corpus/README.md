# Linear A LLM Package

A cleaned package of **1721 Linear A inscription records** formatted for LLM ingestion, fine-tuning experiments, and retrieval pipelines.

## Important warning

Linear A is **undeciphered**. The transliterations in this package are **conventional sign readings**, not a true decipherment. Treat glosses as source annotations only.

## Files

- `linear_a_llm_master.jsonl`  
  Best all-purpose source. One normalized JSON object per inscription.

- `linear_a_llm_flat.csv`  
  Flat spreadsheet-style export.

- `linear_a_instruction_pairs.jsonl`  
  Chat-format examples for instruction tuning or evaluation.

- `linear_a_rag_chunks.jsonl`  
  Chunked text blocks for retrieval systems.

- `linear_a_llm_reading_edition.md`  
  Human-readable site-grouped corpus.

## Recommended uses

### 1. For RAG / vector DB
Use `linear_a_rag_chunks.jsonl`.

### 2. For general corpus analysis
Use `linear_a_llm_master.jsonl`.

### 3. For supervised fine-tuning experiments
Use `linear_a_instruction_pairs.jsonl`, but preserve the undeciphered warning in your system prompt.

## Core schema in `linear_a_llm_master.jsonl`

- `id`: inscription identifier
- `canonical_name`: canonical inscription name
- `alternate_names`: alternate identifiers
- `site`, `context`, `findspot`, `support`, `scribe`: metadata
- `linear_a_text`: normalized continuous transcription
- `linear_a_text_with_linebreaks`: layout-preserving transcription when available
- `tokenized_linear_a`: token stream with explicit line breaks
- `transliteration_tokens`: conventional transliteration token stream with explicit line breaks
- `translation_or_gloss_tokens`: source gloss/annotation token stream with explicit line breaks
- `image_paths`, `facsimile_image_paths`: relative paths from the source explorer dataset
- `image_rights`, `image_rights_url`: source rights metadata
- `source_dataset`: provenance note
- `undeciphered_language_notice`: safety/caution field
- `stats`: light per-record counts

## Corpus summary

- Total records: 1721
- Distinct sites: 52
- Most common site: Haghia Triada (1110 records)
- Supports: Nodule=886, Tablet=393, Roundel=151, Stone vessel=107, Clay vessel=74, Metal object=23, Stone object=19, Lames (short thin tablet)=18, Sealing=12, Inked inscription=9, Architecture=6, 3-sided bar=5, 4-sided bar=5, Graffito=3, Label=3, ivory object=3, clay vessel=2, Loom weight=1, Triton=1

## Suggested system prompt for LLM use

> You are working with an undeciphered Aegean writing system. Use only the provided metadata and conventional transliterations. Do not claim that Linear A has been deciphered, and do not invent translations.
