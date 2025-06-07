import networkx as nx
from itertools import combinations

def generate_risk_hypotheses(G: nx.DiGraph, selected_drugs: list, min_overlap: int = 2):
    """
    Generate risk hypotheses based on overlapping side effects between selected drugs.

    Args:
        G (nx.DiGraph): The drug-side effect graph.
        selected_drugs (list): List of drugs to analyze.
        min_overlap (int): Minimum number of shared side effects to consider.

    Returns:
        list: A list of hypotheses with drug pairs, overlap counts, and shared side effects.
    """
    hypotheses = []
    for d1, d2 in combinations(selected_drugs, 2):
        se1 = {v for u, v in G.edges(d1)} if d1 in G else set()
        se2 = {v for u, v in G.edges(d2)} if d2 in G else set()
        overlap = se1 & se2

        if len(overlap) >= min_overlap:
            freq_scores = []
            for se in overlap:
                f1 = G.edges[d1, se].get("frequency", 0) if G.has_edge(d1, se) else 0
                f2 = G.edges[d2, se].get("frequency", 0) if G.has_edge(d2, se) else 0
                avg_freq = round((f1 + f2) / 2, 4)
                freq_scores.append((se, avg_freq))

            freq_scores.sort(key=lambda x: x[1], reverse=True)
            top_effects = ", ".join([f"{se} (score: {score})" for se, score in freq_scores[:5]])

            hypotheses.append({
                "drug_pair": (d1, d2),
                "overlap_count": len(overlap),
                "top_shared_effects": top_effects,
                "hypothesis": f"Combination of '{d1}' and '{d2}' may significantly increase the risk of: {top_effects}."
            })

    hypotheses.sort(key=lambda x: x["overlap_count"], reverse=True)
    return hypotheses
