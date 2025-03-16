"""This is the spinner_async.py module.

This code is from Chapter 19 of Fluent Pytho by Luciano Ramalho.

It provides basic functions to demonstrate how concurrency works in python.
Same as spinner_thread.py and spinner_proc, but using the aysyncio instead of
threading or multiprocessing.
"""

import asyncio
import itertools


async def spin(msg: str) -> None:
    """Display a spinner while waiting for a task to complete."""
    for char in itertools.cycle('\\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)

        try:
            # Use await asynci.sleep(0.1) instead of time.sleep(0.1) to
            # pause without blocking the other coroutines.
            await asyncio.sleep(0.1)

        # asyncio.CancelledError is raised when the cancel method is called
        # on the Task controlling this coroutine.
        except asyncio.CancelledError:
            break
        # Clear the status line by overwriting with spaces and moving the
        # cursor back to the beginning.
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


async def slow() -> int:
    """Simulate a slow task with a 3-second delay and return a result."""
    await asyncio.sleep(3)  # Simulate a slow task with a 3-second delay
    return 42  # Return the result of the slow function


async def supervisor() -> int:
    """Supervises the spinner task. Waits for the slow function to return."""
    # asyncio.create_task() schedules the eventual execution of spin,
    # immediately returning an instasnce of asyncio.Task.
    spinner = asyncio.create_task(
        spin('thinking...')
    )  # Start the spinner task
    print(f'spinner object: {spinner}')
    # Call the slow function (blocking supervisor until slow returns)
    result = await slow()

    # The task.cancel method raises a CancelledError exception inside the spin
    # coroutine.
    spinner.cancel()  # Cancel the spinner task
    return result


def main() -> None:
    """Main function to demonstrate the spinner with a slow task."""
    # The asyncio.run() function starts the event loop to drive the coroutine
    # that will eventually set the other coroutines in motion. The main
    # function will stay blocked until the supervisor() returns. The return
    # value of the supervisor().
    result = asyncio.run(supervisor())
    print(f'\nAnswer: {result}')


if __name__ == '__main__':
    main()
