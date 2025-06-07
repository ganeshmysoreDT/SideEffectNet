import pandas as pd
import networkx as nx

def build_side_effect_graph(csv_path):
    df = pd.read_csv(csv_path)

    G = nx.DiGraph()  # Directed graph

    for _, row in df.iterrows():
        drug = row['drug_name']
        side_effect = row['side_effect']
        freq = row['freq_pct']

        # Add nodes
        # Drug nodes
        G.add_node(drug, label=drug, type="drug", color="#63b6e5")  # Blue

        # Side effect nodes
        G.add_node(side_effect, label=side_effect, type="side_effect", color="#f26c6c")  # Red

        # Optional: Add for genes later
        # graph.add_node(gene, label=gene, type="gene", color="#a6e22e")  # Green

        # Add edge with optional frequency
        if pd.notnull(freq):
            G.add_edge(drug, side_effect, relation='causes', frequency=float(freq))
        else:
            G.add_edge(drug, side_effect, relation='causes')

    return G
