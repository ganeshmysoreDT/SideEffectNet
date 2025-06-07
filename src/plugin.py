# Set up the framework for plugin development
class PluginBase:
    """
    Base class for all plugins in the Eliza AI framework.
    """
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def execute(self, *args, **kwargs):
        """
        Method to be implemented by all plugins.
        """
        raise NotImplementedError("Plugins must implement the execute method.")

    def get_metadata(self):
        """
        Returns metadata about the plugin.
        """
        return {
            "name": self.name,
            "version": self.version
        }

# Example plugin implementation
class ExamplePlugin(PluginBase):
    def __init__(self):
        super().__init__(name="ExamplePlugin", version="1.0")

    def execute(self, data):
        """
        Example execution logic.
        """
        return f"Processed data: {data}"

# Create a plugin for drug risk analysis
class DrugRiskAnalysisPlugin(PluginBase):
    """
    Plugin for analyzing drug risk scores and side effects.
    """
    def __init__(self):
        super().__init__(name="DrugRiskAnalysisPlugin", version="1.0")

    def execute(self, drug_name, risk_map, side_effect_lookup):
        """
        Analyze the risk score and side effects for a given drug.
        """
        if drug_name not in risk_map:
            return {
                "error": "Drug not found in risk map."
            }

        risk_score = risk_map[drug_name]
        side_effects = side_effect_lookup.get(drug_name, [])

        return {
            "drug_name": drug_name,
            "risk_score": risk_score,
            "side_effects": side_effects
        }

# Update the ElizaDashboardPlugin to use cleaned data from the workspace
import pandas as pd
import os
import json
import tempfile

