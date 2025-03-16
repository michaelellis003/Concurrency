"""Sequentially download flags with error handling.

Code from Chapter 20 of Fluent Python, 2nd Edition by Lucianp Ramalho
"""

from collections import Counter
from http import HTTPStatus

import httpx
import tqdm
from flags2_common import DownloadStatus, main, save_flag

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


def get_flag(base_url: str, cc: str) -> bytes:
    """Download a flag image from the given base URL and country code."""
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content


def download_one(
    cc: str, base_url: str, verbose: bool = False
) -> DownloadStatus:
    """Download a flag image for a given country code and save it.

    Args:
        cc (str): Country code.
        base_url (str): Base URL for downloading flags.
        verbose (bool): If True, print status messages.

    Returns:
        Downloadstatus: Status of the download.
    """
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return status


def download_many(
    cc_list: list[str], base_url: str, verbose: bool, _unused_concur_req: int
) -> Counter[DownloadStatus]:
    """Download multiple flag images and count the outcomes.

    Args:
        cc_list (list[str]): List of country codes.
        base_url (str): Base URL for downloading flags.
        verbose (bool): If True, print status messages.
        _unused_concur_req (int): Unused concurrency request parameter.

    Returns:
        Counter[DownloadStatus]: Counter of download statuses.
    """
    # Count different download outcomes
    counter: Counter[DownloadStatus] = Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose)
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR
        counter[status] += 1  # type: ignore
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
