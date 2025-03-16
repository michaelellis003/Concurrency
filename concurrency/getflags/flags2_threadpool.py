"""Concurrently download flags with error handling using futures.

Code from Chapter 20 of Fluent Python, 2nd Edition by Lucianp Ramalho
"""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tqdm
from flags2_common import DownloadStatus, main
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


def download_many(
    cc_list: list[str], base_url: str, verbose: bool, concur_req: int
) -> Counter[DownloadStatus]:
    """Download flags concurrently using a thread pool.

    Args:
        cc_list (list[str]): List of country codes.
        base_url (str): Base URL for downloading flags.
        verbose (bool): If True, print progress and error messages.
        concur_req (int): Number of concurrent requests.

    Returns:
        Counter[DownloadStatus]: Counter of download statuses.
    """
    counter: Counter[DownloadStatus] = Counter()
    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            # Each call to executor.submit schedules the execution of one
            # callable and returns a Future instance.
            future = executor.submit(download_one, cc, base_url, verbose)

            # Store the future and the country code in the dict
            to_do_map[future] = [cc]

        # futures.as_completed returns an iterator that yields futures as each
        # task is done
        done_iter = as_completed(to_do_map)

        if not verbose:
            # done_iter has no len method so we must pass value to total
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))

        # Iterate over futures as they completed
        for future in done_iter:
            try:
                # returns the value returned by the callable or raises
                # whatever exception was caught when the callable was executed
                status = future.result()
            except httpx.HTTPStatusError as exc:
                error_msg = (
                    'HTTP error {resp.status_code} - {resp.reason_phrase}'
                )
                error_msg = error_msg.format(resp=exc.response)
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
            except KeyboardInterrupt:
                break
            else:
                error_msg = ''

        if error_msg:  # type: ignore
            status = DownloadStatus.ERROR
        counter[status] += 1  # type: ignore
        if verbose and error_msg:  # type: ignore
            cc = to_do_map[future]  # type: ignore # <14>
            print(f'{cc} error: {error_msg}')

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
