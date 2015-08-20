#!/usr/bin/env python

import sys, os, glob, shutil, numpy
import json
from optparse import OptionParser
from region_utils.region_write_utils import *

parser = OptionParser()
parser.add_option("-r", "--regions_file", dest="regions_file", help="Region file to split up", metavar="FILE")

options, args = parser.parse_args()

if not options.regions_file:
	parser.error('A region file is required.')

if options.regions_file:
	if not os.path.exists(options.regions_file):
		parser.error('The file %s does not exist.'%(options.regions_file))

with open(options.regions_file) as f:
	regions_file = json.load(f)


for feature in regions_file['features']:
	region_name = feature['properties']['name']
	component = feature['properties']['component']
	object_dir = "%s"%(feature['properties']['object'])

	dir_name = region_name.strip().replace(' ','_').strip('\'').strip('.',)

	if not os.path.exists('%s/%s/%s'%(component, object_dir, dir_name)):
		os.makedirs('%s/%s/%s'%(component, object_dir, dir_name))

	out_file = open('%s/%s/%s/region.geojson'%(component, object_dir, dir_name), 'w')

	out_file.write('{"type": "FeatureCollection",\n')
	out_file.write(' "features":\n')
	out_file.write('\t[\n')
	write_single_region(feature, out_file, '\t\t')
	out_file.write('\n')
	out_file.write('\t]\n')
	out_file.write('}\n')
	out_file.close()


