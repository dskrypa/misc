#!/usr/bin/env python

'''
Dupe Finder
Author: Douglas Skrypa
Version: 2016.03.06 E
'''

import os, sys, hashlib, re;
import argparse;

from common import *;

def main(args):
	findDupes(args);
#/main

def findDupes(args):
	parser = argparse.ArgumentParser(description="Dupe Finder - Scan the given directories for duplicate files.");
	parser.add_argument("--recurse", "-r", help="Scan directories recursively (default: off)", action="store_true", default=False);
	parser.add_argument("--details", "-t", help="Print a detailed list of file names (default: summary only)", action="store_true", default=False);
	parser.add_argument("--diff1", "-f1", help="Print file paths from dir1 that have a hash that doesn't exist in dir2 (default: off)", action="store_true", default=False);
	parser.add_argument("--diff2", "-f2", help="Print file paths from dir2 that have a hash that doesn't exist in dir1  (default: off)", action="store_true", default=False);
	parser.add_argument("--uniq1", "-u1", help="Print file paths from dir1 that have a name+hash that doesn't exist in dir2 (default: off)", action="store_true", default=False);
	parser.add_argument("--uniq2", "-u2", help="Print file paths from dir2 that have a name+hash that doesn't exist in dir1 (default: off)", action="store_true", default=False);
	parser.add_argument("--dupe1", "-d1", help="Print file paths from dir1 that have a duplicate hash to a file in dir2 (default: off)", action="store_true", default=False);
	parser.add_argument("--dupe2", "-d2", help="Print file paths from dir2 that have a duplicate hash to a file in dir1 (default: off)", action="store_true", default=False);
	parser.add_argument("--level", "-l", metavar="n", help="Recurse level when summarizing directory contents (default: max)", type=int, default=-1);
	parser.add_argument('dir1', help="Directory to scan", default=None);
	parser.add_argument('dir2', help="Directory to scan", default=None);
	args = parser.parse_args();

	if ((args.dir1 == None) or (args.dir2 == None)):
		parser.print_help();													#Print the help text
		parser.exit(0, "Two paths are required!\n");
	elif not os.path.exists(args.dir1):
		parser.print_help();													#Print the help text
		parser.exit(0, "Invalid path: '{}'\n".format(args.dir1));
	elif not os.path.exists(args.dir2):
		parser.print_help();													#Print the help text
		parser.exit(0, "Invalid path: '{}'\n".format(args.dir2));
	elif (True not in (args.diff1, args.diff2, args.uniq1, args.uniq2, args.dupe1, args.dupe2)):
		parser.print_help();													#Print the help text
		parser.exit(0, "No output selected. Please choose --diff#, --uniq#, or --dupe# (-f2 recommended)\n");
	
	p1 = os.path.normpath(args.dir1);
	p2 = os.path.normpath(args.dir2);
	
	p1files = getFilteredPaths(p1, "db", True, True, args.recurse);
	p2files = getFilteredPaths(p2, "db", True, True, args.recurse);
	p1count = len(p1files);
	p2count = len(p2files);
	clio.printf("Comparing '{}/*' ({:,d} files) and '{}/*' ({:,d} files)", p1, p1count, p2, p2count);
	
	p1lc = {os.path.basename(fpath).lower():fpath for fpath in p1files};
	p2lc = {os.path.basename(fpath).lower():fpath for fpath in p2files};
	
	hashes1 = {};
	hashes2 = {};
	dupes1 = {};
	dupes2 = {};
	different1 = {};
	different2 = {};
	unique1 = {};
	unique2 = {};
	sameNameDifHash1 = {};
	sameNameDifHash2 = {};
	fmt = "{} - {:7.2%} [{:20}] [{:20}]";
	
	pt = PerfTimer();
	clio.println();
	clio.printf("Scanning '{}' ({:,d} files)...", p1, p1count);
	lastt = pt.elapsed();
	c = 0;
	for fpath in p1files:
		c += 1;
		elapsed = pt.elapsed();
		if ((elapsed - lastt) > 0.75):
			lastt = elapsed;
			pct = c/p1count;
			clio.showf(fmt, pt.elapsedf(), pct, "="*int(pct*20), "");
		hash = hashlib.sha256(open(fpath,"rb").read()).hexdigest();
		hashes1[hash] = fpath;
	fullBar = "="*20;
	clio.showf(fmt, pt.elapsedf(), 1, fullBar, "");
	
	clio.println();
	clio.printf("Scanning '{}' ({:,d} files)...", p2, p2count);
	lastt = pt.elapsed();
	c = 0;
	for fpath in p2files:
		c += 1;
		elapsed = pt.elapsed();
		if ((elapsed - lastt) > 0.75):
			lastt = elapsed;
			pct = c/p2count;
			clio.showf(fmt, pt.elapsedf(), pct, fullBar, "="*int(pct*20));
		hash = hashlib.sha256(open(fpath,"rb").read()).hexdigest();
		hashes2[hash] = fpath;
		if hash in hashes1:
			dupes2[fpath] = hashes1[hash];
			dupes1[hashes1[hash]] = fpath;
		else:
			different2[fpath] = True;
			if os.path.basename(fpath).lower() in p1lc:
				sameNameDifHash2[fpath] = True;
			else:
				unique2[fpath] = True;
	clio.showf(fmt, pt.elapsedf(), 1, fullBar, fullBar);
	
	for hash in hashes1:
		fpath = hashes1[hash];
		if (hash not in hashes2):
			different1[fpath] = True;
			if os.path.basename(fpath).lower() in p2lc:
				sameNameDifHash1[fpath] = True;
			else:
				unique1[fpath] = True;
	
	dupeCount = len(dupes1);
	diffCount1 = len(different1);
	diffCount2 = len(different2);
	uniqCount1 = len(unique1);
	uniqCount2 = len(unique2);
	
	summary1 = summarize(p1, dupes1, different1, unique1);
	summary2 = summarize(p2, dupes2, different2, unique2);
	
	summaryHeader = "Duplicates  Different    Unique   Folders     Files  Directory";
	
	clio.println("\n");
	if (dupeCount == p1count):
		clio.printf("All files in '{}' are duplicates of files in '{}'!", p1, p2);
	if (dupeCount == p2count):
		clio.printf("All files in '{}' are duplicates of files in '{}'!", p2, p1);
	
	if (dupeCount not in (p1count, p2count)):
		if not (args.dupe1 or args.dupe2):
			clio.printf("Found {:,d} duplicate files!\n", dupeCount);
		elif (dupeCount != p1count) and args.dupe1:
			clio.printf("Found {:,d} duplicate files in '{}':", dupeCount, p1);
			clio.println(summaryHeader);
			printSummary(summary1, p1, args.level, 'dupes', args.details);
		elif (dupeCount != p2count) and args.dupe2:
			clio.printf("Found {:,d} duplicate files in '{}':", dupeCount, p1);
			clio.println(summaryHeader);
			printSummary(summary2, p2, args.level, 'dupes', args.details);
	clio.println();
	
	if (diffCount1 == p1count):
		clio.printf("All files in '{}' have different hashes than the files in '{}'!\n", p1, p2);
	else:
		echar = ":\n" if args.diff1 else "\n";
		clio.printf("Found {:,d} files in '{}' that were not in '{}'{}", diffCount1, p1, p2, echar);
		if args.diff1:
			clio.println(summaryHeader);
			printSummary(summary1, p1, args.level, 'diffs', args.details);
	if (diffCount2 == p2count):
		clio.printf("All files in '{}' have different hashes than the files in '{}'!\n", p2, p1);	
	else:
		echar = ":\n" if args.diff2 else "\n";
		clio.printf("Found {:,d} files in '{}' that were not in '{}'{}", diffCount2, p2, p1, echar);
		if args.diff2:
			clio.println(summaryHeader);
			printSummary(summary2, p2, args.level, 'diffs', args.details);
	clio.println();
	
	if (uniqCount1 == p1count):
		clio.printf("All files in '{}' completely different than the files in '{}'!\n", p1, p2);
	else:
		echar = ":\n" if args.uniq1 else "\n";
		clio.printf("Found {:,d} files in '{}' that have unique names and content{}", uniqCount1, p1, echar);
		if args.uniq1:
			clio.println(summaryHeader);
			printSummary(summary1, p1, args.level, 'uniqs', args.details);
	if (uniqCount2 == p2count):
		clio.printf("All files in '{}' completely different than the files in '{}'!\n", p2, p1);	
	else:
		echar = ":\n" if args.uniq2 else "\n";
		clio.printf("Found {:,d} files in '{}' that have unique names and content{}", uniqCount2, p2, echar);
		if args.uniq2:
			clio.println(summaryHeader);
			printSummary(summary2, p2, args.level, 'uniqs', args.details);
	clio.println();
