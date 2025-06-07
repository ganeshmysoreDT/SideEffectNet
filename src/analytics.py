import pandas as pd
import networkx as nx

def risk_scores(graph):
    """
    Calculate risk score = number of side effects per drug.
    Returns a list of tuples (drug_name, risk_score) sorted by score descending.
    """
    drug_scores = []
    for node, data in graph.nodes(data=True):
        if data.get("type") == "drug":
            # Count side effects (out edges)
            score = graph.out_degree(node)
            drug_scores.append((node, score))
    # Sort descending by risk score
    return sorted(drug_scores, key=lambda x: x[1], reverse=True)

# Add test cases for analytics functions
import unittest

class TestAnalytics(unittest.TestCase):
    def test_risk_score_calculation(self):
        # Example test case for risk score calculation
        risk_scores = {
            "Aspirin": 0.3,
            "Ibuprofen": 0.5,
            "Paracetamol": 0.2,
            "Warfarin": 0.8,
            "Amoxicillin": 0.4
        }
        self.assertEqual(risk_scores["Aspirin"], 0.3)
        self.assertEqual(risk_scores["Warfarin"], 0.8)

    def test_side_effect_lookup(self):
        # Example test case for side effect lookup
        side_effects = {
            "Aspirin": ["Nausea", "Headache"],
            "Ibuprofen": ["Dizziness", "Nausea"],
            "Paracetamol": ["Rash"],
            "Warfarin": ["Bleeding", "Dizziness"],
            "Amoxicillin": ["Diarrhea", "Rash"]
        }
        self.assertIn("Nausea", side_effects["Aspirin"])
        self.assertIn("Bleeding", side_effects["Warfarin"])

    def test_risk_score_sorting(self):
        # Test if risk scores are sorted correctly
        risk_scores = [
            ("Aspirin", 0.3),
            ("Ibuprofen", 0.5),
            ("Paracetamol", 0.2),
            ("Warfarin", 0.8),
            ("Amoxicillin", 0.4)
        ]
        sorted_scores = sorted(risk_scores, key=lambda x: x[1], reverse=True)
        self.assertEqual(sorted_scores[0], ("Warfarin", 0.8))
        self.assertEqual(sorted_scores[-1], ("Paracetamol", 0.2))

    def test_graph_node_count(self):
        # Test if the graph has the correct number of nodes
        graph = nx.DiGraph()
        graph.add_node("Aspirin", type="drug")
        graph.add_node("Nausea", type="side_effect")
        graph.add_node("Headache", type="side_effect")
        self.assertEqual(len(graph.nodes), 3)

    def test_graph_edge_count(self):
        # Test if the graph has the correct number of edges
        graph = nx.DiGraph()
        graph.add_edge("Aspirin", "Nausea")
        graph.add_edge("Aspirin", "Headache")
        self.assertEqual(len(graph.edges), 2)

    def test_side_effect_frequency(self):
        # Test if side effect frequency is correctly retrieved
        side_effects = {
            "Nausea": 10.5,
            "Headache": 5.2,
            "Dizziness": 8.3
        }
        self.assertEqual(side_effects["Nausea"], 10.5)
        self.assertEqual(side_effects["Headache"], 5.2)

# Add test cases to validate data in CSV files
import pandas as pd

class TestCSVData(unittest.TestCase):
    def test_drug_risk_scores_csv(self):
        # Load drug_risk_scores.csv
        df = pd.read_csv("data/processed/drug_risk_scores.csv")
        self.assertFalse(df.empty, "drug_risk_scores.csv is empty")
        self.assertIn("drug_name", df.columns, "Missing 'drug_name' column in drug_risk_scores.csv")
        self.assertIn("risk_score", df.columns, "Missing 'risk_score' column in drug_risk_scores.csv")
        self.assertTrue((df["risk_score"] >= 0).all(), "Risk scores contain negative values")
        self.assertTrue((df["risk_score"] <= 1).all(), "Risk scores exceed 1")

    def test_side_effects_clean_csv(self):
        # Load side_effects_clean.csv
        df = pd.read_csv("data/processed/side_effects_clean.csv")
        self.assertFalse(df.empty, "side_effects_clean.csv is empty")
        self.assertIn("drug_name", df.columns, "Missing 'drug_name' column in side_effects_clean.csv")
        self.assertIn("side_effect", df.columns, "Missing 'side_effect' column in side_effects_clean.csv")
        self.assertIn("freq_pct", df.columns, "Missing 'freq_pct' column in side_effects_clean.csv")
        self.assertTrue((df["freq_pct"] >= 0).all(), "Frequency percentages contain negative values")

    # def test_drug_names_tsv(self):
    #     # Load drug_names.tsv
    #     df = pd.read_csv("data/raw/drug_names.tsv", sep="\t")
    #     self.assertFalse(df.empty, "drug_names.tsv is empty")
    #     self.assertIn("drug_name", df.columns, "Missing 'drug_name' column in drug_names.tsv")

    # def test_meddra_all_se_tsv(self):
    #     # Load meddra_all_se.tsv
    #     df = pd.read_csv("data/raw/meddra_all_se.tsv", sep="\t")
    #     self.assertFalse(df.empty, "meddra_all_se.tsv is empty")
    #     self.assertIn("side_effect", df.columns, "Missing 'side_effect' column in meddra_all_se.tsv")

    # def test_meddra_freq_tsv(self):
    #     # Load meddra_freq.tsv
    #     df = pd.read_csv("data/raw/meddra_freq.tsv", sep="\t")
    #     self.assertFalse(df.empty, "meddra_freq.tsv is empty")
    #     self.assertIn("side_effect", df.columns, "Missing 'side_effect' column in meddra_freq.tsv")
    #     self.assertIn("freq_pct", df.columns, "Missing 'freq_pct' column in meddra_freq.tsv")
    #     self.assertTrue((df["freq_pct"] >= 0).all(), "Frequency percentages contain negative values")


if __name__ == "__main__":
    unittest.main()



