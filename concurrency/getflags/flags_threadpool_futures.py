"""Script to concurrently download images of flags using concurrent.futures.

This code is from Chapter 20 of Fluent Python, 2nd Edition by Luciano Ramalho.

Essentially the same code as flags_threadpool.py but with a more detailed look
at how the Future class works. The Future class represents a deferred
computation that may or may not have completed. Futures encapsulate pending
operations so that we can put them in queues, check whether they are done, and
retrieve results when they become avaiable.
"""

from concurrent import futures

from flags import main
from flags_threadpool import download_one


def download_many(cc_list: list[str]) -> int:
    """Download images concurrently.

    Args:
        cc_list (str): List of country flags to download

    Returns:
        int: count of downloaded flags.
    """
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            # executor.submit schedules the callable to be executed and returns
            # a future representing this pending operation
            future = executor.submit(download_one, cc)

            # Store each future so we can later retrieve them with as_completed
            to_do.append(future)
            print(f'Scheduled for {cc}: {future}')

    # futures.as_completed yeilds futures as they are completed
    for count, future in enumerate(futures.as_completed(to_do), 1):  # noqa: B007
        res: str = future.result()
        print(f'{future} result: {res!r}')

    return count  # type: ignore


if __name__ == '__main__':
    main(download_many)
