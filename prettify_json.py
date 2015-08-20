#!/usr/bin/env python
import sys, os, glob, shutil, numpy
import json
from optparse import OptionParser

from region_utils.region_write_utils import *

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="input file", metavar="FILE")

options, args = parser.parse_args()

if not options.filename:
	parser.error("An input filename is required.")

f = open(options.filename)
region_file = json.load(f)
f.close()

prettied = open('new_region.geojson', 'w')

prettied.write('{"type": "FeatureCollection",\n')
prettied.write(' "features":\n')
prettied.write('\t[\n')

write_all_regions(region_file, prettied, '\t\t')

prettied.write('\n')
prettied.write('\t]\n')
prettied.write('}\n')
prettied.close()

