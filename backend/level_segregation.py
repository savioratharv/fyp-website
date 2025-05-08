import networkx as nx

def segregate_levels(graph):
    """Segregate nodes into levels and capture dependency function import info."""
    levels = {}         # level index -> set of nodes
    dependencies = {}   # child node -> dict { parent_node: imported_functions }
    level = 0
    # Start with leaf nodes (no incoming edges)
    current_level_nodes = {node for node in graph.nodes if graph.in_degree(node) == 0}

    while current_level_nodes:
        levels[level] = current_level_nodes
        next_level_nodes = set()
        for node in graph.nodes:
            if node in set().union(*levels.values()):
                continue
            mapping = {}
            for pred in graph.predecessors(node):
                if pred in current_level_nodes:
                    funcs = graph.edges[pred, node].get("imported_functions", set())
                    mapping[pred] = funcs
            if mapping:
                next_level_nodes.add(node)
                dependencies[node] = mapping
        current_level_nodes = next_level_nodes
        level += 1

    return levels, dependencies
