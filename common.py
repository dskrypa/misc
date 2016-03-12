# -*- coding: UTF-8 -*-

'''
Author: Douglas Skrypa
Date: 2016.01.23
Version: 1.3
'''

import os, sys, time, re;

def getPaths(path):
	'''
	Recursively generates a list of absolute paths for every file discoverable
	via the given path.
	'''
	path = path[:-1] if (path[-1:] == "/") else path;							#Strip trailing slash if it exists
	paths = [];																	#Initialize list to store paths in
	if os.path.isdir(path):														#If the given path is a directory
		for sub in os.listdir(path):											#Iterate through each sub-path in it
			paths += getPaths(path + "/" + sub);								#Add the list of paths discoverable there
	elif os.path.isfile(path):													#Otherwise, if it is a file
		paths += [path];														#Add the path to the list
	return paths;																#Return the list
#/getPaths

def getFilteredPaths(path, ext, sort=True):
	paths = getPaths(path);														#Get the paths
	fileFilter = re.compile(r'.*\.' + ext, re.IGNORECASE);						#Define the filter
	filtered = [fname for fname in paths if fileFilter.match(fname)];			#Apply the filter
	return sorted(filtered) if sort else filtered;								#Return the filtered list (sorted if sort == True)
#/getFilteredPaths

def fTime(seconds):
	seconds = int(seconds);
	minutes = int(seconds / 60);
	seconds -= (minutes * 60);
	hours = int(minutes / 60);
	minutes -= (hours * 60);
	return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds);
#/fTime

class PerfTimer():
	'''Simple performance monitor including a timer and counters'''
	def __init__(self):
		self.start = time.perf_counter();										#Initialize the timer with the current time
	#/init
	def time(self):
		return time.perf_counter();												#Return the current time using the same method as the internal timer
	#/time	
	def elapsed(self, since=None):
		sinceTime = self.start if (since == None) else since;
		return time.perf_counter() - sinceTime;									#Return the time delta in seconds since initialization
	#/elapsed
	def elapsedf(self):
		return time.strftime("%H:%M:%S",time.gmtime(self.elapsed()));			#Return the time delta as a string in the form HH:MM:SS
	#/elapsedf
#/PerfTimer

class clio():
	'''Command Line Interface Output'''
	lml=0;
	#utfout = open(1, 'w', encoding="utf-8", closefd=False);
	@classmethod
	def _fmt(cls, msg):
		'''Format the given message for overwriting'''
		mlen = len(msg);
		suffix = " " * (clio.lml-mlen) if (mlen < clio.lml) else "";
		clio.lml = mlen;
		return "\r" + msg + suffix;
	#/fmt
	@classmethod
	def show(cls, msg=""):
		'''Display overwritable message'''
		wmsg = cls._fmt(msg);	#.encode("utf-8");
		#clio.utfout.write(wmsg);
		#clio.utfout.flush();
		sys.stdout.write(wmsg);
		sys.stdout.flush();
	#/show
	@classmethod
	def showf(cls, fmt, *args):
		'''Display formatted overwritable message'''
		msg = fmt.format(*args);
		cls.show(msg);
	#/showf
	@classmethod
	def println(cls, msg=""):
		'''Display message on a new line'''
		wmsg = cls._fmt(msg + "\n");	#.encode("utf-8");
		#sys.stdout.write(cls._fmt(msg) + "\n");
		#clio.utfout.write(wmsg);
		#clio.utfout.flush();
		sys.stdout.write(wmsg);
		sys.stdout.flush();
	#/println
	@classmethod
	def printf(cls, fmt, *args):
		'''Display formatted message on a new line'''
		msg = fmt.format(*args);
		cls.println(msg);
	#/printf
#/clio

class ErrorLog():
	'''Simple error log that includes a date+time stamp for each line'''
	def __init__(self, path):
		self.logfile = open(path, "a", encoding="utf-8");
		self.tfmt = "%Y-%m-%d_%H:%M:%S";
		self.lfmt = "[{}] {}\n";
	#/init
	def record(self, err):
		ts = time.strftime(self.tfmt, time.localtime());
		self.logfile.write(self.lfmt.format(ts, err));
		self.logfile.flush();
	#/record
	def close(self):
		self.logfile.close();
	#/close
#/ErrorLog