class ElizaDashboardPlugin(PluginBase):
    """
    Plugin for integrating Eliza AI functionalities into the dashboard.
    """
    def __init__(self):
        super().__init__(name="ElizaDashboardPlugin", version="2.0")

        # Load cleaned data with error handling
        try:
            print("Attempting to load risk map...")
            file_path = os.path.join(os.path.dirname(__file__), "../data/processed/drug_risk_scores.csv")
            print(f"Checking if file exists: {os.path.exists(file_path)}")
            self.risk_map = pd.read_csv(file_path).set_index("drug_name")["risk_score"].to_dict()
            print("Risk map loaded successfully.")
        except FileNotFoundError:
            self.risk_map = {}
            print("Error: drug_risk_scores.csv file not found.")
        except Exception as e:
            self.risk_map = {}
            print(f"Error loading risk map: {e}")

        try:
            print("Attempting to load side effect lookup...")
            file_path = os.path.join(os.path.dirname(__file__), "../data/processed/side_effects_clean.csv")
            print(f"Checking if file exists: {os.path.exists(file_path)}")
            self.side_effect_lookup = {
                drug: list(group["side_effect"])
                for drug, group in pd.read_csv(file_path).groupby("drug_name")
            }
            print("Side effect lookup loaded successfully.")
        except FileNotFoundError:
            self.side_effect_lookup = {}
            print("Error: side_effects_clean.csv file not found.")
        except Exception as e:
            self.side_effect_lookup = {}
            print(f"Error loading side effect lookup: {e}")

    def execute(self, action, *args, **kwargs):
        """
        Execute specific actions related to the dashboard.
        """
        if action == "analyze_risk":
            return self.analyze_risk(*args, **kwargs)
        elif action == "generate_graph":
            return self.generate_graph(*args, **kwargs)
        elif action == "validate_data":
            return self.validate_data(*args, **kwargs)
        elif action == "generate_hypotheses":
            return self.generate_hypotheses(*args, **kwargs)
        elif action == "generate_pdf":
            return self.generate_pdf(*args, **kwargs)
        else:
            return {"error": "Unknown action."}

    # Ensure case-insensitive drug name matching in analyze_risk
    def analyze_risk(self, drug_name):
        """
        Analyze the risk score and side effects for a given drug.
        """
        if not self.risk_map:
            return {"error": "Risk map is empty or failed to load."}

        # Normalize drug name to lowercase for case-insensitive matching
        normalized_drug_name = drug_name.lower()
        normalized_risk_map = {key.lower(): value for key, value in self.risk_map.items()}
        normalized_side_effect_lookup = {key.lower(): value for key, value in self.side_effect_lookup.items()}

        if normalized_drug_name not in normalized_risk_map:
            return {"error": f"Drug '{drug_name}' not found in risk map."}

        risk_score = normalized_risk_map[normalized_drug_name]
        side_effects = normalized_side_effect_lookup.get(normalized_drug_name, [])

        if risk_score == 0.0:
            return {
                "drug_name": drug_name,
                "risk_score": risk_score,
                "side_effects": side_effects,
                "warning": "This drug has a risk score of 0.0, indicating minimal or no risk."
            }

        return {
            "drug_name": drug_name,
            "risk_score": risk_score,
            "side_effects": side_effects
        }

    def generate_graph(self, graph_data):
        """
        Generate a graph visualization using PyVis.
        """
        from pyvis.network import Network
        import tempfile

        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")

        for node, attrs in graph_data.get("nodes", {}).items():
            net.add_node(node, **attrs)

        for edge in graph_data.get("edges", []):
            net.add_edge(edge[0], edge[1], **edge[2])

        # Save the graph to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
            net.save_graph(tmpfile.name)
            return f"Graph visualization saved as {tmpfile.name}"

    def validate_data(self, file_path):
        """
        Validate the integrity of a data file.
        """
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                return {"error": "File is empty."}
            return {"status": "File is valid.", "columns": list(df.columns)}
        except Exception as e:
            return {"error": str(e)}

    def generate_hypotheses(self, drug_a, drug_b):
        """
        Generate scientific hypotheses for drug combinations.
        """
        risk_a = self.risk_map.get(drug_a, 0)
        risk_b = self.risk_map.get(drug_b, 0)
        side_effects_a = set(self.side_effect_lookup.get(drug_a, []))
        side_effects_b = set(self.side_effect_lookup.get(drug_b, []))
        overlapping = side_effects_a & side_effects_b

        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "risk_a": risk_a,
            "risk_b": risk_b,
            "shared_side_effects": list(overlapping)
        }

    # Update the generate_pdf method to include detailed risk scores and shared side effects
    def generate_pdf(self, drug_a, drug_b, hypotheses):
        """
        Generate a PDF report for drug risk analysis.
        """
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Title
        c.drawString(100, 750, f"Risk Analysis Report: {drug_a} and {drug_b}")

        # Risk Scores
        c.drawString(100, 730, f"Risk Score for {drug_a}: {self.risk_map.get(drug_a, 'N/A')}")
        c.drawString(100, 710, f"Risk Score for {drug_b}: {self.risk_map.get(drug_b, 'N/A')}")

        # Shared Side Effects
        c.drawString(100, 690, "Shared Side Effects:")
        y = 670
        for side_effect in hypotheses.get("shared_side_effects", []):
            c.drawString(100, y, f"- {side_effect}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        c.save()
        buffer.seek(0)
        return buffer

def generate_graph_for_drug(drug_name, side_effect_lookup):
        """
        Generate graph visualization for a given drug and save it as an HTML file.
        """
        if drug_name not in side_effect_lookup:
            return {"error": f"Drug '{drug_name}' not found in side effect lookup."}

        side_effects = side_effect_lookup[drug_name]

        # Construct graph data
        from pyvis.network import Network
        net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")

        net.add_node(drug_name, color="#636EFA", size=30, title=f"Drug: {drug_name}")

        for side_effect in side_effects:
            net.add_node(side_effect, color="#EF553B", size=20, title=f"Side Effect: {side_effect}")
            net.add_edge(drug_name, side_effect, color="#A3A3A3", width=2)

        # Save graph visualization to an HTML file in the Downloads directory
        import os
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        html_file_path = os.path.join(downloads_dir, f"{drug_name}_graph.html")
        net.save_graph(html_file_path)

        return html_file_path


# Add additional plugins for the Eliza AI framework

class DrugInteractionPlugin(PluginBase):
    """
    Plugin for analyzing drug interactions.
    """
    def __init__(self):
        super().__init__(name="DrugInteractionPlugin", version="1.0")

    def execute(self, drug_a, drug_b, side_effect_lookup):
        """
        Analyze interactions between two drugs based on shared side effects.
        """
        side_effects_a = set(side_effect_lookup.get(drug_a, []))
        side_effects_b = set(side_effect_lookup.get(drug_b, []))
        shared_side_effects = side_effects_a & side_effects_b

        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "shared_side_effects": list(shared_side_effects)
        }

