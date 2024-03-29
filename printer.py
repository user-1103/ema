"""
This module contains the code for displaying data to the user in a cli fasion.
"""
from typing import Final
from rich.console import Console
from rich.markdown import Markdown
from rich.columns import Columns
from rich.table import Table
from time import time

from ema.gacha import PETS, User

CONSOLE: Final[Console] = Console()

def ema_print(t: str) -> None:
    """
    Prints as if ema was taking.

    :param t: The str to print
    """
    CONSOLE.print(f"😾> '{t}'")

def inventory_print(u: User) -> None:
    """
    Prints a users inventory.

    :param u: The user to print
    """
    inventory = list()
    for b in u.banners:
        for r in b.rewards:
            for n in range(r.num_in_invintory):
                tmp = Markdown(f"**{r.name}**\n{r.description}")
                inventory.append(tmp)
    CONSOLE.print(Columns(inventory, expand=True, equal=True))

def todo_print(u: User) -> None:
    """
    Prints a users todos.

    :param u: The user to print
    """
    tasks = list()
    for t in u.tasks:
        if (not t.is_done):
            if (not t.is_daily):
                tmp = f"**{t.name}**\nGives {t.tickets} tickets"
                if (len(t.engraved_reward) > 0):
                    tmp += f"\n{t.engraved_reward}"
                tasks.append(Markdown(tmp))
    CONSOLE.print(Columns(tasks, expand=True, equal=True))

def day_print(u: User) -> None:
    """
    Prints a users dailys.

    :param u: The user to print
    """
    tasks = list()
    for t in u.tasks:
        if (not t.is_done):
            if (t.is_daily):
                tmp = f"**{t.name}**\nGives {t.tickets} tickets"
                if (len(t.engraved_reward) > 0):
                    tmp += f"\n{t.engraved_reward}"
                tasks.append(Markdown(tmp))
    CONSOLE.print(Columns(tasks, expand=True, equal=True))

def done_print(u: User) -> None:
    """
    Prints a users done.

    :param u: The user to print
    """
    tasks = list()
    for t in u.tasks:
        if (t.is_done):
            tmp = f"**{t.name}**\nGives {t.tickets} tickets"
            if (len(t.engraved_reward) > 0):
                tmp += f"\n{t.engraved_reward}"
            tasks.append(Markdown(tmp))
    CONSOLE.print(Columns(tasks, expand=True, equal=True))

    
def banner_print(u: User) -> None:
    """
    Prints available banners

    :param u: The user to print
    """
    banners = [x for x in u.banners if (x.max_win != 0)]
    banners = [x for x in banners if (x.max_pull != 0)]
    banners = [x for x in banners if ((x.max_time == -1) or (x.max_time <= time()))]
    print_list = list()
    for b in banners:
        tmp = f"**{b.name}**\n{b.description}\n"
        if (b.gems > 0):
            tmp += f"*Requires {b.gems} gems to unlock*"
        print_list.append(Markdown(tmp))
    CONSOLE.print(Columns(print_list, expand=True, equal=True))
    
def pet_print(u: User) -> None:
    """
    Prints pet table

    :param u: The user to print
    """
    pets = dict()
    for p in u.pets:
        pets[p] = (pets.get(p, 0) + 1)
    for p in PETS.keys():
        if (p not in pets):
            pets[p] = 0
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("# Owned", style="dim")
    table.add_column("Type", justify="center")
    table.add_column("Description")
    table.add_column("Cost In Silver")
    table.add_column("Gold Production")
    table.add_row(*[str(x) for x in pets.values()])
    table.add_row(*[str(x) for x in pets.keys()])
    table.add_row(*[str(x[2]) for x in PETS.values()])
    table.add_row(*[str(x[0]) for x in PETS.values()])
    table.add_row(*[str(x[1]) for x in PETS.values()])
    CONSOLE.print(table)