#/findDupes

def printSummary(summary, path, levels, section, printDetails=False):
	if (levels == 0): return;
	if (summary[section + "_c"] > 0):
		clio.printf("{:10,d}  {:9,d}  {:8,d}  {:8,d}  {:8,d}  {}", summary['dupes_c'], summary['diffs_c'], summary['uniqs_c'], countDirs(path), countFiles(path), path);
		if printDetails:
			detailFmt = (" " * 53) + "{}";
			for f in sorted(summary[section].keys()):
				if (os.path.dirname(f) == path):
					clio.printf(detailFmt, f);
	for sub in sorted(summary['subs'].keys()):
		printSummary(summary['subs'][sub], sub, levels-1, section, printDetails);
#/printSummary

def countFiles(path):
	return len([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]);
#/countFiles

def countDirs(path):
	return len([f for f in os.listdir(path) if os.path.isdir(path + os.path.sep + f)]);
#/countFiles

def summarize(path, dupeList, diffList, uniqList):
	dc = len([f for f in dupeList if path == os.path.dirname(f)]);
	fc = len([f for f in diffList if path == os.path.dirname(f)]);
	uc = len([f for f in uniqList if path == os.path.dirname(f)]);
	contents = {'subs':{}, 'dupes':dupeList, 'diffs':diffList, 'uniqs':uniqList, 'dupes_c':dc, 'diffs_c':fc, 'uniqs_c':uc};
	if os.path.isdir(path):														#If the given path is a directory
		for sub in os.listdir(path):											#Iterate through each sub-path in it
			subpath = path + os.path.sep + sub;
			if os.path.isdir(subpath):
				subDupes = {f:dupeList[f] for f in dupeList if f.startswith(subpath)};
				subDiffs = {f:diffList[f] for f in diffList if f.startswith(subpath)};
				subUniqs = {f:uniqList[f] for f in uniqList if f.startswith(subpath)};
				
				#subDupes = {f:dupeList[f] for f in dupeList if subpath.startswith(os.path.dirname(f))};
				#subDiffs = {f:diffList[f] for f in diffList if subpath.startswith(os.path.dirname(f))};
				#subUniqs = {f:uniqList[f] for f in uniqList if subpath.startswith(os.path.dirname(f))};
				
				contents['subs'][subpath] = summarize(subpath, subDupes, subDiffs, subUniqs);
	return contents;
