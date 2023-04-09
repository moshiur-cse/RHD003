from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.shortcuts import redirect, render

from django.shortcuts import render
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point
import geopandas as gpd
import json
#from django.contrib.gis.maps.google import GoogleMap



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/dashboards/index.html'


    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        """
        # Example to get page name. Refer to dashboards/urls.py file.
        url_name = resolve(self.request.path_info).url_name

        if url_name == 'dashboard-2':
            # Example to override settings at the runtime
            settings.KT_THEME_DIRECTION = 'rtl'
        else:
            settings.KT_THEME_DIRECTION = 'ltr'
        """

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context
    

        #return render(request, 'map.html')
def map(request):
    layout = 'layout/master.html'  # set a default value 
    template_name = 'pages/maps/map.html'
    shapefile = gpd.read_file('assets/geofiles/division/division.shp')
    my_geojson_str = shapefile.to_crs(epsg=4326).to_json()  

    print('Test');        
    #my_geojson_str = json.dumps(my_geojson_str)      
                #return render(request, 'my_template.html', {'my_geojson': my_geojson_str})     
    print(my_geojson_str)
        

    context = {'layout':layout,'geojson':my_geojson_str,'my_data': ''}
    return render(request, template_name, context)
        #return render(request, 'map.html', {'geojson': geojson,'my_variable':'Moshiur Rahman'})    

  
