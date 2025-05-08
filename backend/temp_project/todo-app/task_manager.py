# /********************************************************************************
#  * @file task_manager.py
#  * @brief This module defines the TaskManager class which provides functionalities
#  *        to manage a list of tasks within a software application.
#  *
#  * @details
#  * The TaskManager class encapsulates the operations for adding, removing,
#  * and listing tasks. It interacts with external storage functions to persist
#  * task data and utilizes utility functions for displaying tasks. It is designed
#  * to integrate into a larger software project, relying on imported external
#  * functions for data persistence and display.
#  *
#  * @note
#  * This file assumes that the functions load_tasks, save_tasks, and display_tasks
#  * are properly defined in their respective modules, with the following summaries:
#  * - load_tasks: Loads and deserializes the list of tasks from a JSON file.
#  * - save_tasks: Saves the list of tasks to a JSON file.
#  * - display_tasks: Displays a list of tasks with enumerated indices.
#  ********************************************************************************/
# 
# """
# This module provides the TaskManager class, which manages a collection of tasks.
# This class offers methods to add, remove, and list tasks, facilitating task
# management within an application. The persistence of task data is handled via
# external functions to load from and save to storage. The display utility
# function is used to output the list of tasks to the user interface or console.
# """
# 
# from storage import save_tasks, load_tasks
# from utils import display_tasks
# 
# class TaskManager:
#     """
#     A class to manage a collection of tasks.
#     
#     Attributes:
#         tasks (list of str): A list that holds task descriptions.
#     """
# 
#     def __init__(self):
#         """
#         Initializes a new instance of the TaskManager class.
#         Loads existing tasks from persistent storage.
#         """
#         self.tasks = load_tasks()
# 
#     def add_task(self, task):
#         """
#         Adds a new task to the task list and updates persistent storage.
#         
#         Parameters:
#             task (str): The description of the task to be added.
#             
#         Returns:
#             None
#         """
#         self.tasks.append(task)
#         save_tasks(self.tasks)
#         print(f"Task '{task}' added.")
# 
#     def remove_task(self, task):
#         """
#         Removes a task from the task list if it exists and updates storage.
#         
#         Parameters:
#             task (str): The description of the task to be removed.
#             
#         Returns:
#             None
#         """
#         if task in self.tasks:
#             self.tasks.remove(task)
#             save_tasks(self.tasks)
#             print(f"Task '{task}' removed.")
#         else:
#             print('Task not found.')
# 
#     def list_tasks(self):
#         """
#         Displays all current tasks using the external display function.
#         If no tasks are present, informs the user that no tasks are available.
#         
#         Returns:
#             None
#         """
#         if self.tasks:
#             display_tasks(self.tasks)
#         else:
#             print('No tasks available.')

from storage import save_tasks, load_tasks
from utils import display_tasks


class TaskManager:

    def __init__(self):
        """
Initializes a new instance of the TaskManager class by loading existing tasks from persistent storage.

Parameters:
    None

Returns:
    None

Usage example:
    task_manager = TaskManager()
"""
        self.tasks = load_tasks()

    def add_task(self, task):
        """
Adds a new task to the task list and updates persistent storage.

Parameters:
    task (str): The description of the task to be added.

Returns:
    None

Usage example:
    task_manager = TaskManager()
    task_manager.add_task("Complete unit testing")
"""
        self.tasks.append(task)
        save_tasks(self.tasks)
        print(f"Task '{task}' added.")

    def remove_task(self, task):
        """
Removes a specified task from the task list if it exists and updates persistent storage.

Parameters:
    task (str): The description of the task to be removed.

Returns:
    None

Usage example:
    task_manager = TaskManager()
    task_manager.remove_task("Read a book")
"""
        if task in self.tasks:
            self.tasks.remove(task)
            save_tasks(self.tasks)
            print(f"Task '{task}' removed.")
        else:
            print('Task not found.')

    def list_tasks(self):
        """
Displays all current tasks using the external display function. If there are no tasks available,
it informs the user accordingly.

Parameters:
    None

Returns:
    None

Usage example:
    task_manager = TaskManager()
    task_manager.list_tasks()
"""
        if self.tasks:
            display_tasks(self.tasks)
        else:
            print('No tasks available.')
