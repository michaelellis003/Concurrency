"""This module provides a concurrent primality test for a list of numbers.

This code is from Chapter 19 of Fluent Python, 2nd Edition by Luciano Ramalho.
This code uses multiprocessing to start a number of worker prcoesses qual to
the number of CPU codes, as determined by multiprocessing.cpu_count(). The
total time in this case is much less then the sum of the elasped time for
the code in sequential.py. There is some overhead in spinning up processes and
in inter-process communication.
"""

import sys
from multiprocessing import Process, SimpleQueue, cpu_count, queues
from time import perf_counter
from typing import NamedTuple

from primes import NUMBERS, is_prime


class PrimeResult(NamedTuple):
    """A named tuple to store the result of the primality test."""

    n: int
    prime: bool
    elapsed: float


# Type alias for a SimpleQueue that the main function will use to send numbers
# to the processes that will do the work
JobQueue = queues.SimpleQueue[int]

# Type alias for a second SimpleQueue that will collect the results in main,
ResultQueue = queues.SimpleQueue[PrimeResult]


def check(n: int) -> PrimeResult:
    """Check if a number is prime and measure the time taken."""
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


# Worker gets a queue with the numbers to be checked, and another to put
# results
def worker(jobs: JobQueue, results: ResultQueue) -> None:
    """Worker function to process numbers from the job queue."""
    # I use the number 0 as a poison pill: a signal for the worker to finish.
    # If n is not 0, proceed with the loop.
    while n := jobs.get():
        results.put(check(n))  # Invoke check and enqueue PrimeResult

    # Send back PrimeResult(0, False, 0.0) to let the main loop know that this
    # worker is done.
    results.put(PrimeResult(0, False, 0.0))


def start_jobs(procs: int, jobs: JobQueue, results: ResultQueue) -> None:
    """Start worker processes and return a list of Process objects."""
    for n in NUMBERS:
        jobs.put(n)  # Enqueue the number to be checked in jobs
    for _ in range(procs):
        # Fork a child prcoess for each worker. Each child will run the loop
        # inside its own instance of the worker function, until it fetches a 0
        # from the jobs queue.
        proc = Process(target=worker, args=(jobs, results))
        proc.start()  # start each child process
        jobs.put(0)  # Enqueue one 0 for each process, to terminate them.


def main() -> None:
    """Main function to check primality of numbers in the NUMBERS list."""
    # If no command line argument, set the number of prcoesses to the number
    # of CPU cores. Otherwise, create as many processes as given in the first
    # command line argument.
    procs = cpu_count() if len(sys.argv) < 2 else int(sys.argv[1])
    if procs is None:
        raise ValueError('Number of processes cannot be None')
    print(
        f'Checking {len(NUMBERS)} numbers for primality using {procs} \
          processes...'
    )

    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()  # Create a queue for the jobs
    results: ResultQueue = SimpleQueue()  # Create a queue for the results
    start_jobs(procs, jobs, results)  # Start the worker processes
    checked = report(procs, results)  # Report the results
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')


def report(procs: int, results: ResultQueue) -> int:
    """Report the results of the primality tests."""
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        if n == 0:  # Check for the poison pill
            procs_done += 1
            continue
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16} {label} {elapsed:9.6f}s')
    return checked


if __name__ == '__main__':
    main()
