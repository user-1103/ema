"""
This module contains the code responsible for storing, spinning, and rewarding
items from banners.
"""

from dataclasses import dataclass, field
from typing import Dict, Final, List, Tuple
from pathlib import Path
from pickle import dump, load
from time import time
from random import choices, randint


PETS: Final[Dict[str, Tuple[int, int, str]]] = {
        "👶": (5, 0, "Christan Baby: do not get in an ariplaine with him"),
        "😀": (100, 5, "Normal Human: fears god, works slowly"),
        "😇": (100, -5, "Angle: they work for god?"),
        "🤐": (110, 6, "Mute Human: they do not fear new languages"),
        "💁": (115, 7, "Fruit: Not exactly psyked about the catholic church"),
        "🥵": (120, 8, "Horny Human: lets clap some angleic cheaks"),
        "🤓": (130, 9, "Anti-Theist Human: what is there to fear"),
        "🐴": (135, 10, "Horse: he wants revenge for being put in this form"),
        "😈": (140, 11, "Lucifer: just wants to talk to the big guy..."),
        "🤖": (150, 15, "Cylon: this tower is just part of his plan"),
        "🍄": (160, 20, "Mushroom: already knows the name of god")
        }

@dataclass
class Reward():
    """
    Represents a reward that can be won.

    :param name: The name of the item
    :param description: What is this item
    :param weight: Rarity of this item 1-5, 1 being rare
    :param num_in_store: How many can still be won
    :param num_in_invintory: How many have been used
    :param num_in_exile: How many have been used
    """
    name: str
    description: str = "<No Description>"
    weight: int = 3
    num_in_store: int = 1
    num_in_invintory: int = 0
    num_in_exile: int = 0


@dataclass
class Banner():
    """
    Represents a group of rewards that can be won.

    :param name: The name of the item
    :param description: What is this banner about
    :param max_pull: What is max number of pulls, -1 for no limit
    :param max_time: What is the expiration of the banner in seconds from EPOC, -1 for no limit
    :param max_win: What is max number of wins, -1 for no limit
    :param pity_level: How much pity has been accumulated for this banner
    :param pity_step: How much pity gets added each pull
    :param pity_threshold: How much pity is required to get a good item
    :param gems: How many gems are required to use this banner
    :param cost: How many tickets are required to use this banner
    :param win_to_fail: 0-100 percent chance a reward is given 
    :param rewards: The list of rewards in the banner
    """
    name: str
    description: str = "<No Description>"
    max_pull: int = -1
    max_time: int = -1
    max_win: int = -1
    pity_level: int = 0
    pity_step: int = 0
    pity_threshold: int = 100
    gems: int = 0
    cost: int = 1
    win_to_fail: int = 70
    rewards: List[Reward] = field(default_factory=list)

@dataclass
class Task():
    """
    Represents a task

    :param name: What needs to be done
    :param tickets: The number of tickets rewarded
    :param engraved_reward: Does this task directly give a reward
    :param is_done: Is it done
    :param is_daily: Is it a daily?
    :param uuid: Unique id?
    """
    name: str
    tickets: int = 0
    engraved_reward: str = ""
    is_done: bool = False
    is_daily: bool = False
    UUID: str = field(default_factory=lambda : str(time()))


@dataclass
class User():
    """
    Represents a user and their inventory.

    :param uname: The users name
    :param gems: How many gems the user has
    :param gold: How many gold the user has
    :param silver: How many silver the user has
    :param tickets: How many tickets the user has
    :param version: What version is the save file
    :param lastlogin: Timestamp of last login
    :param pets: List of pets
    :param banners: List of banners
    :param tasks: List of tasks
    """
    uname: str
    gems: int = 0
    gold: int = 0
    silver: int = 0
    tickets: int = 0
    version: int = 1
    lastlogin: float = 0.0
    pets: List[str] = field(default_factory=list)
    banners: List[Banner] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

def save_user(u: User) -> None:
    """
    Saves the users data to the home dir.

    :param u: The user to save
    """
    with open(Path(f"~/.ema-save"), 'wb') as f:
        dump(u, f)

def load_user() -> User:
    """
    Loads the users data to the home dir.

    :return: The user to save
    """
    with open(Path(f"~/.ema-save"), 'rb') as f:
        ret = load(f)
    return ret

def spin_user(u: User, banner_name: str) -> str:
    """
    Performs a spin for a user on a given banner. Updates User.

    :param u: The user who is spinning
    :param banner_name: The name of the banner to spin
    :return: The won reward or None if miss
    """
    banner = [x for x in u.banners if (x.name == banner_name)]
    banner = [x for x in banner if (x.max_win != 0)]
    banner = [x for x in banner if (x.max_pull != 0)]
    banner = [x for x in banner if ((x.max_time == -1) or (x.max_time <= time()))]
    if (len(banner) == 0):
        raise Exception("Banner is not acessable!")
    if (len(banner) > 1):
        raise Exception("To many banners!")
    curent_banner = banner[0]
    curent_rewards = [x for x in curent_banner.rewards if (x.num_in_store != 0)]
    if (len(curent_banner.rewards) == 0):
        raise Exception("Banner is empty!")
    if (User.tickets < curent_banner.cost):
        raise Exception("Not enough tickets!")
    User.tickets -= curent_banner.cost
    if (User.gems < curent_banner.gems):
        raise Exception("Not enough gems!")
    User.gems -= curent_banner.gems
    curent_banner.gems = 0
    curent_banner.max_pull -= 1
    if (curent_banner.pity_threshold >= curent_banner.pity_level):
        if (curent_banner.win_to_fail > randint(0, 100)):
            curent_banner.pity_level += curent_banner.pity_step
            return give_user_secondary_prize(u)
    weights = [x.weight for x in curent_rewards]
    rolls = choices(curent_rewards, weights, k=curent_banner.pity_level)
    rolls.sort(reverse=True, key=lambda x: x.weight)
    curent_banner.max_win -= 1
    ret = rolls[0]
    ret.num_in_store -= 1
    ret.num_in_invintory += 1
    return ret.name

def give_user_secondary_prize(u: User) -> str:
    """
    Gives the user a secondary prize.

    :param u: The user to give a prize
    :return: A info text about what was done
    """
    mode = randint(0, 4)
    if (mode == 0):
        u.tickets += 1
        return "a bonus spin"
    elif (mode == 1):
        tmp = randint(0, 3)
        u.gems += tmp
        return f"{tmp} gems"
    elif (mode == 2):
        tmp = randint(0, 3)
        u.gold += tmp
        return f"{tmp} gold"
    elif (mode == 3):
        tmp = randint(0, 3)
        u.silver += tmp
        return f"{tmp} silver"
    else:
        tmp = randint(0, 3)
        return f"{tmp} clowns"


def calculate_day_reward(u: User) -> int:
    """
    Calculate daily check in reward.

    :param u: The user to give a prize
    :return: The number of silver the user has received
    """
    ret = 0
    for x in u.pets:
        for k,v in PETS.items():
            if (k in x):
                ret += v[1]
    return ret

def check_in_user(u: User) -> int:
    """
    Gives the user their daily check in reward.

    :param u: The user to give a prize
    :return: The number of silver the user has received
    """
    if ((u.lastlogin + 86400) >= time()):
        raise Exception("You already checked in!")
    u.lastlogin = time()
    return calculate_day_reward(u)




