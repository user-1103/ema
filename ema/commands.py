"""
This module contains all the user facing commands
"""



def add(u: User, t: str) -> None:
    """
    Adds a task to a user.

    :param u: The user to add to
    :param t: The str description of the task format
    """
    tast_string = t.split("/")


