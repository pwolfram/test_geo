#!/use/bin/env python
import json

def write_all_regions(regions, out_file, base_indent):#{{{
	first_region = True
	for feature in regions['features']:
		if not first_region:
			out_file.write(',\n')
		write_single_region(feature, out_file, base_indent)
		first_region = False
#}}}

def write_single_region(feature, out_file, base_indent):#{{{
	# Write properties first

	out_file.write('%s{"type": "Feature",\n'%(base_indent))
	out_file.write('%s "properties": {\n'%(base_indent))

	# Write out properties
	out_file.write('%s\t"name": "%s",\n'%(base_indent, feature['properties']['name']))
	out_file.write('%s\t"component": "%s",\n'%(base_indent, feature['properties']['component']))

	feature_type = feature['geometry']['type']

	# Determine object property value based on feature type.
	if feature_type == "Polygon" or feature_type == "MultiPolygon":
		out_file.write('%s\t"object": "region"\n'%(base_indent))
		
	out_file.write('%s },\n'%(base_indent))

	# Write out geometry
	out_file.write('%s "geometry":\n'%(base_indent))
	out_file.write('%s\t{"type": "%s",\n'%(base_indent, feature_type))
	out_file.write('%s\t "coordinates":\n'%(base_indent))

	out_file.write('%s\t\t[\n'%(base_indent))

	if feature_type == "MultiPolygon":
		out_file.write('%s\t\t\t[\n'%(base_indent))
		indentation = '%s\t\t\t\t'%(base_indent)
		poly_list = feature['geometry']['coordinates']
	else:
		indentation = '\t\t\t'
		poly_list = []
		poly_list.append(feature['geometry']['coordinates'])

	write_poly_seps = False

	for poly in poly_list:
		if write_poly_seps:
			out_file.write('%s%s],\n'%(base_indent, indentation))
			out_file.write('%s%s[\n'%(base_indent, indentation))
		else:
			write_poly_seps = True

		write_comma = False
		for coord in poly:
			if write_comma:
				out_file.write(',\n')
			else:
#				out_file.write('\n')
				write_comma = True

			out_file.write('%s%s[ %f, %f]'%(base_indent, indentation, coord[0], coord[1]))

		out_file.write('\n')


	if feature_type == "MultiPolygon":
		out_file.write('%s\t\t\t]\n'%(base_indent))
	out_file.write('%s\t\t]\n'%(base_indent))
	out_file.write('%s\t}\n'%(base_indent))
	out_file.write('%s}'%(base_indent))

#}}}
