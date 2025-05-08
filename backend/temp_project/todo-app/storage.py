# """
# storage.py
# 
# This module provides functionalities for persistent storage and retrieval of tasks data using JSON format.
# It defines two primary functions: save_tasks and load_tasks.
# 
# Functions:
# - save_tasks(tasks): Serializes a list of tasks and writes it to a JSON file.
# - load_tasks(): Reads a JSON file and deserializes its content into a list of tasks.
# 
# Constants:
# - FILE_NAME (str): The filename used for storing tasks data in JSON format.
# 
# Details:
# - The save_tasks function opens the designated JSON file in write mode and uses the json.dump() method to write the provided tasks data.
# - The load_tasks function attempts to open the JSON file in read mode and load its content. If the file does not exist or contains invalid JSON, it returns an empty list.
# - Exception handling ensures that missing or corrupt files do not cause the program to crash and provides a fallback to an empty task list.
# 
# Usage:
# - These functions facilitate persistent storage of tasks, enabling data to be saved between program executions.
# - They can be integrated into a larger task management system where tasks are stored as data structures (e.g., dictionaries) within a list.
# 
# Design considerations:
# - The JSON format ensures human-readable storage and compatibility with various systems.
# - Error handling enhances robustness by managing common file-related exceptions.
# - The module does not impose a specific structure on tasks, allowing flexibility for different task representations.
# """

import json
FILE_NAME = 'tasks.json'


def save_tasks(tasks):
    """
Save the list of tasks to a JSON file.

Parameters:
- tasks (list): A list of task data structures (e.g., dictionaries) to be stored.

Returns:
- None

Usage example:
    tasks = [{'id': 1, 'title': 'Sample Task', 'completed': False}]
    save_tasks(tasks)
"""
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f)


def load_tasks():
    """
Load and deserialize the list of tasks from a JSON file.

Parameters:
- None

Returns:
- list: A list of task data structures (e.g., dictionaries). If the file does not exist or contains invalid JSON, returns an empty list.

Usage example:
    tasks = load_tasks()
    for task in tasks:
        print(task)
"""
    try:
        with open(FILE_NAME, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
