import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from create_graph import build_dependency_graph
from level_segregation import segregate_levels
import multiprocessing
import ast
import astor
import time
from pyvis.network import Network
import networkx as nx

def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# def process_node(node, project_root, dependencies):
#     sanitized_file_name = node.replace("\\/", "\/")
#     full_path = os.path.join(project_root, sanitized_file_name)
#     file_content = extract_text_from_file(full_path)
    
#     if not file_content:
#         return f"Failed to process {node}"

#     prompt = f"""{file_content}You are a technical writer tasked with creating code documentation for this particular 
#     code file in the Engineering department of a technology/software company. 
#     Write a function-by-function overview explaining key tasks, purpose, and aspects, and defining 
#     segments of each function. Follow consistent formatting, use clear and concise language, provide context 
#     where necessary. Keep in mind, that this code file is a part of a much larger software project.
#     Since this code file is part of a larger software project, the functions used may be defined in other 
#     files or dependencies. 
#     generate a markdown documentation for this current file: {node}. Return only the markdown part 
#     of the documentation. Do not include any other text or explanation. No ''''markdown tag or anything."""

#     client = OpenAI()
#     client.api_key = os.getenv("OPENAI_API_KEY")
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
    
#     docs_dir = os.path.join(os.getcwd(), "generated_docs")
#     os.makedirs(docs_dir, exist_ok=True)
#     doc_path = os.path.join(docs_dir, f"{node[:-3]}.md")
#     with open(doc_path, "w", encoding="utf-8") as f:
#         f.write(response.choices[0].message.content.strip())

#     dependent_nodes = dependencies.get(node, {})
#     dependent_functions = {dep_node: functions for dep_node, functions in dependent_nodes.items()}
    
#     return f"Processed {node}"

# Global storage for function summaries:
node_function_summaries = {}  # { parent_node: { function_name: summary } }

