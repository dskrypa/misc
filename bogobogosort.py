#!/usr/bin/python3

'''
Bogobogosort
Author: Douglas Skrypa
Version: 2016.02.05

This implementation of Bogobogosort is based on the description found here:
http://www.dangermouse.net/esoteric/bogobogosort.html
'''

import random, time, sys;
from argparse import ArgumentParser;

def main():
	parser = ArgumentParser(description="Bogobogosort");
	parser.add_argument("--value", "-v", type=int, nargs="+", help="Values to sort", action="append");
	parser.add_argument("--nargs", "-n", type=int, help="Number of values to generate to sort");
	parser.add_argument("--test", "-t", type=int, metavar="maxN", help="Test with list lengths up to maxN");
	parser.add_argument("--count", "-c", type=int, help="Number of trials to test. Only applies when running a test.", default=5);
	args = parser.parse_args();
	
	if (args.value == None) and (args.nargs == None) and (args.test == None):
		parser.print_help();
		parser.exit(0, "At least one argument is required.\n");
	elif (args.test != None) and ((args.value != None) or (args.nargs != None)):
		parser.print_help();
		parser.exit(0, "Invalid combination of arguments.\n");
	elif (args.value != None) and (args.nargs != None):
		parser.print_help();
		parser.exit(0, "Provide a list of numbers, or a number of values to generate, not both.\n");
		
	if (args.test != None):
		bbsTest(args.test+1, args.count);
	else:
		if (args.value != None):
			vals = [item for sublist in args.value for item in sublist];
		else:
			vals = randlist(0, 10000, args.nargs);
		
		print("Sorting {}...".format(vals));
		pt = PerfTimer();
		srtd = bogobogosort(vals);
		elapsed = pt.elapsedf();
		print("Sorted {} in {}".format(srtd, elapsed));
#/main

def randlist(minval, maxval, count):
	return [random.randint(minval, maxval) for c in range(count)];
#/randlist

def bbsTest(maxN, trials):
	fmt = "{:11.4f}s for N={}: {} -> {}";
	tests = {};
	for n in range(1, maxN):
		tests[n] = [];
		for t in range(trials):
			vals = randlist(0, 10000, n);
			pt = PerfTimer();
			srtd = bogobogosort(vals);
			elapsed = pt.elapsed();
			tests[n].append(elapsed);
			print(fmt.format(elapsed, n, vals, srtd));
	
	thdr = "  N  | Average Time";
	tfmt = "{:4d} | {:11.4f}s";
	print(thdr);
	print("-" * len(thdr));
	for n in range(1, maxN):
		ttime = sum(tests[n]);
		atime = ttime / trials;
		print(tfmt.format(n, atime));
#/bbsTest

def bogobogosort(arr):
	cpy = list(arr);						#Create a copy of the list
	last = len(cpy) - 1;					#Determine the index of the last element in the list
	if (last < 1):							#If the last index is less than 1 (i.e., there are fewer than 2 elements)
		return cpy;							#Then the list is sorted
	subl = bogobogosort(cpy[:last]);		#Sort the first n-1 elements of the list
	if (cpy[last] >= max(subl)):			#If the nth element is greater than or equal to the max of the first n-1 elements
		srtd = subl + [cpy[last]];			#Then the list is sorted
		sameAsOrig = (srtd == arr);			#Check to see if the copy is in the same order as the original list
		return srtd;						#Return the sorted list
	else:									#If the nth element doesn't have the highest value
		random.shuffle(cpy);				#Randomize the order of the elements in the list
		return bogobogosort(cpy);			#Run bogobogosort on the shuffled copy
#/bogobogosort

def fTime(seconds):
	orig = seconds;
	s = int(seconds);
	rmd = orig - s;
	m, s = divmod(s, 60);
	h, m = divmod(m, 60);
	return "{:02d}:{:02d}:{:07.4f}".format(h, m, s + rmd);						#Return a string representation of the given number of seconds as HH:MM:SS.ssss
#/fTime

class PerfTimer():
	def __init__(self):
		PY2 = (sys.version_info.major == 2);									#Determine whether or not the current version of Python is 2.x
		self.now = time.time if PY2 else time.perf_counter;						#Pick the timer function based on the current version of Python
		self.start = self.now();												#Initialize the timer with the current time
	def time(self):
		return self.now();														#Return the current time using the same method as the internal timer
	def elapsed(self, since=None):
		sinceTime = self.start if (since == None) else since;					#Calculate time since the given time, or since initialization
		return self.now() - sinceTime;											#Return the time delta in seconds
	def elapsedf(self, since=None):
		return fTime(self.elapsed(since));										#Return the time delta as a string in the form HH:MM:SS
#/PerfTimer

if __name__ == "__main__":
	main();
#/__main__