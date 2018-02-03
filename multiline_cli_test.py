#!/usr/bin/env python3
"""
Multithreaded multiline CLI output tests / examples

The end-goal is to figure out how to present an ordered table of sorted rows, where rows will be made available out of
order compared to where they should be printed in the table.
"""

import time
from argparse import ArgumentParser
from collections import OrderedDict
from concurrent import futures

import urwid
from blessings import Terminal


def main():
    parser = ArgumentParser(description="Multithreaded multiline CLI output tests / examples")
    egroup = parser.add_mutually_exclusive_group()
    egroup.add_argument("--blessings", "-b", action="store_true", help="Run the example using blessings")
    egroup.add_argument("--urwid", "-u", action="store_true", help="Run the example using urwid")
    args = parser.parse_args()

    if args.blessings:
        blessings_example()
    elif args.urwid:
        urwid_example()
    else:
        print("Invalid option.")


def wait_and_return(n):
    time.sleep(abs(n - 5))
    return "This is line {}".format(n)


def urwid_example():
    lines = 10
    output = OrderedDict((n, "") for n in range(lines))
    txt = urwid.Text("\n".join(output.values()))
    frame = urwid.Filler(txt, valign="bottom")
    loop = urwid.MainLoop(frame)
    with loop.start():
        with futures.ThreadPoolExecutor(max_workers=lines) as fexec:
            to_do_map = {fexec.submit(wait_and_return, n): n for n in range(lines)}
            for future in futures.as_completed(to_do_map):
                n = to_do_map[future]
                output[n] = future.result()
                txt.set_text("\n".join(output.values()))
                loop.draw_screen()


def blessings_example():
    term = Terminal()
    lines = 10

    for n in range(lines):  # make room for new lines
        print()

    with futures.ThreadPoolExecutor(max_workers=lines) as fexec:
        to_do_map = {fexec.submit(wait_and_return, n): n for n in range(lines)}
        for future in futures.as_completed(to_do_map):
            n = to_do_map[future]

            with term.location(0, term.height - 11 + n):
                print(future.result())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