def process_node(node, project_root, dependencies):
    print(f"Processing node: {node}")
    sanitized_file_name = node.replace("\\/", "\/")
    full_path = os.path.join(project_root, sanitized_file_name)
    file_content = extract_text_from_file(full_path)
    
    if not file_content:
        return f"Failed to process {node}"
    
    if node_function_summaries and node in node_function_summaries:
        functions = {}
        
        for func in node_function_summaries[node].keys():
            functions[func] = node_function_summaries[node][func]
        
        prompt = f"""{file_content}
        Generate comprehensive Python file documentation following IEEE 1016 and GNU coding standards.

        Use clear, concise language and consistent terminology. Avoid jargon and abbreviations. Provide context where necessary.
       
        Since this code file is part of a larger software project, the functions used may be defined in other files or dependencies. Here is a list of functions that have been defined outside the current code file and their summaries:
        {functions}
        Use these summaries to help you understand the context of the current file.
        
        generate documentation for this current file: {node}. Return only the documentation text and nothing else.
        
        NO MARKDOWN TAGS OR ANYTHING ELSE."""
    
    else:
    # Create documentation for the current node file
        prompt = f"""{file_content}
        Generate comprehensive Python file documentation following IEEE 1016 and GNU coding standards.

        Use clear, concise language and consistent terminology. Avoid jargon and abbreviations. Provide context where necessary.

        generate documentation for this current file: {node}. Return only the documentation text and nothing else.
        
        NO MARKDOWN TAGS OR ANYTHING ELSE."""
    

    history = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    start_time = time.time()
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for {node} overall documentation: {elapsed_time:.2f} seconds")
    
    history.append(response.choices[0].message)

    overall_doc = response.choices[0].message.content.strip()
    # Convert overall documentation into a comment block
    overall_doc_comment = "\n".join([f"# {line}" for line in overall_doc.splitlines()])

    func_documented = {}

    def generate_docstring(func_node):
        """Generate a basic docstring for a function node."""
        func_name = func_node.name
        func_prompt = (
                f"For the file {node}, generate a Python docstring for the function '{func_name}' that explains its purpose, "
                f"lists all parameters with types and descriptions, specifies the return value, and provides a usage example. "
                f"Follow PEP 257 standards and return only the docstring text."
            )
        history.append({
                    "role": "user",
                    "content": func_prompt
                })
        
        start_time = time.time()
        response_func = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=history
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken for {node} function docstring: {elapsed_time:.2f} seconds")
        history.append(response_func.choices[0].message)
        doc = f'"""{response_func.choices[0].message.content.strip()}"""'
        func_documented[func_name] = response_func.choices[0].message.content.strip()
        time.sleep(20)
        return doc

    class DocstringInserter(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            # Check if the function already has a docstring
            if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str)):
                # No docstring, so create one
                docstring = generate_docstring(node)
                # Create a new node for the docstring and insert it at the start of the function body
                doc_node = ast.Expr(value=ast.Str(s=docstring.strip('"""')))
                node.body.insert(0, doc_node)
            return node

    def insert_docstrings(source_code):
        tree = ast.parse(source_code)
        tree = DocstringInserter().visit(tree)
        # Optionally fix the missing locations (only needed if you plan to use this AST further)
        ast.fix_missing_locations(tree)
        return astor.to_source(tree)
    
    file_content = extract_text_from_file(full_path)
    
    updated_source = insert_docstrings(file_content)

    final_source = overall_doc_comment + "\n\n" + updated_source
    
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(final_source)

    print("Documentation generation completed for file:", node)

    print("Starting to look for dependencies of file:", node)    
    # Find parents in the dependency graph that depend on the current node.
    # For example, given Dependencies: {'task_manager.py': {'storage.py': {'load_tasks', 'save_tasks'}, ...}, ...}
    dependents = {}  # { parent_node: set(functions) }
    for parent_node, child_mapping in dependencies.items():
        if node in child_mapping:
            dependents[parent_node] = child_mapping[node]
    
    print("Adding function summaries for dependents of file:", node)
    # For every parent dependent, query the agent for a summary of each used function.
    if dependents:
        for parent, functions in dependents.items():
            func_summaries_for_parent = {}
            for func in functions:
                # func_prompt = (
                #     f"For the file {node}"
                #     f"Generate a Python docstring for this function {func} that explains its purpose, lists all parameters with types and descriptions, specifies the return value, and includes a usage example. Follow PEP 257 standards."
                # )
                # history.append({
                #     "role": "user",
                #     "content": func_prompt
                # })
                # start_time = time.time()
                # response_func = client.chat.completions.create(
                #     model="gpt-4.1-nano",
                #     messages=history
                # )
                # end_time = time.time()
                # elapsed_time = end_time - start_time
                # print(f"Time taken for {node} function dependency docstring: {elapsed_time:.2f} seconds")
                # history.append(response_func.choices[0].message)
                # summary_text = response_func.choices[0].message.content.strip()
                func_summaries_for_parent[func] = func_documented.get(func)
            if node_function_summaries.get(parent) is None:
                node_function_summaries[parent] = func_summaries_for_parent
            else:
                node_function_summaries[parent].update(func_summaries_for_parent)


    return f"Processed {node}"

def main():
    project_root = input("Enter the project root directory: ").strip()
    if not os.path.isdir(project_root):
        print("Invalid directory. Please check the path.")
        return
    graph = build_dependency_graph(project_root)

    visualize_graph = graph

    print("Nodes:", graph.nodes)
    print("Edges:", graph.edges)

    for u, v, data in visualize_graph.edges(data=True):
        for key in data:
            if isinstance(data[key], set):
                data[key] = list(data[key])
            
    # Plot with pyvis
    net = Network(
        directed = True
    )
    net.from_nx(visualize_graph) # Create directly from nx graph
    net.save_graph(f'{project_root}.html')

    print(graph)

    # Get Levels
    levels, dependencies = segregate_levels(graph)

    print("Levels:", levels)
    print("Dependencies:", dependencies)
    
    # Map node names to pyvis node ids (usually the same as the node name)
    node_id_map = {str(node): str(node) for node in graph.nodes}

    for level in levels:
        print(f"Processing level {level} ...")
        curr_level = list(levels[level])

        # Set current level nodes to orange before processing
        for n in net.nodes:
            if n['id'] in curr_level:
                n['color'] = 'orange'
        net.save_graph(f'{project_root}.html')

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_node, node, project_root, dependencies): node for node in curr_level}
            for future in as_completed(futures):
                node = futures[future]
                print(future.result())
                # Update node color in pyvis to green after processing
                for n in net.nodes:
                    if n['id'] == node:
                        n['color'] = 'green'
                net.save_graph(f'{project_root}.html')
        print(f"Completed processing level {level}.")
        print("Agents sleeping for 60 seconds to avoid rate limits.")
        time.sleep(30)

    # Save final graph
    

if __name__ == "__main__":
    main()

