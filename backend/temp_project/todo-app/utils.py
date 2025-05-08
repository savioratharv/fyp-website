# """
# File: utils.py
# 
# Description:
# This module provides utility functions for managing and displaying task lists.
# It contains functions to present tasks in a human-readable format, facilitating
# easy viewing and interaction with task data within a larger application.
# 
# Function:
# - display_tasks(tasks): Displays a list of tasks on the console with enumerated indices.
#   Accepts a list of task descriptions and prints each task preceded by its number in the list.
# 
# Author: [Your Name]
# Date: [Date of creation or last modification]
# Version: 1.0
# 
# Usage:
# Import this module into your Python project and call the display_tasks function
# by passing a list of tasks. Ensure that the tasks parameter is an iterable containing
# string descriptions of each task.
# """

def display_tasks(tasks):
    """
Displays a list of tasks with enumerated indices.

Parameters:
    tasks (list of str): A list containing task descriptions to be displayed.

Returns:
    None: This function only prints the tasks to the console.

Example:
    tasks_list = ["Buy groceries", "Read a book", "Write code"]
    display_tasks(tasks_list)
"""
    print('\nYour Tasks:')
    for i, task in enumerate(tasks, 1):
        print(f'{i}. {task}')
