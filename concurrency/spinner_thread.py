"""This is the spinner_thread.py module.

This code is from Chapter 19 of Fluent Pytho by Luciano Ramalho.

It provides basic functions to demonstrate how concurrency works in python
"""

import itertools
import time
from threading import Event, Thread


# This function will run in a separate thread. The done arguement is an
# instance of threading.Event, a simple object to synchronize threads.
def spin(msg: str, done: Event) -> None:
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


# slow() will be called by main thread. Imagine this is a slow API call over
# the network. Calling sleep blocks the main thread, but the GIL is released
# so the spinner thread can proceed.
def slow() -> int:
    """Simulate a slow task."""
    time.sleep(3)
    return 42


# The spin() and slow() functions will execute concurrently. The main thread -
# the only thread when the program starts - will start a new thread to run
# spin() while it runs slow(). The supervisor() function uses an Event to
# signal the spin function to exit.
def supervisor() -> int:
    """Run a slow task with a spinner."""
    # The threading.Event instance is the key to coordinate the activities of
    # the main thread and the spinner thread.
    done = Event()

    # To create a new Thread, provide a function as the target keyword argument
    # and positional arguments to the target as a tuple passed via args.
    spinner = Thread(target=spin, args=('thinking...', done))

    print(f'spinner object: {spinner}')
    spinner.start()  # Start the spinner thread

    # Call the slow function (this blocks the main thread). Meanwhile, the
    # secondary thread runs the spinner function.
    result = slow()
    done.set()  # Sets the Event flag to True, signaling the spinner to exit.
    spinner.join()  # Wait for the spinner to finish
    return result  # Return the result of the slow task


def main() -> None:
    """Main function to demonstrate the spinner with a slow task."""
    result = supervisor()
    print(f'\nAnswer: {result}')


if __name__ == '__main__':
    main()
