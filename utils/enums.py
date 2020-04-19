# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Enumeration utility classes.
"""

from enum import Enum, auto


__all__ = ['OptionRight', 'BarrierUpDown', 'BarrierInOut']


class PPEnum(Enum):
    """Enum with prettier printing."""

    def __repr__(self) -> str:
        return super().__repr__().split('.')[1].split(':')[0]

    def __str__(self) -> str:
        return super().__str__().split('.')[1]


class OptionRight(PPEnum):
    """Right of an option."""
    Call = auto()
    Put = auto()


class BarrierUpDown(PPEnum):
    """Up or down type barrier option."""
    Up = auto()
    Down = auto()


class BarrierInOut(PPEnum):
    """In or out type barrier option."""
    In = auto()
    Out = auto()
