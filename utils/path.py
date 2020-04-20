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
from typing import List, Sequence, Tuple

from utils.misc import Number


__all__ = ['PathGenerator']


@dataclass
class PathGenerator:
    """
    Class for generating underlying prices using MC techniques.

    Attributes
    ----------
    S : Number
        Spot price.
    r : Number
        Risk-free interest rate.
    div : Number
        Dividend yield.
    vol : Number
        Volatility.
    net_r

    Methods
    -------
    generate(T)
        Generate a random path {S_t1, S_t2, ..., S_tn}.
    generate_antithetic(T)
        Generate a random plus antithetic path
        [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

    Examples
    --------
    >>> from utils.path import PathGenerator
    >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
    >>> print(path)
    PathGenerator(S=100.0, r=0.1, div=0.01, vol=0.3)

    """
    __slots__ = 'S', 'r', 'div', 'vol'
    S: Number
    r: Number
    div: Number
    vol: Number

    @property
    def net_r(self) -> float:
        """Net risk free rate."""
        return float(self.r - self.div)

    def generate(self, T: Sequence[Number]) -> List[float]:
        """
        Generate a random path {S_t1, S_t2, ..., S_tn}.

        Parameters
        ----------
        T : Sequence of Numbers
            Set of times {t1, t2, ..., tn} in years.

        Returns
        -------
        spot_prices : List of floats
            Set of prices for the underlying {S_t1, S_t2, ..., S_tn}.

        Examples
        --------
        >>> from utils.path import PathGenerator
        >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
        >>> print(path.generate(T=range(4)))
        [100.0, 100.33539853588853, 122.76017088387074, 142.29540684005462]
        >>> print(path.generate(T=range(4)))
        [100.0, 73.03094019139712, 77.37310245438943, 66.54240939439934]

        """
        # Calculate dt time differences
        dts = [T[idx + 1] - T[idx] for idx in range(len(T) - 1)]

        spot_prices: List[float] = [0] * len(T)
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

    def generate_antithetic(
            self, T: Sequence[Number]
    ) -> Tuple[List[float], List[float]]:
        """
        Generate a random plus antithetic path
        [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

        Parameters
        ----------
        T : Sequence of Numbers
            Set of times {t1, t2, ..., tn} in years.

        Returns
        -------
        prices_tuple : Tuple of two Lists of floats
            Set of prices for the underlying
            [{S_t1, S_t2, ..., S_tn}, {S'_t1, S'_t2, ..., S'_tn}].

        Examples
        --------
        >>> from utils.path import PathGenerator
        >>> path = PathGenerator(S=100., r=0.1, div=0.01, vol=0.3)
        >>> print(path.generate_antithetic(T=range(4)))
        ([100.0, 106.30304144532359, 122.02501765852367, 108.71120035365013],
         [100.0, 102.92972513566257, 98.11245153613649, 120.49949282794978])
        >>> print(path.generate_antithetic(T=range(4)))
        ([100.0, 130.1595970941697, 103.35241529329348, 93.58800177914543],
         [100.0, 84.06404968460234, 115.83835362960282, 139.97140935058962])

        """
        # Calculate dt time differences
        dts = [T[idx + 1] - T[idx] for idx in range(len(T) - 1)]

        # Create data structures
        spot_prices: List[float] = [0] * len(T)
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
