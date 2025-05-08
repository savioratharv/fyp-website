import os
import ast
import sys
import pkg_resources
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def get_python_files(root_dir):
    """Recursively get all Python files in a project using pathlib."""
    root = Path(root_dir)
    print([str(path.relative_to(root)) for path in root.rglob("*.py")])
    return [str(path.relative_to(root)) for path in root.rglob("*.py")]

def extract_imports(file_path):
    """Extract import statements from a Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    imports = {}  # key: module, value: set of functions (empty set if not specified)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name.split(".")[0]
                if mod not in imports:
                    imports[mod] = set()  # module imported as whole; no specific functions
        elif isinstance(node, ast.ImportFrom) and node.module:
            mod = node.module.split(".")[0]
            funcs = {alias.name for alias in node.names}
            if mod in imports:
                imports[mod] |= funcs
            else:
                imports[mod] = funcs
    
    return imports

def is_internal_import(import_name, project_files):
    """Check if the import corresponds to a file in the project,
       by comparing the expected basename.
    """
    candidate = import_name.replace(".", os.sep) + ".py"  # e.g. "wrapped_flappy_bird.py"
    # Direct match
    if candidate in project_files:
        return candidate
    # Otherwise, search by basename match
    for file in project_files:
        if os.path.basename(file) == candidate:
            return file
    return None

def build_dependency_graph(root_dir):
    """Construct a dependency graph for the project."""
    project_files = get_python_files(root_dir)  # relative paths
    project_files_set = set(project_files)

    # Get list of standard library modules
    stdlib_modules = set(sys.builtin_module_names)

    # Get installed third-party libraries
    installed_packages = set(pkg.key for pkg in pkg_resources.working_set)

    dep_graph = nx.DiGraph()

    # Ensure all files are added as nodes, even if they have no edges
    for file in project_files:
        dep_graph.add_node(file)

    for file in project_files:
        file_path = os.path.join(root_dir, file)
        imports_dict = extract_imports(file_path)
        for imp, funcs in imports_dict.items():
            if imp in stdlib_modules or imp in installed_packages:
                continue  # Ignore these imports

            parent_file = is_internal_import(imp, project_files_set)
            # Eliminate self-loop edges
            if parent_file and parent_file != file:
                dep_graph.add_edge(parent_file, file, imported_functions=funcs)
    return dep_graph

def visualize_dependency_graph(graph):
    """Visualize the dependency graph using matplotlib and networkx."""
    plt.figure(figsize=(10, 6))

    pos = nx.shell_layout(graph, seed=42)  # Position nodes using spring layout
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight="bold", arrows=True)

    plt.title("Python Project Dependency Graph")
    plt.savefig("dependency_graph.png")
