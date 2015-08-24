#!/usr/bin/env python

"""

This script has two modes of usage:
1. To create a new file (regions.geojson) containing one or more regions that
are pointed to using the -r or -d flags.

2. To append one or more regions on an already existing regions.geojson file,
again defined by the -r and -d flags.

The usage mode is automatically detected for you, depending on if the
regions.geojson file exists or not before calling this script.

"""

import sys, os, glob, shutil, numpy
import json
import argparse
from region_utils.region_write_utils import *

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-r", "--region_file", dest="region_file", help="Single region file to append to regions.geojson", metavar="FILE")
parser.add_argument("-d", "--region_directory", dest="region_dir", help="Directory containing multiple region files, each will be appended to regions.geojson", metavar="PATH")

args = parser.parse_args()

if not args.region_file and not args.region_dir:
	parser.error('Either a region file (-r) or a region directory (-d) is required.')

if args.region_dir:
	if not os.path.exists(args.region_dir):
		parser.error('The path %s does not exist.'%(args.region_dir))

if args.region_file:
	if not os.path.exists(args.region_file):
		parser.error('The file %s does not exist.'%(args.region_file))

file_to_append = "regions.geojson"

new_file = True
first_feature = True
if os.path.exists(file_to_append):
	new_file = False
	with open(file_to_append) as f:
		appended_file = json.load(f)
		first_feature = False

out_file = open(file_to_append, 'w')

out_file.write('{"type": "FeatureCollection",\n')
out_file.write(' "features":\n')
out_file.write('\t[\n')

if args.region_file:
	with open(args.region_file) as f:
		region_file = json.load(f)

		for feature in region_file['features']:
			if new_file:
				appended_file = region_file
				new_file = False
				first_feature = False
			else:
				appended_file['features'].append(feature)
				first_feature = False

		del region_file

if args.region_dir:
	for (dirpath, dirnames, filenames) in os.walk(args.region_dir):
		for filename in sorted(filenames):
			with open('%s/%s'%(dirpath, filename), 'r') as f:
				region_file = json.load(f)

				if first_feature:
					appended_file = region_file
					first_feature = False
				else:
					for feature in region_file['features']:
						appended_file['features'].append(feature)
						first_feature = False
				del region_file

write_all_regions(appended_file, out_file, '\t\t')
out_file.write('\n')
out_file.write('\t]\n')
out_file.write('}\n')

