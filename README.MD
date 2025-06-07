# Eliza AI Plugin Framework

## Overview
The Eliza AI Plugin Framework is an intelligent scientific assistant designed to solve specific scientific problems and provide particular capabilities. The framework consists of self-contained plugins that:

- Solve specific scientific problems.
- Connect to Eliza through standardized interfaces.
- Can be developed independently but work together in the larger ecosystem.

## Features
- **Risk Analysis**: Analyze drug risk scores and side effects.
- **Hypothesis Generation**: Generate scientific hypotheses for drug combinations.
- **Graph Visualization**: Visualize drug-side effect relationships.
- **Data Validation**: Validate the integrity of data files.
- **PDF Report Generation**: Create PDF reports for drug risk analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sideeffectnet.git
   ```
2. Navigate to the project directory:
   ```bash
   cd sideeffectnet
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Command Line Interface
Interact with the plugins using the CLI:

```bash
python3 src/plugin.py <action> [options]
```

### Actions
- `analyze_risk`: Analyze the risk score and side effects for a drug.
  ```bash
  python3 src/plugin.py analyze_risk --drug_name "Aspirin"
  ```
- `generate_hypotheses`: Generate scientific hypotheses for drug combinations.
  ```bash
  python3 src/plugin.py generate_hypotheses --drug_a "Aspirin" --drug_b "Ibuprofen"
  ```
- `generate_pdf`: Create a PDF report for drug risk analysis.
  ```bash
  python3 src/plugin.py generate_pdf --drug_a "Aspirin" --drug_b "Ibuprofen"
  ```
- `validate_data`: Validate the integrity of a data file.
  ```bash
  python3 src/plugin.py validate_data --file_path "data/processed/side_effects_clean.csv"
  ```
- `generate_graph`: Visualize drug-side effect relationships.
  ```bash
  python3 src/plugin.py generate_graph --graph_data "graph_data.json"
  ```

## Development
### Adding New Plugins
1. Create a new class inheriting from `PluginBase`.
2. Implement the `execute` method.
3. Add the plugin to the CLI interface.

### Testing
Run unit tests:
```bash
python3 -m unittest discover src
```

## License
This project is licensed under the MIT License.

Total nodes: 7470
Total edges: 158559


I dont need to build complete KG of all nodes and edges to make it accurate actually, visualizing that many nodes with edges will crash my browser/laptop... so instead i focus on subgraph-based analysis and targeted graph construction to improve performance and maintain accuracy

1. Use Subgraphs for Targeted Analysis: Instead of building the entire graph, dynamically construct subgraphs based on user input or specific queries


AIzaSyAOJe_qdKZnKZBhgkOiyiS-r-PgoMIzPDw
