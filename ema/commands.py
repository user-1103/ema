"""
This module contains all the user facing commands
"""

from collections.abc import Callable
from typing import Any, Dict, Final, Tuple
from ema.gacha import Task, User, check_in_user, spin_user
from printer import day_print, done_print, ema_print, inventory_print, spin_print, todo_print


def tasks(u: User, t: str) -> None:
    """
    List todos.

    :param u: The user
    :param t: unused
    """
    ema_print("I will pay you if you do these tasks for me...")
    todo_print(u)

def archive(u: User, t: str) -> None:
    """
    List done tasks.

    :param u: The user
    :param t: unused
    """
    ema_print("This is what you have done for me...")
    done_print(u)

def daily(u: User, t: str) -> None:
    """
    List daily tasks.

    :param u: The user
    :param t: unused
    """
    ema_print("If you want a cut of what my workers have found you must do"
              " your dailes!")
    day_print(u)

def inventory(u: User, t: str) -> None:
    """
    List inventory.

    :param u: The user
    :param t: unused
    """
    ema_print("This is what you have on your person:")
    inventory_print(u)

def checkin(u: User, t: str) -> None:
    """
    Checkin daily tasks.

    :param u: The user
    :param t: unused
    """
    ema_print("Have you done your daily tasks?")
    day_print(u)
    if (input("Done [Y/n]?").lower() == "n"):
        raise Exception("You must do you daily tasks first!")
    check_in_user(u)

def roll(u: User, t: str) -> None:
    """
    Adds a task to a user.

    :param u: The user to add to
    :param t: The name of the banner to roll
    """
    reward = spin_user(u, t)
    ema_print("Lets spin the wheal and see what you got!")
    spin_print(reward)

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

CMDS: Final[Dict[str, Tuple[Callable[[User, str], None], str]]] = {
        "t": ( tasks, "List undone tasks."),
        "T": ( archive, "List finished tasks."),
        "d": ( done, "Mark task as done."),
        "D": ( daily, "List daily tasks."),
        "i": ( inventory, "List invintory."),
        "x": ( remove, "Delete named task."),
        "c": ( checkin, "Checkin."),
        "r": ( roll, "Roll for a given banner."),
        }
