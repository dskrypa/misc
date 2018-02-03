#!/usr/bin/env python3
'''
Bogobogosort

This is not intended to be efficient!  It is a purposefully inefficient algorithm intended as a joke.

This implementation of Bogobogosort is based on the description found here:
http://www.dangermouse.net/esoteric/bogobogosort.html
'''

import random
import sys
import time
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="Bogobogosort")
    parser.add_argument("--value", "-v", type=int, nargs="+", help="Values to sort", action="append")
    parser.add_argument("--nargs", "-n", type=int, help="Number of values to generate to sort")
    parser.add_argument("--test", "-t", type=int, metavar="maxN", help="Test with list lengths up to maxN")
    parser.add_argument("--count", "-c", type=int, help="Number of trials to test. Only applies when running a test.", default=5)
    args = parser.parse_args()

    if (args.value is None) and (args.nargs is None) and (args.test is None):
        parser.print_help()
        parser.exit(0, "value, nargs, or test is required.\n")
    elif (args.test is not None) and ((args.value is not None) or (args.nargs is not None)):
        parser.print_help()
        parser.exit(0, "Invalid combination of arguments.\n")
    elif (args.value is not None) and (args.nargs is not None):
        parser.print_help()
        parser.exit(0, "Provide a list of numbers, or a number of values to generate, not both.\n")

    if args.test is not None:
        bbsTest(args.test+1, args.count)
    else:
        if args.value is not None:
            vals = [item for sublist in args.value for item in sublist]
        else:
            vals = randlist(0, 10000, args.nargs)

        print("Sorting {}...".format(vals))
        pt = PerfTimer()
        srtd = bogobogosort(vals)
        elapsed = pt.elapsedf()
        print("Sorted {} in {}".format(srtd, elapsed))


def randlist(minval, maxval, count):
    return [random.randint(minval, maxval) for c in range(count)]


def bbsTest(maxN, trials):
    fmt = "{:11.4f}s for N={}: {} -> {}"
    tests = {}
    for n in range(1, maxN):
        tests[n] = []
        for t in range(trials):
            vals = randlist(0, 10000, n)
            pt = PerfTimer()
            srtd = bogobogosort(vals)
            elapsed = pt.elapsed()
            tests[n].append(elapsed)
            print(fmt.format(elapsed, n, vals, srtd))

    thdr = "  N  | Average Time"
    tfmt = "{:4d} | {:11.4f}s"
    print(thdr)
    print("-" * len(thdr))
    for n in range(1, maxN):
        ttime = sum(tests[n])
        atime = ttime / trials
        print(tfmt.format(n, atime))


def bogobogosort(arr):
    cpy = list(arr)						#Create a copy of the list
    last = len(cpy) - 1					#Determine the index of the last element in the list
    if (last < 1):						#If the last index is less than 1 (i.e., there are fewer than 2 elements)
        return cpy						#Then the list is sorted
    subl = bogobogosort(cpy[:last])		#Sort the first n-1 elements of the list
    if (cpy[last] >= max(subl)):		#If the nth element is greater than or equal to the max of the first n-1 elements
        srtd = subl + [cpy[last]]		#Then the list is sorted
        sameAsOrig = (srtd == arr)		#Check to see if the copy is in the same order as the original list
        return srtd						#Return the sorted list
    else:								#If the nth element doesn't have the highest value
        random.shuffle(cpy)				#Randomize the order of the elements in the list
        return bogobogosort(cpy)		#Run bogobogosort on the shuffled copy


def fTime(seconds):
    """Returns a string representation of the given number of seconds as HH:MM:SS.ssss"""
    orig = seconds
    s = int(seconds)
    rmd = orig - s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:07.4f}".format(h, m, s + rmd)


class PerfTimer():
    def __init__(self):
        PY2 = (sys.version_info.major == 2)
        self.now = time.time if PY2 else time.perf_counter
        self.start = self.now()

    def time(self):
        return self.now()

    def elapsed(self, since=None):
        """Calculates the time since the given time or since initialization"""
        sinceTime = self.start if since is None else since
        return self.now() - sinceTime

    def elapsedf(self, since=None):
        """Returns the time delta as a string in the form HH:MM:SS"""
        return fTime(self.elapsed(since))


if __name__ == "__main__":
    main()