class RiskVisualizationPlugin(PluginBase):
    """
    Plugin for visualizing risk scores.
    """
    def __init__(self):
        super().__init__(name="RiskVisualizationPlugin", version="1.0")

    def execute(self, risk_map):
        """
        Generate a bar chart visualization of risk scores.
        """
        import matplotlib.pyplot as plt

        drugs = list(risk_map.keys())
        scores = list(risk_map.values())

        plt.figure(figsize=(10, 6))
        plt.bar(drugs, scores, color="skyblue")
        plt.xlabel("Drugs")
        plt.ylabel("Risk Scores")
        plt.title("Drug Risk Scores")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig("risk_scores_graph.png")
        return "Risk scores graph saved as risk_scores_graph.png"

# Convert the plugin system into a CLI interface
import argparse

class ElizaCLI:
    """
    Command Line Interface for interacting with Eliza plugins.
    """
    def __init__(self):
        self.plugin = ElizaDashboardPlugin()

    def run(self):
        parser = argparse.ArgumentParser(description="Eliza AI Plugin CLI")
        parser.add_argument("action", type=str, help="Action to perform (analyze_risk, generate_hypotheses, generate_pdf, validate_data, generate_graph)")
        parser.add_argument("--drug_name", type=str, help="Drug name for risk analysis")
        parser.add_argument("--drug_a", type=str, help="First drug name for hypothesis generation")
        parser.add_argument("--drug_b", type=str, help="Second drug name for hypothesis generation")
        parser.add_argument("--file_path", type=str, help="Path to the data file for validation")
        parser.add_argument("--graph_data", type=str, help="Path to graph data JSON file")

        args = parser.parse_args()

        if args.action == "analyze_risk":
            if not args.drug_name:
                print("Error: --drug_name is required for analyze_risk.")
                return
            result = self.plugin.execute("analyze_risk", args.drug_name)
            print(result)

        elif args.action == "generate_hypotheses":
            if not args.drug_a or not args.drug_b:
                print("Error: --drug_a and --drug_b are required for generate_hypotheses.")
                return
            result = self.plugin.execute("generate_hypotheses", args.drug_a, args.drug_b)
            print(result)

        elif args.action == "generate_pdf":
            if not args.drug_a or not args.drug_b:
                print("Error: --drug_a and --drug_b are required for generate_pdf.")
                return
            pdf_buffer = self.plugin.execute("generate_pdf", args.drug_a, args.drug_b, "Generated hypotheses text")
            with open("risk_analysis_report.pdf", "wb") as f:
                f.write(pdf_buffer.read())
            print("PDF report saved as risk_analysis_report.pdf")

        elif args.action == "validate_data":
            if not args.file_path:
                print("Error: --file_path is required for validate_data.")
                return
            result = self.plugin.execute("validate_data", args.file_path)
            print(result)

        elif args.action == "generate_graph":
            if not args.graph_data:
                print("Error: --graph_data is required for generate_graph.")
                return
            import json
            with open(args.graph_data, "r") as f:
                graph_data = json.load(f)
            result = self.plugin.execute("generate_graph", graph_data)
            print(result)

        else:
            print("Error: Unknown action.")

from colorama import Fore, Style

