import json
import os
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)  # automatically reset color after each print

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print(Fore.YELLOW + "No tasks found!")
        return
    table = []
    for task in tasks:
        status = Fore.GREEN + "✅ Completed" if task["completed"] else Fore.RED + "❌ Pending"
        table.append([task["id"], task["task"], status])
    print(tabulate(table, headers=[Fore.CYAN + "ID", "Task", "Status"], tablefmt="fancy_grid"))

def add_task():
    tasks = load_tasks()
    task_desc = input(Fore.CYAN + "Enter task description: ")
    task_id = max([task["id"] for task in tasks], default=0) + 1
    tasks.append({"id": task_id, "task": task_desc, "completed": False})
    save_tasks(tasks)
    print(Fore.GREEN + "Task added!")

def remove_task():
    tasks = load_tasks()
    list_tasks()
    try:
        task_id = int(input(Fore.CYAN + "Enter task ID to remove: "))
        tasks = [task for task in tasks if task["id"] != task_id]
        save_tasks(tasks)
        print(Fore.GREEN + "Task removed!")
    except ValueError:
        print(Fore.RED + "Invalid input!")

def mark_complete():
    tasks = load_tasks()
    list_tasks()
    try:
        task_id = int(input(Fore.CYAN + "Enter task ID to mark complete: "))
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
        save_tasks(tasks)
        print(Fore.GREEN + "Task marked complete!")
    except ValueError:
        print(Fore.RED + "Invalid input!")

def menu():
    while True:
        print("\n" + Fore.MAGENTA + "--- TO-DO LIST MENU ---")
        print(Fore.YELLOW + "1." + Fore.RESET + " List tasks")
        print(Fore.YELLOW + "2." + Fore.RESET + " Add task")
        print(Fore.YELLOW + "3." + Fore.RESET + " Remove task")
        print(Fore.YELLOW + "4." + Fore.RESET + " Mark task complete")
        print(Fore.YELLOW + "5." + Fore.RESET + " Exit")
        choice = input(Fore.CYAN + "Choose an option: ")
        if choice == "1":
            list_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            remove_task()
        elif choice == "4":
            mark_complete()
        elif choice == "5":
            print(Fore.MAGENTA + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice!")

if __name__ == "__main__":
    menu()
