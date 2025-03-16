"""Script to concurrently download images of flags using concurrent.futures.

This code is from Chapter 20 of Fluent Python, 2nd Edition by Luciano Ramalho.

This  scripts uses ThreadPoolExecutor from concurrent.futures to submit
callables that download flag images for execution in different threads. The
class transparently manages a pool of worker threads, and queues to distribute
jobs and collect results.
"""

from concurrent import futures

from flags import get_flag, main, save_flag


def download_one(cc: str):
    """Download a single images; this is what each worker will execute.

    Args:
        cc (str): The country code (e.g., 'CN' for China).

    Returns:
        str: The country code of the downloaded image.
    """
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc


def download_many(cc_list: list[str]) -> int:
    """Download images concurrently."""
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    main(download_many)
