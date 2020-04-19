# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Miscellaneous utility methods.
"""

from typing import Any, Union


__all__ = ['Number', 'is_num', 'is_pos']


_T = (int, float)
Number = Union[int, float]


def is_num(val: Any) -> bool:
    """
    Check if the input value is a finite number.

    Parameters
    ----------
    val : object
        Value to check.

    Returns
    -------
    bool

    Examples
    --------
    >>> from utils.misc import is_num
    >>> print(is_num(10))
    True
    >>> print(is_num(None))
    False

    """
    if not isinstance(val, _T):
        return False
    return True


def is_pos(val: Any) -> bool:
    """
    Check if the input value is a finite positive number.

    Parameters
    ----------
    val : object
        Value to check.

    Returns
    -------
    bool

    Examples
    --------
    >>> from utils.misc import is_pos
    >>> print(is_pos(10))
    True
    >>> print(is_pos(-10))
    False

    """
    if not is_num(val):
        return False
    if not val >= 0:
        return False
    return True
