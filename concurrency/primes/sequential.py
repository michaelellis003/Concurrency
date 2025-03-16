"""Sequential primality test for a list of numbers.

This code is from Chapter 19 of Fluent Python, 2nd Edition by Luciano Ramalho.
"""

from time import perf_counter
from typing import NamedTuple

from primes import NUMBERS, is_prime


class Result(NamedTuple):
    """A named tuple to store the result of the primality test."""

    prime: bool
    elapsed: float


def check(n: int) -> Result:
    """Check if a number is prime and measure the time taken."""
    start = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() - start)


def main() -> None:
    """Main function to check primality of numbers in the NUMBERS list."""
    print(f'Checking {len(NUMBERS)} numbers for primality...')
    t0 = perf_counter()
    for n in NUMBERS:
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16} {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:9.6f}s')


if __name__ == '__main__':
    main()
