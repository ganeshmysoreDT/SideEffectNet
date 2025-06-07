from pyvis.network import Network
import networkx as nx

def visualize_graph(graph, output_path="graph.html", max_nodes=300):
    
    net = Network(height="750px", width="100%", notebook=False, bgcolor="#222222", font_color="white")

    # Optional: limit nodes for performance
    subgraph = graph.subgraph(list(graph.nodes)[:max_nodes])

    # Customize nodes
    for node in subgraph.nodes():
        degree = subgraph.degree(node)
        subgraph.nodes[node]['size'] = 10 + degree  # Base size + degree

    for node, data in subgraph.nodes(data=True):
        size = data.get("size", 10)  # Use the calculated size
        net.add_node(
            node,
            label=data.get("label", node),
            color=data.get("color", "#97c2fc"),
            group=data.get("type", "unknown"),  # Group by node type
            size=size,
            title=f"Node: {node}<br>Degree: {subgraph.degree(node)}"  # Tooltip with additional info
        )

    # Add edges with optional titles
    for src, dst, edge_data in subgraph.edges(data=True):
        net.add_edge(
            src, 
            dst, 
            title=edge_data.get("title", "causes"), 
            color=edge_data.get("color", "#cccccc"), 
            width=edge_data.get("weight", 2)  # Edge thickness based on weight
        )

    # Apply layout algorithm with adjusted parameters to reduce edge overlap
    net.force_atlas_2based(
        gravity=-30,  # Adjust gravity to spread nodes further apart
        central_gravity=0.01, 
        spring_length=150,  # Increase spring length to reduce edge overlap
        spring_strength=0.1  # Adjust spring strength for better spacing
    )

    net.from_nx(subgraph)

    print(f"Generating interactive graph with {len(subgraph.nodes)} nodes and {len(subgraph.edges)} edges...")

    net.show_buttons(filter_=['physics'])  # Add physics control buttons for user customization
    net.write_html(output_path, notebook=False, open_browser=False)
    print(f"Graph saved as {output_path}")


def visualize_complete_graph(graph, output_path="complete_graph.html"):

        net = Network(height="750px", width="100%", notebook=False, bgcolor="#222222", font_color="white")

        # Customize nodes
        for node in graph.nodes():
            degree = graph.degree(node)
            graph.nodes[node]['size'] = 10 + degree  # Base size + degree

        for node, data in graph.nodes(data=True):
            size = data.get("size", 10)  # Use the calculated size
            net.add_node(
                node,
                label=data.get("label", node),
                color=data.get("color", "#97c2fc"),
                group=data.get("type", "unknown"),  # Group by node type
                size=size,
                title=f"Node: {node}<br>Degree: {graph.degree(node)}"  # Tooltip with additional info
            )

        # Add edges with optional titles
        for src, dst, edge_data in graph.edges(data=True):
            net.add_edge(
                src, 
                dst, 
                title=edge_data.get("title", "causes"), 
                color=edge_data.get("color", "#cccccc"), 
                width=edge_data.get("weight", 2)  # Edge thickness based on weight
            )

        # Apply layout algorithm
        net.force_atlas_2based()

        net.from_nx(graph)

        print(f"Generating complete interactive graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges...")

        net.show_buttons(filter_=['physics'])  # Add physics control buttons for user customization
        net.write_html(output_path, notebook=False, open_browser=False)
        print(f"Complete graph saved as {output_path}")
