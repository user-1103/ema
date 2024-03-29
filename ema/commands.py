"""
This module contains all the user facing commands
"""

from ema.gacha import Task, User
from printer import ema_print, todo_print

def add(u: User, t: str) -> None:
    """
    Adds a task to a user.

    :param u: The user to add to
    :param t: The str description of the task format
    """
    task_string = t.split("/")
    if (len(task_string) != 3):
        raise Exception(f"Task not added. Bad Format!")
    is_daily = False
    if (task_string[0] == "d"):
        is_daily = True
    try:
        tickets = int(task_string[2])
        tmp = Task(task_string[1], tickets=tickets, is_daily=is_daily )
    except Exception as e:
        tmp = Task(task_string[1], engraved_reward=task_string[2],
                   is_daily=is_daily)
    u.tasks.append(tmp)
    ema_print("I will now pay you if you do these tasks!")
    todo_print(u)

def remove(u: User, name: str) -> None:
    """
    Remove a task to a user.

    :param u: The user to add to
    :param name: The name of the task
    """
    u.tasks = [x for x in u.tasks if (x.name == name)]
    ema_print("I will now pay you if you do these tasks!")
    todo_print(u)

def done(u: User, name: str) -> None:
    """
    Mark task as done

    :param u: The user to add to
    :param name: The name of the task
    """
    tmp = [x for x in u.tasks if (x.name == name)]
    tmp = [x for x in u.tasks if (x.is_done == False)]
    tmp = [x for x in u.tasks if (x.is_daily == False)]
    if (len(tmp) != 1):
        raise Exception("Can't find the task!")
    for x in tmp:
        x.is_done = True
        u.tickets += x.tickets
        ema_print((f"Very good! I will give you {x.tickets}"
                    f"tickets for your work!"))

    



