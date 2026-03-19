#!/usr/bin/env python3
"""
Sign Clustering Analysis — Strategy 7
Linear A Decipherment Project — 2026-03-19

Purpose: Build a sign co-occurrence matrix from the full corpus, apply PCA and k-means
clustering to place signs in distributional space, and identify which phonological
neighborhoods unknown signs (*-prefixed) fall into.

Evidence tier: Tier 1 (Structural/Distributional) — NO phonetic values claimed as proven.
"""

import json
import math
import re
from collections import defaultdict, Counter

# ─── Constants ────────────────────────────────────────────────────────────────

CORPUS_PATH = "corpus/linear_a_llm_master.jsonl"
OUTPUT_PATH = "analysis/outputs/sign_clustering_2026-03-19.json"

# Known logograms to exclude from syllabic clustering
LOGOGRAMS = {
    "GRA", "VIN", "OLE", "OLIV", "VIR", "MUL", "CYP", "FIG", "OVI", "BOS",
    "EQU", "SUS", "CAP", "TELA", "LANA", "AES", "GRA+KU", "GRA+E",
    "GRA+PA", "GRA+SI", "GRA+TE", "OLIV+E",
}

# Punctuation / structural tokens to exclude
EXCLUDE_TOKENS = {"𐄁", "↵", "\n", "", " "}

# Numeral pattern (pure digits or fraction notations)
NUMERAL_RE = re.compile(r'^[\d/.,½⅓¼⅕]+$')

# Known syllabic phonetic values (for cluster labeling)
KNOWN_PHONETICS = {
    "A", "E", "I", "O", "U",
    "DA", "DE", "DI", "DO", "DU",
    "JA", "JE", "JO", "JU",
    "KA", "KE", "KI", "KO", "KU",
    "MA", "ME", "MI", "MO", "MU",
    "NA", "NE", "NI", "NO", "NU",
    "PA", "PE", "PI", "PO", "PU",
    "QA", "QE", "QI", "QO",
    "RA", "RA2", "RE", "RI", "RO", "RU",
    "SA", "SE", "SI", "SO", "SU",
    "TA", "TA2", "TE", "TI", "TO", "TU",
    "WA", "WE", "WI", "WO",
    "ZA", "ZE", "ZO",
    "NWA", "DWE", "DWI",
    "TWE", "TWO",
    "PHA", "PHE",
}

# Signs whose phonetic class is known for labeling clusters
PHONETIC_CLASSES = {
    # Stops
    "KA": "stop", "KE": "stop", "KI": "stop", "KO": "stop", "KU": "stop",
    "PA": "stop", "PE": "stop", "PI": "stop", "PO": "stop", "PU": "stop",
    "TA": "stop", "TE": "stop", "TI": "stop", "TO": "stop", "TU": "stop",
    "DA": "stop", "DE": "stop", "DI": "stop", "DO": "stop", "DU": "stop",
    "QA": "stop", "QE": "stop", "QI": "stop", "QO": "stop",
    # Nasals
    "NA": "nasal", "NE": "nasal", "NI": "nasal", "NO": "nasal", "NU": "nasal",
    "MA": "nasal", "ME": "nasal", "MI": "nasal", "MO": "nasal", "MU": "nasal",
    # Sibilants
    "SA": "sibilant", "SE": "sibilant", "SI": "sibilant", "SO": "sibilant", "SU": "sibilant",
    "ZA": "sibilant", "ZE": "sibilant", "ZO": "sibilant",
    # Liquids
    "RA": "liquid", "RA2": "liquid", "RE": "liquid", "RI": "liquid", "RO": "liquid", "RU": "liquid",
    # Glides / semivowels
    "JA": "glide", "JE": "glide", "JO": "glide", "JU": "glide",
    "WA": "glide", "WE": "glide", "WI": "glide", "WO": "glide",
    # Pure vowels
    "A": "vowel", "E": "vowel", "I": "vowel", "O": "vowel", "U": "vowel",
}


# ─── Data Loading ─────────────────────────────────────────────────────────────

