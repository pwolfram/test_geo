#!/usr/bin/env python

"""

This script has two modes of usage:
1. To create a new file (features.geojson) containing one or more features that
are pointed to using the -f or -d flags.

2. To append one or more features on an already existing features.geojson file,
again defined by the -f and -d flags.

The usage mode is automatically detected for you, depending on if the
features.geojson file exists or not before calling this script.

"""

import sys, os, glob, shutil, numpy
import json
import argparse
from utils.feature_write_utils import *

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--feature_file", dest="feature_file", help="Single feature file to append to features.geojson", metavar="FILE")
parser.add_argument("-d", "--features_directory", dest="features_dir", help="Directory containing multiple feature files, each will be appended to features.geojson", metavar="PATH")

args = parser.parse_args()

if not args.feature_file and not args.features_dir:
	parser.error('Either a feature file (-f) or a feature directory (-d) is required.')

if args.features_dir:
	if not os.path.exists(args.features_dir):
		parser.error('The path %s does not exist.'%(args.features_dir))

if args.feature_file:
	if not os.path.exists(args.feature_file):
		parser.error('The file %s does not exist.'%(args.feature_file))

file_to_append = "features.geojson"

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

if args.feature_file:
	with open(args.feature_file) as f:
		feature_file = json.load(f)

		for feature in feature_file['features']:
			if new_file:
				appended_file = feature_file
				new_file = False
				first_feature = False
			else:
				appended_file['features'].append(feature)
				first_feature = False

		del feature_file

if args.features_dir:
	for (dirpath, dirnames, filenames) in os.walk(args.features_dir):
		for filename in sorted(filenames):
			with open('%s/%s'%(dirpath, filename), 'r') as f:
				feature_file = json.load(f)

				if first_feature:
					appended_file = feature_file
					first_feature = False
				else:
					for feature in feature_file['features']:
						appended_file['features'].append(feature)
						first_feature = False
				del feature_file

write_all_features(appended_file, out_file, '\t\t')
out_file.write('\n')
out_file.write('\t]\n')
out_file.write('}\n')