# Add prompt to enter drug names for hypothesis generation
if __name__ == "__main__":
    print(Fore.CYAN + "Welcome to the Eliza AI Framework!" + Style.RESET_ALL)
    print(Fore.YELLOW + "This project provides intelligent scientific assistance for drug risk analysis and visualization." + Style.RESET_ALL)
    print(Fore.GREEN + "Plugins available:" + Style.RESET_ALL)
    print(Fore.MAGENTA + "- DrugRiskAnalysisPlugin: Analyze drug risk scores and side effects." + Style.RESET_ALL)
    print(Fore.MAGENTA + "- DrugInteractionPlugin: Analyze interactions between drugs based on shared side effects." + Style.RESET_ALL)
    print(Fore.MAGENTA + "- RiskVisualizationPlugin: Visualize risk scores using bar charts." + Style.RESET_ALL)
    print(Fore.BLUE + "Visit our website for more information: https://github.com/your-repo" + Style.RESET_ALL)

    cli = ElizaCLI()

    # Prompt user for action
    action = input(Fore.CYAN + "Enter action (analyze_risk, generate_hypotheses, generate_pdf, validate_data, generate_graph): " + Style.RESET_ALL).strip().lower()

    if action in ["analyze_risk", "analyze risk"]:
        print(Fore.YELLOW + "Analyze Risk: This action allows you to analyze the risk score and side effects for a specific drug." + Style.RESET_ALL)
        drug_name = input(Fore.CYAN + "Enter the drug name: " + Style.RESET_ALL)
        result = cli.plugin.execute("analyze_risk", drug_name)
        print(Fore.GREEN + str(result) + Style.RESET_ALL)
    elif action in ["generate_hypotheses", "generate hypotheses"]:
        print(Fore.YELLOW + "Generate Hypotheses: This action generates scientific hypotheses for drug combinations based on risk scores and shared side effects." + Style.RESET_ALL)
        drug_a = input(Fore.CYAN + "Enter the first drug name: " + Style.RESET_ALL)
        drug_b = input(Fore.CYAN + "Enter the second drug name: " + Style.RESET_ALL)
        result = cli.plugin.execute("generate_hypotheses", drug_a, drug_b)
        print(Fore.GREEN + str(result) + Style.RESET_ALL)
    elif action in ["generate_pdf", "generate pdf"]:
        print(Fore.YELLOW + "Generate PDF: This action creates a PDF report for drug risk analysis, including risk scores and shared side effects." + Style.RESET_ALL)
        drug_a = input(Fore.CYAN + "Enter the first drug name: " + Style.RESET_ALL)
        drug_b = input(Fore.CYAN + "Enter the second drug name: " + Style.RESET_ALL)
        hypotheses = cli.plugin.execute("generate_hypotheses", drug_a, drug_b)
        pdf_buffer = cli.plugin.execute("generate_pdf", drug_a, drug_b, hypotheses)
        with open("risk_analysis_report.pdf", "wb") as f:
            f.write(pdf_buffer.read())
        print(Fore.GREEN + "PDF report saved as risk_analysis_report.pdf" + Style.RESET_ALL)
    elif action in ["validate_data", "validate data"]:
        print(Fore.YELLOW + "Validate Data: This action checks the integrity of a data file and ensures it is correctly formatted." + Style.RESET_ALL)
        file_path = input(Fore.CYAN + "Enter the file path: " + Style.RESET_ALL)
        result = cli.plugin.execute("validate_data", file_path)
        print(Fore.GREEN + str(result) + Style.RESET_ALL)
    elif action in ["generate_graph", "generate graph"]:
        print(Fore.YELLOW + "Generate Graph: This action creates a graph visualization using PyVis based on the provided drug name." + Style.RESET_ALL)
        drug_name = input(Fore.CYAN + "Enter the drug name: " + Style.RESET_ALL)
        
        graph_file_path = generate_graph_for_drug(drug_name, cli.plugin.side_effect_lookup)
        if "error" in graph_file_path:
            print(Fore.RED + graph_file_path["error"] + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Graph visualization saved to {graph_file_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Unknown action." + Style.RESET_ALL)


# Add prompt to enter drug names for hypothesis generation
if __name__ == "__main__":
    print(Fore.CYAN + "Welcome to the Eliza AI Framework!" + Style.RESET_ALL)
    print(Fore.YELLOW + "This project provides intelligent scientific assistance for drug risk analysis and visualization." + Style.RESET_ALL)
    print(Fore.GREEN + "Plugins available:" + Style.RESET_ALL)
    print(Fore.MAGENTA + "- DrugRiskAnalysisPlugin: Analyze drug risk scores and side effects." + Style.RESET_ALL)
    print(Fore.MAGENTA + "- DrugInteractionPlugin: Analyze interactions between drugs based on shared side effects." + Style.RESET_ALL)
    print(Fore.MAGENTA + "- RiskVisualizationPlugin: Visualize risk scores using bar charts." + Style.RESET_ALL)
    print(Fore.BLUE + "Visit our website for more information: https://github.com/your-repo" + Style.RESET_ALL)

    cli = ElizaCLI()

    # Prompt user for action
    action = input(Fore.CYAN + "Enter action (analyze_risk, generate_hypotheses, generate_pdf, validate_data, generate_graph): " + Style.RESET_ALL).strip().lower()

    if action in ["generate_graph", "generate graph"]:
        print(Fore.YELLOW + "Generate Graph: This action creates a graph visualization using PyVis based on the provided drug name." + Style.RESET_ALL)
        drug_name = input(Fore.CYAN + "Enter the drug name: " + Style.RESET_ALL)
        graph_file_path = generate_graph_for_drug(drug_name, cli.plugin.side_effect_lookup)
        if "error" in graph_file_path:
            print(Fore.RED + graph_file_path["error"] + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Graph visualization saved to {graph_file_path}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Unknown action." + Style.RESET_ALL)