def load_corpus(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def is_syllabic(token):
    """Return True if token is a syllabic sign (not logogram, numeral, or punctuation)."""
    if not token:
        return False
    if not isinstance(token, str):
        return False
    if token in EXCLUDE_TOKENS:
        return False
    if token in LOGOGRAMS:
        return False
    if NUMERAL_RE.match(token):
        return False
    # Exclude pure punctuation
    if all(c in "𐄁↵ \t" for c in token):
        return False
    return True


def get_token_values(rec):
    """Extract string values from token dicts."""
    raw = rec.get("transliteration_tokens", [])
    return [t.get("value", "") if isinstance(t, dict) else str(t) for t in raw]


def extract_sign_sequences(records):
    """Extract all syllabic-sign sequences from corpus."""
    sequences = []
    for rec in records:
        tokens = get_token_values(rec)
        if not tokens:
            continue
        # Filter to syllabic signs only
        syllabic = [t for t in tokens if is_syllabic(t)]
        if syllabic:
            sequences.append(syllabic)
    return sequences


# ─── Co-occurrence Matrix ──────────────────────────────────────────────────────

def build_cooccurrence(sequences, window=2):
    """Build sign co-occurrence counts within ±window positions."""
    cooccur = defaultdict(Counter)
    sign_freq = Counter()

    for seq in sequences:
        for i, sign in enumerate(seq):
            sign_freq[sign] += 1
            for j in range(max(0, i - window), min(len(seq), i + window + 1)):
                if j != i:
                    cooccur[sign][seq[j]] += 1

    return cooccur, sign_freq


def compute_pmi(cooccur, sign_freq, total_tokens):
    """Compute PMI-weighted co-occurrence matrix."""
    # Total co-occurrence events
    total_cooccur = sum(sum(v.values()) for v in cooccur.values())

    pmi_matrix = {}
    for sign_a, neighbors in cooccur.items():
        pmi_matrix[sign_a] = {}
        p_a = sign_freq[sign_a] / total_tokens
        for sign_b, count in neighbors.items():
            p_b = sign_freq[sign_b] / total_tokens
            p_ab = count / total_cooccur
            if p_a > 0 and p_b > 0 and p_ab > 0:
                pmi = math.log(p_ab / (p_a * p_b))
                pmi_matrix[sign_a][sign_b] = max(0, pmi)  # Positive PMI only
    return pmi_matrix


# ─── Simple PCA Implementation ────────────────────────────────────────────────

def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def dot(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def norm(v):
    return math.sqrt(dot(v, v))


def normalize(v):
    n = norm(v)
    if n == 0:
        return v
    return [x / n for x in v]


def subtract_mean(matrix_rows):
    """Subtract column means from matrix (centering)."""
    if not matrix_rows:
        return matrix_rows
    n_cols = len(matrix_rows[0])
    col_means = [mean([row[j] for row in matrix_rows]) for j in range(n_cols)]
    return [[row[j] - col_means[j] for j in range(n_cols)] for row in matrix_rows]


def power_iteration(matrix, n_iter=50):
    """Find approximate first principal component via power iteration."""
    import random
    n = len(matrix[0])
    v = [random.gauss(0, 1) for _ in range(n)]
    v = normalize(v)

    for _ in range(n_iter):
        # Av = matrix^T @ matrix @ v (covariance matrix times v)
        # Step 1: z = matrix @ v
        z = [dot(row, v) for row in matrix]
        # Step 2: v_new = matrix^T @ z
        v_new = [sum(matrix[i][j] * z[i] for i in range(len(matrix))) for j in range(n)]
        v = normalize(v_new)
    return v


def project_onto(matrix, component):
    """Project matrix rows onto a component vector."""
    return [dot(row, component) for row in matrix]


def simple_pca(matrix_rows, n_components=5):
    """Simple PCA returning first n_components principal components."""
    centered = subtract_mean(matrix_rows)
    components = []
    projections = []

    residual = [row[:] for row in centered]
    for _ in range(n_components):
        if not any(any(x != 0 for x in row) for row in residual):
            break
        pc = power_iteration(residual)
        proj = project_onto(residual, pc)
        components.append(pc)
        projections.append(proj)
        # Deflate: subtract projection
        residual = [
            [residual[i][j] - proj[i] * pc[j] for j in range(len(residual[i]))]
            for i in range(len(residual))
        ]

    # Return sign coordinates: each sign gets [proj[0][i], proj[1][i], ...]
    n_signs = len(matrix_rows)
    coords = [[projections[c][i] for c in range(len(projections))] for i in range(n_signs)]
    return coords


# ─── K-means Clustering ───────────────────────────────────────────────────────

def kmeans(points, k, n_iter=100):
    """Simple k-means clustering."""
    import random
    n = len(points)
    dim = len(points[0]) if points else 0

    # Initialize centroids by random selection
    centroids = [list(points[i]) for i in random.sample(range(n), min(k, n))]

    assignments = [0] * n
    for _ in range(n_iter):
        # Assign
        new_assignments = []
        for p in points:
            dists = [sum((p[d] - c[d]) ** 2 for d in range(min(dim, len(c)))) for c in centroids]
            new_assignments.append(dists.index(min(dists)))
        if new_assignments == assignments:
            break
        assignments = new_assignments

        # Update centroids
        for ki in range(k):
            cluster_points = [points[i] for i in range(n) if assignments[i] == ki]
            if cluster_points:
                centroids[ki] = [mean([p[d] for p in cluster_points]) for d in range(dim)]

    return assignments, centroids


# ─── Main Analysis ────────────────────────────────────────────────────────────

def analyze_clusters(signs, assignments, k, sign_freq):
    """Analyze each cluster: what known signs are in it, what unknown signs are in it."""
    clusters = defaultdict(list)
    for i, sign in enumerate(signs):
        clusters[assignments[i]].append(sign)

    cluster_analysis = {}
    for cluster_id in range(k):
        members = clusters.get(cluster_id, [])
        known = [(s, PHONETIC_CLASSES.get(s, "?"), sign_freq.get(s, 0))
                 for s in members if not s.startswith("*")]
        unknown = [(s, sign_freq.get(s, 0)) for s in members if s.startswith("*")]

        # Determine dominant phonetic class
        class_counts = Counter(PHONETIC_CLASSES.get(s) for s in members
                               if not s.startswith("*") and PHONETIC_CLASSES.get(s))
        dominant_class = class_counts.most_common(1)[0][0] if class_counts else "mixed"
        dominant_count = class_counts.most_common(1)[0][1] if class_counts else 0
        known_total = sum(class_counts.values())
        purity = dominant_count / known_total if known_total > 0 else 0.0

        cluster_analysis[cluster_id] = {
            "cluster_id": cluster_id,
            "size": len(members),
            "dominant_phonetic_class": dominant_class,
            "class_purity": round(purity, 3),
            "class_distribution": {k: v for k, v in class_counts.items()},
            "known_signs": sorted(known, key=lambda x: -x[2]),
            "unknown_signs": sorted(unknown, key=lambda x: -x[1]),
        }

    return cluster_analysis


def find_star301_neighbors(pmi_matrix, sign_freq, top_n=10):
    """Find the top co-occurrence neighbors of *301."""
    star301_neighbors = []
    if "*301" in pmi_matrix:
        neighbors = pmi_matrix["*301"]
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: -x[1])[:top_n]
        for neighbor, pmi_score in sorted_neighbors:
            phonetic_class = PHONETIC_CLASSES.get(neighbor, "unknown")
            star301_neighbors.append({
                "sign": neighbor,
                "pmi": round(pmi_score, 4),
                "frequency": sign_freq.get(neighbor, 0),
                "phonetic_class": phonetic_class,
            })
    return star301_neighbors


def run():
    print("Loading corpus...")
    records = load_corpus(CORPUS_PATH)
    print(f"  Loaded {len(records)} records")

    print("Extracting sign sequences...")
    sequences = extract_sign_sequences(records)
    total_tokens = sum(len(s) for s in sequences)
    print(f"  {len(sequences)} sequences, {total_tokens} total syllabic tokens")

    print("Building co-occurrence matrix...")
    cooccur, sign_freq = build_cooccurrence(sequences, window=2)
    print(f"  {len(sign_freq)} distinct signs in corpus")

    # Filter: only signs appearing ≥5 times for clustering (avoid noise)
    MIN_FREQ = 5
    active_signs = sorted([s for s, c in sign_freq.items() if c >= MIN_FREQ])
    print(f"  {len(active_signs)} signs with freq ≥ {MIN_FREQ} for clustering")

    print("Computing PMI...")
    pmi_matrix = compute_pmi(cooccur, sign_freq, total_tokens)

    # Build feature vectors: for each sign, its PMI with every other active sign
    sign_to_idx = {s: i for i, s in enumerate(active_signs)}
    vectors = []
    for sign in active_signs:
        vec = []
        for other in active_signs:
            if sign == other:
                vec.append(0.0)
            else:
                vec.append(pmi_matrix.get(sign, {}).get(other, 0.0))
        vectors.append(vec)

    print("Running PCA (5 components)...")
    try:
        coords = simple_pca(vectors, n_components=5)
    except Exception as e:
        print(f"  PCA failed: {e}, using raw PMI top-5 neighbors as features")
        # Fallback: use top-5 PMI neighbor sign indices as feature dimensions
        coords = []
        for sign in active_signs:
            neighbors = sorted(pmi_matrix.get(sign, {}).items(), key=lambda x: -x[1])[:5]
            coord = [pmi for _, pmi in neighbors] + [0.0] * (5 - len(neighbors))
            coords.append(coord)

    print("Running k-means (k=10)...")
    K = 10
    assignments, centroids = kmeans(coords, k=K)

    print("Analyzing clusters...")
    cluster_analysis = analyze_clusters(active_signs, assignments, K, sign_freq)

    # Unknown signs summary
    unknown_signs_summary = []
    star_signs = [s for s in active_signs if s.startswith("*")]
    for sign in star_signs:
        idx = sign_to_idx[sign]
        cluster_id = assignments[idx]
        cluster_info = cluster_analysis[cluster_id]
        top_neighbors = sorted(pmi_matrix.get(sign, {}).items(), key=lambda x: -x[1])[:5]
        neighbor_classes = [PHONETIC_CLASSES.get(n, "?") for n, _ in top_neighbors]

        unknown_signs_summary.append({
            "sign": sign,
            "frequency": sign_freq[sign],
            "cluster_id": cluster_id,
            "cluster_dominant_class": cluster_info["dominant_phonetic_class"],
            "cluster_class_purity": cluster_info["class_purity"],
            "top_pmi_neighbors": [
                {"sign": n, "pmi": round(pmi, 4),
                 "phonetic_class": PHONETIC_CLASSES.get(n, "?")}
                for n, pmi in top_neighbors
            ],
            "inferred_phonetic_class": cluster_info["dominant_phonetic_class"],
            "confidence": "Low" if cluster_info["class_purity"] < 0.5 else
                          "Low-Medium" if cluster_info["class_purity"] < 0.65 else
                          "Medium",
            "note": "Tier 1 evidence only — phonetic value not claimed as proven",
        })

    # Special analysis for *301
    star301_neighbors = find_star301_neighbors(pmi_matrix, sign_freq)

    # Sign frequency overview
    sign_freq_table = [
        {"sign": s, "frequency": c,
         "is_unknown": s.startswith("*"),
         "known_phonetic_class": PHONETIC_CLASSES.get(s, None)}
        for s, c in sign_freq.most_common(100)
    ]

    result = {
        "metadata": {
            "date": "2026-03-19",
            "strategy": "Strategy 7 — Computational Sign Clustering",
            "corpus_records": len(records),
            "sequences_analyzed": len(sequences),
            "total_syllabic_tokens": total_tokens,
            "distinct_signs": len(sign_freq),
            "signs_clustered": len(active_signs),
            "min_frequency_threshold": MIN_FREQ,
            "n_clusters": K,
            "evidence_tier": "Tier 1 (Structural/Distributional)",
            "note": "No phonetic values claimed as proven; cluster membership is distributional inference only",
        },
        "unknown_signs_analysis": sorted(unknown_signs_summary, key=lambda x: -x["frequency"]),
        "star301_special_analysis": {
            "frequency": sign_freq.get("*301", 0),
            "top_pmi_neighbors": star301_neighbors,
            "note": (
                "*301 appears both as an HT administrative classifier (230/238 occ) "
                "and embedded in ritual formula A-TA-I-*301-WA-JA. "
                "The PMI neighbors reflect combined usage; context-split analysis needed."
            ),
        },
        "cluster_details": {
            str(cid): info for cid, info in cluster_analysis.items()
        },
        "sign_frequency_top100": sign_freq_table,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nResults written to {OUTPUT_PATH}")

    # Print summary
    print("\n=== SIGN CLUSTERING SUMMARY ===")
    print(f"\nUnknown signs with freq ≥ {MIN_FREQ}:")
    for item in sorted(unknown_signs_summary, key=lambda x: -x["frequency"]):
        sign = item["sign"]
        freq = item["frequency"]
        cluster = item["cluster_id"]
        dom_class = item["cluster_dominant_class"]
        purity = item["cluster_class_purity"]
        print(f"  {sign:12s} freq={freq:4d}  cluster={cluster}  "
              f"dominant_class={dom_class}  purity={purity:.2f}  "
              f"confidence={item['confidence']}")

    print("\n*301 top PMI neighbors:")
    for n in star301_neighbors[:5]:
        print(f"  {n['sign']:10s} pmi={n['pmi']:.4f}  class={n['phonetic_class']}  freq={n['frequency']}")

    print("\nCluster overview:")
    for cid, info in sorted(cluster_analysis.items()):
        known_names = [s for s, cls, freq in info["known_signs"][:5]]
        unk_names = [s for s, freq in info["unknown_signs"][:3]]
        print(f"  Cluster {cid}: dominant={info['dominant_phonetic_class']:10s} "
              f"purity={info['class_purity']:.2f}  "
              f"known_sample={known_names[:3]}  "
              f"unknowns={unk_names}")

    return result


if __name__ == "__main__":
    run()