#/summarize

def getDirs(path):
	dirs = [];
	if os.path.isdir(path):														#If the given path is a directory
		for sub in os.listdir(path):											#Iterate through each sub-path in it
			subpath = path + os.path.sep + sub;
			if os.path.isdir(subpath):
				dirs += subdir;
				dirs += getDirs(subdir);										#Add the list of paths discoverable there
	return dirs;																#Return the list
#/getDirs

def getPaths(path):
	paths = [];																	#Initialize list to store paths in
	if os.path.isdir(path):													#If the given path is a directory
		for sub in os.listdir(path):											#Iterate through each sub-path in it
			paths += getPaths(path + os.path.sep + sub);						#Add the list of paths discoverable there
	elif os.path.isfile(path):													#Otherwise, if it is a file
		paths += [path];														#Add the path to the list
	return paths;																#Return the list
#/getPaths

def getFilteredPaths(path, ext, sort=True, reverse=False, recurseDirs=False):
	paths = getPaths(path) if recurseDirs else os.listdir(path);				#Get the paths
	fileFilter = re.compile(r'.*\.' + ext, re.IGNORECASE);						#Define the filter	
	if not recurseDirs:
		paths = [path + os.path.sep + fname for fname in paths];
		paths = [fpath for fpath in paths if os.path.isfile(fpath)];

	if reverse:
		filtered = [fname for fname in paths if not fileFilter.match(fname)];	#Apply the filter
	else:
		filtered = [fname for fname in paths if fileFilter.match(fname)];		#Apply the filter
	return sorted(filtered) if sort else filtered;								#Return the filtered list (sorted if sort == True)
#/getFilteredPaths

if __name__ == "__main__":
	main(sys.argv);
#/__main__