#!/usr/bin/env python
"""
Script to plot regions.geojson file via basemap
Phillip J. Wolfram
08/25/2015
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic

def plot_base(maptype): #{{{
    if maptype == 'ortho':
        map = Basemap(projection='ortho', lat_0=45, lon_0=-100, resolution='l')
        map.drawmeridians(np.arange(0,360,30))
        map.drawparallels(np.arange(-90,90,30))
    elif maptype == 'mill': 
        map = Basemap(llcrnrlon=0,llcrnrlat=-90,urcrnrlon=360,urcrnrlat=90,projection='mill')
        map.drawparallels(np.arange(-80,81,20),labels=[1,1,0,0])
        map.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
    elif maptype == 'mill2': 
        map = Basemap(llcrnrlon=-180,llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,projection='mill')
        map.drawparallels(np.arange(-80,81,20),labels=[1,1,0,0])
        map.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
    elif maptype == 'hammer':
        map = Basemap(projection='hammer',lon_0=180)
        map.drawmeridians(np.arange(0,360,30))
        map.drawparallels(np.arange(-90,90,30))
    elif maptype == 'northpole':
        map = Basemap(projection='ortho', lat_0=90, lon_0=-100, resolution='l')
        map.drawmeridians(np.arange(0,360,30))
        map.drawparallels(np.arange(-90,90,30))
    elif maptype == 'southpole':
        map = Basemap(projection='ortho', lat_0=-90, lon_0=-100, resolution='l')
        map.drawmeridians(np.arange(0,360,30))
        map.drawparallels(np.arange(-90,90,30))
    else:
        raise NameError("Didn't select a valid maptype!")

    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='#e0e0e0', lake_color='white')
    map.drawmapboundary(fill_color='white')
    return map #}}}
  

def plot_regions_file(regionfile, plotname):
    # open up the database
    with open(regionfile) as f:
        regiondat = json.load(f)

    fig = plt.figure(figsize=(16,12),dpi=100)
    for anum, maptype in enumerate(['northpole','mill2','mill', 'southpole']):
        ax = fig.add_subplot(2,2,1+anum)
        for feature in regiondat['features']:
            polytype = feature['geometry']['type']
            coords = feature['geometry']['coordinates']
            region = feature['properties']['name']

            map = plot_base(maptype)
            try:
                if polytype == 'MultiPolygon':
                    for poly in coords:
                        points = np.asarray(poly)
                        map.plot(points[:,0], points[:,1], linewidth=2.0, color='r',latlon=True)
                elif polytype == 'Polygon':
                    points = np.asarray(coords)
                    map.plot(points[:,0], points[:,1], linewidth=2.0, color='r',latlon=True)
                else:
                    assert False, 'Geometry %s not known.'%(polytype)
            except:
                print 'Error plotting %s for map type %s'%(region, maptype)
    print 'saving ' + plotname 
    plt.savefig(plotname)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-r", "--regions_file", dest="regions_file", help="Region file to plot", metavar="FILE")
    parser.add_option("-o", "--regions_plot", dest="regions_plotname", help="Region plot filename", metavar="FILE")

    options, args = parser.parse_args()

    if not options.regions_file:
        parser.error("A region file is required.")
    
    if not options.regions_plotname:
        options.regions_plotname = 'plot_' + options.regions_file.strip('.*') + '.png'

    plot_regions_file(options.regions_file, options.regions_plotname)


