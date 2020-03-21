# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020

"""
Path generator for underlying.
"""

import math
import random
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple


__all__ = ['PathGenerator']


@dataclass
class PathGenerator:
    """
    Class for generating underlying prices using MC techniques.

    Attributes
    ----------
    S : Spot price.
    r : Risk-free interest rate.
    div : Dividend yield.
    vol : Volatility.
    net_r : Net risk free rate.

    Methods
    ----------
    generate(T)
        Generate a random path {S_t1, S_t2, ..., S_tn}.
    generate_antithetic(T)
        Generate a random plus antithetic path
        [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

    Examples
    ----------
    >>> from utils.path import PathGenerator
    >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
    >>> print(path.generate(T=range(4)))
    [100.0, 91.11981160354563, 94.87596210593794, 117.44132223235353]
    >>> print(path.generate(T=range(4)))
    [100.0, 68.73668230722738, 71.43490333826567, 70.70833180133955]

    """
    S: float
    r: float
    div: float
    vol: float

    @property
    def net_r(self) -> float:
        """Net risk free rate."""
        return self.r - self.div

    def generate(self, T: List[float]) -> List[float]:
        """
        Generate a random path {S_t1, S_t2, ..., S_tn}.

        Parameters
        ----------
        T : Set of times {t1, t2, ..., tn} in years.

        Returns
        ----------
        spot_prices : Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        """
        # Calculate dt time differences
        dts = [T[idx + 1] - T[idx] for idx in range(len(T) - 1)]

        spot_prices = [0] * len(T)
        spot_prices[0] = self.S
        for idx, dt in enumerate(dts):
            # Calculate the drift e^{(r - (1/2) σ²) Δt}
            drift = math.exp((self.net_r - (1/2) * self.vol**2) * dt)

            # Calculate the volatility term e^{σ √{Δt} N(0, 1)}
            rdm_gauss = random.gauss(0, 1)
            vol_term = math.exp(self.vol * math.sqrt(dt) * rdm_gauss)

            # Calculate next spot price
            S_t = spot_prices[idx] * drift * vol_term
            spot_prices[idx + 1] = S_t
        return spot_prices

    def generate_antithetic(self, T: List[float]) -> Tuple[List[float],
                                                           List[float]]:
        """
        Generate a random plus antithetic path
        [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

        Parameters
        ----------
        T : Set of times {t1, t2, ..., tn} in years.

        Returns
        ----------
        prices_tuple : Set of prices for the underlying
                       [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

        """
        # Calculate dt time differences
        dts = [T[idx + 1] - T[idx] for idx in range(len(T) - 1)]

        # Create data structures
        spot_prices = [0] * len(T)
        spot_prices[0] = self.S

        a_spot_prices = deepcopy(spot_prices)

        for idx, dt in enumerate(dts):
            # Calculate the drift e^{(r - (1/2) σ²) Δt}
            drift = math.exp((self.net_r - (1/2) * self.vol**2) * dt)

            # Calculate the volatility term e^{σ √{Δt} N(0, 1)}
            rdm_gauss = random.gauss(0, 1)
            a_gauss = -rdm_gauss
            vol_term = math.exp(self.vol * math.sqrt(dt) * rdm_gauss)
            a_vol_term = math.exp(self.vol * math.sqrt(dt) * a_gauss)

            # Calculate next spot price
            S_t = spot_prices[idx] * drift * vol_term
            a_S_t = a_spot_prices[idx] * drift * a_vol_term

            # Add to data structure
            spot_prices[idx + 1] = S_t
            a_spot_prices[idx + 1] = a_S_t

        return (spot_prices, a_spot_prices)
