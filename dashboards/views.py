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
    
    def map(request):
        data_source = DataSource('/path/to/geotiff.tiff')

    # Get the first layer from the file
        layer = data_source[0]

        # Create a GeoJSON object from the layer
        geojson = layer.geojson

        # Get the bounding box of the layer
        bbox = layer.extent

        # Create a Point object from the center of the bounding box
        center = Point((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

        # Create a GoogleMap object with the center and zoom level
        map = GoogleMap(center=center, zoom=10)

        # Add the GeoJSON data to the map
        map.add_layer(geojson)

        # Render the map using a template
        #return render(request, 'map.html', {'map': map})
        return render(request, 'map.html')
