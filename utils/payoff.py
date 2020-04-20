# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Payoff of an option.
"""

from abc import ABC, abstractmethod
from typing import AnyStr, List, Union, Sequence

from utils.enums import OptionRight, BarrierUpDown, BarrierInOut
from utils.misc import Number


__all__ = [
    'BasePayoff',
    'VanillaPayOff',
    'AsianArithmeticPayOff',
    'DiscreteBarrierPayOff'
]


class BasePayoff(ABC):
    """Base class for calculating the payoff."""
    __slots__ = 'K', '_option_right'

    def __init__(self, K: Number,
                 option_right: Union[AnyStr, OptionRight]) -> None:
        self.K: Number = K
        # https://github.com/python/mypy/issues/3004
        self.option_right = option_right  # type: ignore

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'K={self.K!r}, '
            f'option_right={self.option_right!r}'
            ')'
        )

    @property
    def option_right(self) -> OptionRight:
        """Right of the option."""
        return self._option_right

    @option_right.setter
    def option_right(self, val: Union[AnyStr, OptionRight]) -> None:
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

    def _calculate_call(self, S: Number) -> float:
        """
        Price call option for a given underlying price.

        Parameters
        ----------
        S : Number
            Price of underlying.

        Returns
        -------
        float
            Price of the call option.

        """
        return float(max(S - self.K, 0.0))

    def _calculate_put(self, S: Number) -> float:
        """
        Price put option for a given underlying price.

        Parameters
        ----------
        S : Number
            Price of underlying.

        Returns
        -------
        float
            Price of the put option.

        """
        return float(max(self.K - S, 0.0))

    @abstractmethod
    def calculate(self, S: Sequence[Number]) -> float:
        """Calulate the payoff for a given path."""


class VanillaPayOff(BasePayoff):
    """
    Class for calculating the payoff of a vanilla option.

    Attributes
    ----------
    option_right : OptionRight
        Right of the option.
    K : Number
        Strike price.

    Methods
    -------
    calculate(S)
        Calulate the payoff for a given path.

    Examples
    --------
    >>> from utils.payoff import VanillaPayOff
    >>> payoff = VanillaPayOff(option_right='Call', K=150.)
    >>> print(payoff)
    VanillaPayOff(K=150.0, option_right=Call)

    """

    def calculate(self, S: Sequence[Number]) -> float:
        """
        Calulate the payoff for a given path.

        Parameters
        ----------
        S : Sequence of Numbers
            Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Returns
        -------
        payoff : float
            Payoff.

        Notes
        -----
        The final entry will be taken to evaluate the payoff.

        Examples
        --------
        >>> from utils.payoff import VanillaPayOff
        >>> payoff = VanillaPayOff(option_right='Call', K=150.)
        >>> print(payoff.calculate([160.]))
        10.0

        """
        # Calculate payoff using final price
        if self.option_right == OptionRight.Call:
            payoff = self._calculate_call(S[-1])
        else:
            payoff = self._calculate_put(S[-1])
        return payoff


class AsianArithmeticPayOff(BasePayoff):
    """
    Class for calculating the payoff of an arithmetic Asian option.

    Attributes
    ----------
    option_right : OptionRight
        Right of the option.
    K : Number
        Strike price.

    Methods
    -------
    calculate(S)
        Calulate the payoff given a set of prices for the underlying.

    Examples
    --------
    >>> from utils.payoff import AsianArithmeticPayOff
    >>> payoff = AsianArithmeticPayOff(option_right='Call', K=150)
    >>> print(payoff)
    AsianArithmeticPayOff(K=150, option_right=Call)

    """

    def calculate(self, S: Sequence[Number]) -> float:
        """
        Calulate the payoff given a set of prices for the underlying.

        Parameters
        ----------
        S : Sequence of Numbers
            Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Returns
        -------
        payoff : float
            Payoff.

        Examples
        --------
        >>> from utils.payoff import AsianArithmeticPayOff
        >>> payoff = AsianArithmeticPayOff(option_right='Call', K=150)
        >>> print(payoff.calculate([140, 150, 160, 170, 180]))
        10.0

        """
        avg_sum = sum(S) / len(S)
        if self.option_right == OptionRight.Call:
            payoff = self._calculate_call(avg_sum)
        else:
            payoff = self._calculate_put(avg_sum)
        return payoff


class DiscreteBarrierPayOff(BasePayoff):
    """
    Class for calculating the payoff of a discrete barrier European style
    option.

    Attributes
    ----------
    option_right : OptionRight
        Right of the option.
    K : Number
        Strike price.
    B : Number
        Barrier price.
    barrier_updown : BarrierUpDown
        Up or down type barrier option.
    barrier_inout : BarrierInOut
        In or out type barrier option.

    Methods
    -------
    calculate(S)
        Calulate the payoff given a set of prices for the underlying.

    Examples
    --------
    >>> from utils.payoff import DiscreteBarrierPayOff
    >>> payoff = DiscreteBarrierPayOff(option_right='Call', K=100, B=90, \
                                       barrier_updown='Down', barrier_inout='Out')
    >>> print(payoff)
    DiscreteBarrierPayOff(K=100, option_right=Call, B=90, barrier_updown=Down, barrier_inout=Out)

    """
    __slots__ = 'K', '_option_right', 'B', '_barrier_updown', '_barrier_inout'

    def __init__(
            self,
            K: Number,
            option_right: Union[AnyStr, OptionRight],
            B: Number,
            barrier_updown: Union[AnyStr, BarrierUpDown],
            barrier_inout: Union[AnyStr, BarrierInOut]
    ) -> None:
        super().__init__(K, option_right)
        self.B: Number = B
        # https://github.com/python/mypy/issues/3004
        self.barrier_updown = barrier_updown  # type: ignore
        self.barrier_inout = barrier_inout  # type: ignore

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'K={self.K!r}, '
            f'option_right={self.option_right!r}, '
            f'B={self.B!r}, '
            f'barrier_updown={self.barrier_updown!r}, '
            f'barrier_inout={self.barrier_inout!r}'
            ')'
        )

    @property
    def barrier_updown(self) -> BarrierUpDown:
        """Up or down type barrier option."""
        return self._barrier_updown

    @barrier_updown.setter
    def barrier_updown(self, val: Union[AnyStr, BarrierUpDown]) -> None:
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
    def barrier_inout(self, val: Union[AnyStr, BarrierInOut]) -> None:
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

    def calculate(self, S: Sequence[Number]) -> float:
        """
        Calulate the payoff given a set of prices for the underlying.

        Parameters
        ----------
        S : Sequence of Numbers
            Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Returns
        -------
        payoff : float
            Payoff.

        Examples
        --------
        >>> from utils.payoff import DiscreteBarrierPayOff
        >>> payoff = DiscreteBarrierPayOff(option_right='Call', K=100, B=90, \
                                           barrier_updown='Down', barrier_inout='Out')
        >>> print(payoff.calculate([100., 110., 120.]))
        20.0
        >>> print(payoff.calculate([100., 110., 120., 80., 110.]))
        0.0

        """
        # Calculate the heavyside
        H: List[int]
        if self.barrier_updown == BarrierUpDown.Up:
            H = [1 if self.B - x > 0 else 0 for x in S]
        else:
            H = [1 if x - self.B > 0 else 0 for x in S]

        # Calculate whether it has been activated
        activation: int
        if self.barrier_inout == BarrierInOut.In:
            activation = 1 if min(H) == 0 else 0
        else:
            activation = min(H)

        # Calculate payoff using final price
        payoff: float
        if self.option_right == OptionRight.Call:
            payoff = activation * self._calculate_call(S[-1])
        else:
            payoff = activation * self._calculate_put(S[-1])
        return payoff
