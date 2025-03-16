"""This is the spinner_proc.py module.

This code is from Chapter 19 of Fluent Pytho by Luciano Ramalho.

It provides basic functions to demonstrate how concurrency works in python.
Same as spinner_thread.py, but using the multiprocessing module instead of
threading. The multiprocessing package supports running concurrent tasks in
separate processes intead of threads.

When you create a multiprocessing.Process, instance, whole new Python
interpreter is started as a child process in the background. Since each Python
prcoess has its own GIL, this allows your program to use all available CPU
cores.
"""

import itertools
import time
from multiprocessing import Event, Process, synchronize


# Unchanged from spinner_thread.py
def spin(msg: str, done: synchronize.Event) -> None:
    """Display a spinner while waiting for a task to complete."""
    for char in itertools.cycle('\\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)

        # The Event.wait(timeout=None) method returns True when the event is
        # set by another thread; if the timeout elapses, it returns False. The
        # .1s timeout sets the "frame rate" of the animation to 10FPS. If you
        # want the spinner to go faster, use a smaller timeout.
        if done.wait(0.1):
            break

        # Clear the status line by overwriting with spaces and moving the
        # cursor back to the beginning.
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')


# Unchanged from spinner_thread.py
def slow() -> int:
    """Simulate a slow task."""
    time.sleep(3)
    return 42


def supervisor() -> int:
    """Run a slow task with a spinner."""
    done = Event()
    spinner = Process(target=spin, args=('thinking...', done))
    print(f'spinner object: {spinner}')
    spinner.start()  # Start the spinner process
    result = slow()  # Call the slow function (this blocks the main process)
    done.set()  # Sets the Event flag to True, signaling the spinner to exit.
    spinner.join()  # Wait for the spinner process to exit
    return result  # Return the result of the slow function


def main() -> None:
    """Main function to demonstrate the spinner with a slow task."""
    result = supervisor()
    print(f'\nAnswer: {result}')


if __name__ == '__main__':
    main()
