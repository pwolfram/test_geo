#!/use/bin/env python
import json

def match_tag_list(feature, master_tags):#{{{
	try:
		feature_tags = feature['properties']['tags']
	except:
		return True
	
	feature_tag_list = feature_tags.split(';')

	return any((True for tag in feature_tag_list if tag in master_tags))
#}}}
