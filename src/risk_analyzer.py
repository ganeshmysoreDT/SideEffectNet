import pandas as pd
import networkx as nx
from pyvis.network import Network

def calculate_and_add_risk_scores(graph):
    """
    Calculate average frequency (risk score) for each drug and assign as a node attribute.
    """
    drug_freqs = {}

    for src, dst, edge_data in graph.edges(data=True):
        freq = edge_data.get('frequency', None)
        if freq is not None and graph.nodes[src]['type'] == 'drug':
            if src not in drug_freqs:
                drug_freqs[src] = {'total_freq': 0, 'count': 0}
            drug_freqs[src]['total_freq'] += freq
            drug_freqs[src]['count'] += 1

    # Assign risk scores to drug nodes
    for drug, stats in drug_freqs.items():
        avg_freq = stats['total_freq'] / stats['count']
        graph.nodes[drug]['risk_score'] = round(avg_freq, 4)

    # Default risk score for drugs without frequency info
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'drug' and 'risk_score' not in data:
            graph.nodes[node]['risk_score'] = 0.0
    return graph

def export_risk_scores(graph, output_csv="drug_risk_scores.csv"):
    """
    Export drug names and risk scores to a CSV.
    """
    drug_data = []
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'drug':
            drug_data.append({
                'drug_name': data.get('label', node),
                'risk_score': data.get('risk_score', 0.0)
            })

    df = pd.DataFrame(drug_data)
    df = df.sort_values(by='risk_score', ascending=False)
    df.to_csv(output_csv, index=False)
    print(f"[✓] Drug risk scores saved to: {output_csv}")

def visualize_risk_scores(csv_path, output_html="risk_scores_graph.html"):
    df = pd.read_csv(csv_path)

    net = Network(height="750px", width="100%", bgcolor="#1e1e1e", font_color="white")

    for _, row in df.iterrows():
        drug = row['drug_name']
        score = row['risk_score']
        size = 20 + (score * 50)
        color = "#ff4c4c" if score > 0.5 else "#fca103"

        net.add_node(
            drug,
            label=f"{drug}\nScore: {score:.2f}",
            title=f"{drug}<br>Risk Score: {score:.2f}",
            value=score,
            size=size,
            color=color
        )

    net.show_buttons(filter_=['physics'])
    net.write_html(output_html, open_browser=False)
    print(f"Generated risk score graph: {output_html}")

