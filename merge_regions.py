#!/usr/bin/env python

import sys, os, glob, shutil, numpy
import json
from optparse import OptionParser
from region_utils.region_write_utils import *

parser = OptionParser()
parser.add_option("-a", "--append_file", dest="append_file", help="File to append to", metavar="FILE")
parser.add_option("-r", "--region_file", dest="region_file", help="Region file to append", metavar="FILE")
parser.add_option("-d", "--region_directory", dest="region_dir", help="Directory containing multiple region files", metavar="PATH")

options, args = parser.parse_args()

if not options.append_file:
	parser.error('A file that will be appended is required.')

if not options.region_file and not options.region_dir:
	parser.error('Either a region file (-r) or a region directory (-d) is required.')

if options.region_dir:
	if not os.path.exists(options.region_dir):
		parser.error('The path %s does not exist.'%(options.region_dir))

if options.region_file:
	if not os.path.exists(options.region_file):
		parser.error('The file %s does not exist.'%(options.region_file))

new_file = True
first_feature = True
if os.path.exists(options.append_file):
	new_file = False
	with open(options.append_file) as f:
		appended_file = json.load(f)
		first_feature = False

out_file = open(options.append_file, 'w')

out_file.write('{"type": "FeatureCollection",\n')
out_file.write(' "features":\n')
out_file.write('\t[\n')

if options.region_file:
	with open(options.region_file) as f:
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

if options.region_dir:
	for (dirpath, dirnames, filenames) in os.walk(options.region_dir):
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

