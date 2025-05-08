# /******************************************************************************/
# /*                                                                            */
# /*                                main.py                                     */
# /*                                                                            */
# /*  File Description:                                                         */
# /*  This script implements the main entry point for the TODO application. It  */
# /*  provides a command-line interface allowing users to manage a list of tasks.*/
# /*  Through a menu-driven system, users can add new tasks, remove existing   */
# /*  tasks, list all current tasks, or exit the application.                   */
# /*                                                                            */
# /*  Dependencies:                                                             */
# /*    - task_manager.TaskManager: A class responsible for handling task data.  */
# /*                                                                            */
# /*  Functions:                                                                */
# /*    - main(): Orchestrates the user interface loop, processes user input,   */
# /*      and interacts with the TaskManager instance to perform task management*/
# /*      operations.                                                           */
# /*                                                                            */
# /******************************************************************************/
# 
# """
# This script provides the main interface for the TODO application.
# 
# Module Description:
# -------------------
# The script initializes an instance of the TaskManager class, which manages the
# list of tasks. It then enters an infinite loop presenting a menu-driven user
# interface allowing users to perform various operations:
# 
# - Add a new task to the list.
# - Remove an existing task from the list.
# - List all current tasks.
# - Exit the application.
# 
# User input is taken via standard input, and based on the input, the script
# calls appropriate methods of the TaskManager instance. If an invalid choice
# is entered, the user is prompted to try again.
# 
# This design separates the user interface logic from the task management logic,
# which is encapsulated within the TaskManager class defined elsewhere in the
# project.
# 
# Function Descriptions:
# --------------------
# main():
#     - Creates an instance of TaskManager.
#     - Repeatedly displays a menu and prompts the user for choices.
#     - Calls TaskManager methods to manipulate or display tasks based on user input.
#     - Exits when the user selects the exit option.
# 
# Note:
# -----
# This script assumes that the TaskManager class has the following methods:
# - add_task(task): Adds a task to the task list.
# - remove_task(task): Removes a specified task from the list.
# - list_tasks(): Displays all current tasks.
# 
# Since the class definitions are imported from external files, their internal
# implementations are not included in this script but are essential for the
# correct operation of the main interface.
# """

from task_manager import TaskManager


def main():
    """def main():
    ""\"
    Entry point for the TODO application.

    Initializes the TaskManager instance and presents a menu-driven interface
    that allows users to add, remove, list tasks, or exit the application.

    Parameters:
        None

    Returns:
        None

    Usage example:
        Run the script from the command line:
        python main.py

        The interactive menu will be displayed, and the user can input choices
        to manage tasks accordingly.
    """
    manager = TaskManager()
    while True:
        print('\nTODO App')
        print('1. Add Task')
        print('2. Remove Task')
        print('3. List Tasks')
        print('4. Exit')
        choice = input('Enter choice: ').strip()
        if choice == '1':
            task = input('Enter task: ').strip()
            manager.add_task(task)
        elif choice == '2':
            task = input('Enter task to remove: ').strip()
            manager.remove_task(task)
        elif choice == '3':
            manager.list_tasks()
        elif choice == '4':
            print('Exiting TODO App.')
            break
        else:
            print('Invalid choice. Try again.')


if __name__ == '__main__':
    main()
