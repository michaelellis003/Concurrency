"""Check if numbers are prime concurrently.

This code is from Chapter 20 of Fluent Python, 2nd Edition by Luciano Ramalho.

Rewrite procs.py using ProcessPoolExecutor. Using concurrent.futures means
we do not need to us multiprocessing, SimpleQueue, etc. concurrent.futures
hides all that from us.
"""

import sys
from concurrent import futures
from time import perf_counter
from typing import NamedTuple

from primes import NUMBERS, is_prime


class PrimeResult(NamedTuple):
    """A named tuple to store the result of a prime check."""

    n: int
    flag: bool
    elapsed: float


def check(n: int) -> PrimeResult:
    """Check if a number is prime and return the result with elapsed time.

    Args:
        n (int): The number to check for primality.

    Returns:
        PrimeResult: A named tuple containing the number, a boolean indicating
            if it is prime, and the elapsed time.
    """
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def main() -> None:
    """Function to check if numbers are prime using ProcessPoolExecutor."""
    workers = None if len(sys.argv) < 2 else int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers  # type: ignore

    print(f'Checking {len(NUMBERS)} with {actual_workers} processess:')

    t0 = perf_counter()
    numbers = sorted(NUMBERS, reverse=True)
    with executor:
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')


if __name__ == '__main__':
    main()
