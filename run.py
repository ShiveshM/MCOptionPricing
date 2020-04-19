#! /usr/bin/env python3
# author : S. Mandalia
#          shivesh.mandalia@outlook.com
#
# date   : March 19, 2020


"""
Exotic options by Monte Carlo.

B.7 Project 5 from Mark Joshi's "The Concepts and practice of mathematical
finance", published by Cambridge University Press.

"""

import random
from typing import List

from utils.engine import PricingEngine
from utils.path import PathGenerator
from utils.payoff import AsianArithmeticPayOff, DiscreteBarrierPayOff
from utils.payoff import VanillaPayOff


__all__ = ['asian_options', 'discrete_barrier']


def asian_options(ntrials_arr: List[int]) -> None:
    """Pricing Asian options."""
    # Having implemented the engine, price the following with
    # S0=100, σ=0.1, r=0.05, d=0.03, and strike=103
    print('==================')
    print('Pricing Asian options')
    print('==================')

    path = PathGenerator(S=100, r=0.05, div=0.03, vol=0.1)
    payoff = AsianArithmeticPayOff(K=103, option_right='Call')
    engine = PricingEngine(payoff=payoff, path=path)

    # (i) an Asian call option with maturity in one year and monthly setting
    #     dates.
    T = [x / 12 for x in range(12 + 1)]

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(i) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # (ii) an Asian call option with maturity in one year and three month
    #      setting dates.
    T = [x / 4 for x in range(4 + 1)]

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(ii) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # (iii) an Asian call option with maturity in one year and weekly setting
    #       dates.
    T = [x / 52 for x in range(52 + 1)]

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(iii) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    print('''How do the prices compare?
We see that Asian options with more frequent setting dates are more expensive.
This is because the averaging is less pronounced with more setting dates,
making the Asian option more volatile.''')
    print('==================')

    # Vanilla option
    T = [0, 1]
    engine.payoff = VanillaPayOff(K=103, option_right='Call')

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(vanilla) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    print('''How do the prices compare with a vanilla option?
We see that Asian options are cheaper than vanilla options.
This is because Asian options are less volatile, due to the averaging feature -
the volatility of the averaged price is less volatile than the spot price.''')
    print('==================')

    print('''How does the speed of convergence vary?
The rate of convergence is faster for sparser date settings, as seen by the
standard error. More dense date settings converge slower as the timing
evolution needs to be simulated. For the same reason, vanilla options converge
the fastest.''')


def discrete_barrier(ntrials_arr: List[int]) -> None:
    """Pricing discrete barrier options."""
    # Price some discrete barrier options, all with maturity one year and
    # struck at 103.
    print('==================')
    print('Pricing discrete barrier options')
    print('==================')

    path = PathGenerator(S=100, r=0.05, div=0.03, vol=0.1)

    # (i) a down-and-out call with barrier at 80 and monthly barrier dates.
    payoff = DiscreteBarrierPayOff(
        K=103, option_right='Call', B=80, barrier_updown='Down',
        barrier_inout='Out'
    )
    engine = PricingEngine(payoff=payoff, path=path)
    T = [x / 12 for x in range(12 + 1)]

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(i) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # (ii) a down-and-in call with barrier at 80 and monthly barrier dates.
    engine.path = PathGenerator(S=84, r=0.05, div=0.03, vol=0.1)
    engine.payoff = DiscreteBarrierPayOff(
        K=103, option_right='Call', B=80, barrier_updown='Down',
        barrier_inout='In'
    )

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(ii) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # (iii) a down-and-out put with barrier at 80 and monthly barrier dates.
    engine.path = path
    engine.payoff = DiscreteBarrierPayOff(
        K=103, option_right='Put', B=80, barrier_updown='Down',
        barrier_inout='Out'
    )

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(iii) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # (iv) a down-and-out put with barrier at 120 and barrier dates at
    # 0.05, 0.15, ..., 0.95
    engine.payoff = DiscreteBarrierPayOff(
        K=103, option_right='Put', B=120, barrier_updown='Down',
        barrier_inout='Out'
    )
    T = [x / 20 for x in range(20)]

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(iv) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # Vanilla call option
    T = [0, 1]
    engine.payoff = VanillaPayOff(K=103, option_right='Call')

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(vanilla call) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    # Vanilla put option
    T = [0, 1]
    engine.payoff = VanillaPayOff(K=103, option_right='Put')

    # Price
    for ntrials in ntrials_arr:
        result = engine.price(T=T, ntrials=ntrials)
        print('(vanilla put) = {0:.4f} +- {1:.4f} with {2} trials'.format(
            result.price, result.stderr, int(ntrials)
        ))
    print('==================')

    print('''Compare prices and speed of convergence. Also compare prices with
the vanilla option.
Similar to Asian options, the rate of convergence is faster for sparser date
settings. Vanilla options converge the fastest.
Discrete barrier options can be much cheaper than vanilla options. This is
because these type of options offer less flexibility compared to vanilla
options, and thus this is priced in.''')


def main() -> None:
    random.seed(1)

    # Define number of trials to run
    ntrials_arr = list(map(int, [1e4, 1e5, 1e6]))

    # Pricing Asian options
    asian_options(ntrials_arr)

    # Pricing discrete barrier options
    discrete_barrier(ntrials_arr)

    print('==================')
    print('Shivesh Mandalia https://shivesh.org/')
    print('==================')


main.__doc__ = __doc__


if __name__ == '__main__':
    main()
