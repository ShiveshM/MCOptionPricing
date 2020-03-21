# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Payoff of an option.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from utils.enums import OptionRight, BarrierUpDown, BarrierInOut


__all__ = ['BasePayoff', 'VanillaPayOff', 'AsianArithmeticPayOff',
           'DiscreteBarrierPayOff']


@dataclass
class BasePayoff(ABC):
    """Base class for calculating the payoff."""
    K: float
    option_right: (str, OptionRight)

    @property
    def option_right(self) -> OptionRight:
        """Right of the option."""
        return self._option_right

    @option_right.setter
    def option_right(self, val: (str, OptionRight)) -> None:
        """Set the option_right of the option."""
        if isinstance(val, str):
            if not hasattr(OptionRight, val):
                or_names = [x.name for x in OptionRight]
                raise ValueError(f'Invalid str {val}, expected {or_names}')
            self._option_right = OptionRight[val]
        elif isinstance(val, OptionRight):
            self._option_right = val
        else:
            raise TypeError(
                f'Expected str or OptionRight, instead got type {type(val)}!'
            )

    def _calculate_call(self, S: float) -> float:
        """Call option."""
        return max(S - self.K, 0.)

    def _calculate_put(self, S: float) -> float:
        """Put option."""
        return max(self.K - S, 0.)

    @abstractmethod
    def calculate(self, S: float) -> float:
        """Calulate the payoff for a given spot."""


class VanillaPayOff(BasePayoff):
    """
    Class for calculating the payoff of a vanilla option.

    Attributes
    ----------
    option_right : Right of the option.
    K : Strike price.

    Methods
    ----------
    calculate(S)
        Calulate the payoff given a spot price.

    Examples
    ----------
    >>> from utils.payoff import VanillaPayOff
    >>> payoff = VanillaPayOff(option_right='Call', K=150.)
    >>> print(payoff.calculate(160.))
    10.0

    """

    def calculate(self, S: (float, List[float])) -> float:
        """
        Calulate the payoff given a spot price.

        Parameters
        ----------
        S : Spot price or list of spot prices.

        Returns
        ----------
        payoff : Payoff.

        Notes
        ----------
        If a list is given as input, the final entry will be taken to evaluate.

        """
        if not isinstance(S, float):
            S = S[-1]
        if self.option_right == OptionRight.Call:
            payoff = self._calculate_call(S)
        else:
            payoff = self._calculate_put(S)
        return payoff


class AsianArithmeticPayOff(BasePayoff):
    """
    Class for calculating the payoff of an arithmetic Asian option.

    Attributes
    ----------
    option_right : Right of the option.
    K : Strike price.

    Methods
    ----------
    calculate(S)
        Calulate the payoff given a set of prices for the underlying.

    Examples
    ----------
    >>> from utils.payoff import AsianArithmeticPayOff
    >>> payoff = AsianArithmeticPayOff(option_right='Call', K=150)
    >>> print(payoff.calculate([140, 150, 160, 170, 180]))
    10.0

    """

    def calculate(self, S: List[float]) -> float:
        """
        Calulate the payoff given a set of prices for the underlying.

        Parameters
        ----------
        S : Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Returns
        ----------
        payoff : Payoff.

        """
        avg_sum = sum(S) / len(S)
        if self.option_right == OptionRight.Call:
            payoff = self._calculate_call(avg_sum)
        else:
            payoff = self._calculate_put(avg_sum)
        return payoff


@dataclass(init=False)
class DiscreteBarrierPayOff(BasePayoff):
    """
    Class for calculating the payoff of a discrete barrier European style
    option.

    Attributes
    ----------
    option_right : Right of the option.
    K : Strike price.
    B : Barrier price.
    barrier_updown : Up or down type barrier option.
    barrier_inout : In or out type barrier option.

    Methods
    ----------
    calculate(S)
        Calulate the payoff given a set of prices for the underlying.

    Examples
    ----------
    >>> from utils.payoff import DiscreteBarrierPayOff
    >>> payoff = DiscreteBarrierPayOff(option_right='Call', K=100, B=90,
                                       barrier_updown='Down', barrier_inout='Out')
    >>> print(payoff.calculate([100., 110., 120.]))
    20.0
    >>> print(payoff.calculate([100., 110., 120., 80., 110.]))
    0.0

    """
    B: float
    barrier_updown: (str, BarrierUpDown)
    barrier_inout: (str, BarrierInOut)

    def __init__(self, option_right: (str, OptionRight), K: float, B: float,
                 barrier_updown: (str, BarrierUpDown),
                 barrier_inout: (str, BarrierInOut)):
        super().__init__(K, option_right)
        self.B = B
        self.barrier_updown = barrier_updown
        self.barrier_inout = barrier_inout

    @property
    def barrier_updown(self) -> BarrierUpDown:
        """Up or down type barrier option."""
        return self._barrier_updown

    @barrier_updown.setter
    def barrier_updown(self, val: (str, BarrierUpDown)) -> None:
        """Set either up or down type barrier option."""
        if isinstance(val, str):
            if not hasattr(BarrierUpDown, val):
                or_names = [x.name for x in BarrierUpDown]
                raise ValueError(f'Invalid str {val}, expected {or_names}')
            self._barrier_updown = BarrierUpDown[val]
        elif isinstance(val, BarrierUpDown):
            self._barrier_updown = val
        else:
            raise TypeError(
                f'Expected str or BarrierUpDown, instead got type {type(val)}!'
            )

    @property
    def barrier_inout(self) -> BarrierInOut:
        """Up or down type barrier option."""
        return self._barrier_inout

    @barrier_inout.setter
    def barrier_inout(self, val: (str, BarrierInOut)) -> None:
        """Set either up or down type barrier option."""
        if isinstance(val, str):
            if not hasattr(BarrierInOut, val):
                or_names = [x.name for x in BarrierInOut]
                raise ValueError(f'Invalid str {val}, expected {or_names}')
            self._barrier_inout = BarrierInOut[val]
        elif isinstance(val, BarrierInOut):
            self._barrier_inout = val
        else:
            raise TypeError(
                f'Expected str or BarrierInOut, instead got type {type(val)}!'
            )

    def calculate(self, S: List[float]) -> float:
        """
        Calulate the payoff given a set of prices for the underlying.

        Parameters
        ----------
        S : Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Returns
        ----------
        payoff : Payoff.

        """
        # Calculate the heavyside
        if self.barrier_updown == BarrierUpDown.Up:
            H = [1 if self.B - x > 0 else 0 for x in S]
        else:
            H = [1 if x - self.B > 0 else 0 for x in S]

        # Calculate whether it has been activated
        if self.barrier_inout == BarrierInOut.In:
            activation = 1 if min(H) == 0 else 0
        else:
            activation = min(H)

        # Calculate payoff using final price
        if self.option_right == OptionRight.Call:
            payoff = activation * self._calculate_call(S[-1])
        else:
            payoff = activation * self._calculate_put(S[-1])
        return payoff
