#!/usr/bin/python

'''
Author: Douglas Skrypa
Date: 2016-02-28
Pascal's Triangle Printer
Use -t to center each line based on the width of the longest one
'''

import sys, math;
fact = math.factorial;

def main(args):
	if len(args) < 2: return 0;					#Exit if no args
	tri = (str(args[1])[:2].lower() == "-t");	#Print as triangle?
	ao = 1 if tri else 0;						#Arg offset
	n = int(args.get(1+ao, 0));					#First value
	m = int(args.get(2+ao, n));					#Second value, if provided
	ln = str(len(str(max(n,m))));				#Used to line up 1s place of N
	fmt = "N={:"+ln+"d}: {}"					#Format for output
	
	if tri:
		wlen = len(str(max(plevel(m))));		#Max value's str width
		ttype = args[1][2:3];					#Triangle type if provided after -t
		sm = 2;									#Defaults to centered
		sc = " ";								#Space character for joining
		if (ttype == "l"):						#Left-aligned
			sm = -1;
		elif (ttype == "r"):					#Right-aligned
			sm = 1;
		elif (ttype == "w"):					#Centered with wider spacing
			sc = " " * (wlen+2);
		
		prints = {};
		for x in xrange(m, n-1, -1):
			level_arr = [str(choose(x,y)).rjust(wlen) for y in xrange(x+1)];
			level = sc.join(level_arr);
			xwidth = len(level);
			if (n <= x < m):
				level = " "*int((pwidth - xwidth)/sm) + level;
			prints[x] = level;
			if (x == m):
				pwidth = xwidth;
				
		for x in xrange(n, m+1):
			print(fmt.format(x, prints[x]));
	else:
		for x in xrange(n, m+1):
			print(fmt.format(x, ", ".join(plevel(x,True))));
#/main

def plevel(n, asStrings=False):
	'''Returns all values in the given level of Pascal's Triangle'''
	if asStrings:
		return [str(choose(n,m)) for m in xrange(n+1)];
	return [choose(n,m) for m in xrange(n+1)];
#/plevel

def choose(n, k):
	return fact(n) / (fact(k) * fact(n - k)) if (0<=k<=n) else 0;
#/choose

class List(list):
	'''Simple extension of list to add .get(index, defaultValue)'''
	def get(self, index, default=None):
		return default if (len(self) <= index) else self[index];
#/List

if __name__ == "__main__":
	main(List(sys.argv));
#/__main__
