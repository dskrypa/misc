# -*- coding: UTF-8 -*-
"""
Old library of functions that I used often while learning...  Cleaned up slightly.
"""

import os
import re
import sys
import time


def getPaths(path):
    """Recursively generates a list of absolute paths for every file discoverable via the given path."""
    path = path[:-1] if (path[-1:] == "/") else path
    paths = []
    if os.path.isdir(path):
        for sub in os.listdir(path):
            paths += getPaths(path + "/" + sub)
    elif os.path.isfile(path):
        paths += [path]
    return paths


def getFilteredPaths(path, ext, sort=True):
    paths = getPaths(path)
    fileFilter = re.compile(r'.*\.' + ext, re.IGNORECASE)
    filtered = [fname for fname in paths if fileFilter.match(fname)]
    return sorted(filtered) if sort else filtered


def fTime(seconds):
    seconds = int(seconds)
    minutes = int(seconds / 60)
    seconds -= (minutes * 60)
    hours = int(minutes / 60)
    minutes -= (hours * 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)


class PerfTimer():
    """Simple performance monitor including a timer and counters"""
    def __init__(self):
        self.start = time.perf_counter()

    def time(self):
        """Return the current time using the same method as the internal timer"""
        return time.perf_counter()

    def elapsed(self, since=None):
        """Return the time delta in seconds since initialization"""
        sinceTime = self.start if since is None else since
        return time.perf_counter() - sinceTime

    def elapsedf(self):
        """Return the time delta as a string in the form HH:MM:SS"""
        return time.strftime("%H:%M:%S",time.gmtime(self.elapsed()))


class clio():
    """Command Line Interface Output"""
    lml=0;
    #utfout = open(1, 'w', encoding="utf-8", closefd=False)
    @classmethod
    def _fmt(cls, msg):
        """Format the given message for overwriting"""
        mlen = len(msg)
        suffix = " " * (clio.lml-mlen) if mlen < clio.lml else ""
        clio.lml = mlen
        return "\r" + msg + suffix

    @classmethod
    def show(cls, msg=""):
        """Display overwritable message"""
        wmsg = cls._fmt(msg)	#.encode("utf-8")
        #clio.utfout.write(wmsg)
        #clio.utfout.flush()
        sys.stdout.write(wmsg)
        sys.stdout.flush()

    @classmethod
    def showf(cls, fmt, *args):
        """Display formatted overwritable message"""
        msg = fmt.format(*args)
        cls.show(msg)

    @classmethod
    def println(cls, msg=""):
        """Display message on a new line"""
        wmsg = cls._fmt(msg + "\n")	#.encode("utf-8")
        #sys.stdout.write(cls._fmt(msg) + "\n")
        #clio.utfout.write(wmsg)
        #clio.utfout.flush()
        sys.stdout.write(wmsg)
        sys.stdout.flush()

    @classmethod
    def printf(cls, fmt, *args):
        """Display formatted message on a new line"""
        msg = fmt.format(*args)
        cls.println(msg)


class ErrorLog():
    """Simple error log that includes a date+time stamp for each line"""
    def __init__(self, path):
        self.logfile = open(path, "a", encoding="utf-8")
        self.tfmt = "%Y-%m-%d_%H:%M:%S"
        self.lfmt = "[{}] {}\n"

    def record(self, err):
        ts = time.strftime(self.tfmt, time.localtime())
        self.logfile.write(self.lfmt.format(ts, err))
        self.logfile.flush()

    def close(self):
        self.logfile.close()
