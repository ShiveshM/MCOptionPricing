# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Pricing engine for exotic options.
"""

import math
from statistics import mean, stdev
from dataclasses import dataclass
from typing import List, Sequence

from utils.misc import Number
from utils.path import PathGenerator
from utils.payoff import BasePayoff


__all__ = ['MCResult', 'PricingEngine']


@dataclass
class MCResult:
    """
    Price of option along with its MC error.

    Attributes
    ----------
    price : float
        Spot Price.
    path : float
        MC standard error.

    """
    price: float
    stderr: float


@dataclass
class PricingEngine:
    """
    Class for generating underlying prices using MC techniques.

    Attributes
    ----------
    payoff : BasePayoff
        Payoff object for calculating the options payoff.
    path : PathGenerator
        PathGenerator object for generating the evolution of the underlying.

    Methods
    -------
    price()
        Price the option using MC techniques.

    Examples
    --------
    >>> from utils.engine import PricingEngine
    >>> from utils.path import PathGenerator
    >>> from utils.payoff import AsianArithmeticPayOff
    >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
    >>> payoff = AsianArithmeticPayOff(option_right='Call', K=110)
    >>> engine = PricingEngine(payoff=payoff, path=path)
    >>> print(engine)
    PricingEngine(payoff=AsianArithmeticPayOff(K=110, option_right=Call),
                  path=PathGenerator(S=100.0, r=0.1, div=0.01, vol=0.3))

    """
    payoff: BasePayoff
    path: PathGenerator

    def price(
            self,
            T: Sequence[Number],
            ntrials: int = 10_000,
            antithetic: bool = True
    ) -> MCResult:
        """
        Price the option using MC techniques.

        Parameters
        ----------
        T : Sequence of Numbers
            Set of times {t1, t2, ..., tn} in years.
        ntrials : int
            Number of trials to simulate.
        antithetic : bool
            Use antithetic variates technique.

        Returns
        -------
        MCResult
            Price of the option.

        Examples
        --------
        >>> from utils.engine import PricingEngine
        >>> from utils.path import PathGenerator
        >>> from utils.payoff import AsianArithmeticPayOff
        >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
        >>> payoff = AsianArithmeticPayOff(option_right='Call', K=110)
        >>> engine = PricingEngine(payoff=payoff, path=path)
        >>> print(engine.price(T=range(4)))
        MCResult(price=12.003704847790525, stderr=0.2327352760696234)

        """
        if ntrials < len(T):
            raise AssertionError('Number of trials cannot be less than the '
                                 'number of setting dates!')

        # Generation start
        ntrials = int(ntrials // len(T))
        payoffs: List[float] = [0] * ntrials
        for idx in range(ntrials):
            # Generate a random path
            if not antithetic:
                spot_prices = self.path.generate(T)
            else:
                prices_tuple = self.path.generate_antithetic(T)
                spot_prices, a_spot_prices = prices_tuple

            # Calculate the payoff
            payoff = self.payoff.calculate(spot_prices)
            if antithetic:
                a_po = self.payoff.calculate(a_spot_prices)
                payoff = (payoff + a_po) / 2
            payoffs[idx] = payoff

        # Discount to current time
        df = math.exp(-self.path.net_r * (T[-1] - T[0]))
        dis_payoffs = [x * df for x in payoffs]

        # Payoff expectation and standard error
        exp_payoff = mean(dis_payoffs)
        stderr = stdev(dis_payoffs, exp_payoff) / math.sqrt(ntrials)

        return MCResult(exp_payoff, stderr)
