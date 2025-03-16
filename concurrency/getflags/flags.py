"""Script to sequentially download images of flags.

This code is from Chapter 20 of Fluent Python, 2nd Edition by Luciano Ramalho.
"""

import time
from collections.abc import Callable
from pathlib import Path

import httpx

POP20_CC = [
    'CN',
    'IN',
    'US',
    'ID',
    'BR',
    'PK',
    'NG',
    'BD',
    'RU',
    'JP',
    'MX',
    'PH',
    'VN',
    'ET',
    'EG',
    'DE',
    'IR',
    'TR',
    'CD',
    'FR',
]

BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('downloaded')


def save_flag(img: bytes, filename: str) -> None:
    """Save the the img bytes to filename in DEST_DIR.

    Args:
        img (bytes): The binary contents of the image.
        filename (str): The name to save the image as (e.g., 'CN.gif').

    Returns:
        None
    """
    (DEST_DIR / filename).write_bytes(img)


def get_flag(cc: str) -> bytes:
    """Download the flag image for the given country code.

    Given a country code, build the URL and download the image, returning the
    binary contents of the response.

    Args:
        cc (str): The country code (e.g., 'CN' for China).

    Returns:
        bytes: The binary contents of the flag image.
    """
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, follow_redirects=True)
    resp.raise_for_status()  # Raise an error for bad responses
    return resp.content


def download_any(cc_list: list[str]) -> int:
    """Download flags for a list of country codes.

    Args:
        cc_list (list[str]): A list of country codes (e.g., ['CN', 'US']).

    Returns:
        int: The number of flags successfully downloaded.
    """
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True)

    return len(cc_list)


def main(downloader: Callable[[list[str]], int]) -> None:
    """Main function to download flags and measure time taken.

    Args:
        downloader (Callable[[list[str]], int]): The function to download flags

    Returns:
        None
    """
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\nDownloaded {count} flags in {elapsed:.2f} seconds.')


if __name__ == '__main__':
    main(download_any)  # Sequential download of flags
