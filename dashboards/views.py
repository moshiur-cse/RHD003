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
from django.http import JsonResponse
from django.core.serializers import serialize
import os
from .forms import UploadFileForm

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
    #shapefile = gpd.read_file('assets/geofiles/division/division.shp')
    #my_geojson_str = shapefile.to_crs(epsg=4326).to_json()  
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for shapefile in files:
                if shapefile.name.endswith('.shp'):
                    os.environ['SHAPE_RESTORE_SHX'] = 'YES'                   
                    shapefile_path = shapefile.temporary_file_path()
                    shape_file = gpd.read_file(shapefile_path)
                    shape_file = shape_file.set_crs(epsg=4326)                  
                if shapefile.name.endswith('.dbf'):
                    os.environ['SHAPE_RESTORE_SHX'] = 'YES'
                    dbffile_path = shapefile.temporary_file_path()
                    dbf_file = gpd.read_file(dbffile_path)
                    dbf_file = dbf_file.set_crs(epsg=4326)                     
                    
            joined_df = gpd.pd.merge(shape_file, dbf_file, on='common_field')   
            print(joined_df.head())                 
            my_geojson_str = joined_df.to_crs(epsg=4326).to_json()    
            # do something with the uploaded files
    else:
        form = UploadFileForm()
    
    
    #my_geojson_data = MyModel.objects.get(pk=1).geojson_field
    # Define the folder path and file name
    # folder_path = 'assets/geofiles/division'
    # file_name = 'moshiur.json'
    
    # filepath = os.path.join(folder_path, file_name)
    # with open(filepath, 'w') as f:
    #     f.write(my_geojson_str)
    # Save the GeoJSON data to the folder
    #save_geojson_to_folder(my_geojson_str, folder_path, file_name) 
    #print('Test');        
    #my_geojson_str = json.dumps(my_geojson_str)      
    #return render(request, 'my_template.html', {'my_geojson': my_geojson_str})                
    #my_geojson_str=  gpd.read_file('assets/geofiles/division/division.json')        
    #print(my_geojson_str)
        

    #context = {'layout':layout,'geojson':JsonResponse(my_geojson_str, safe=False),'my_data': '','form': form}
    
    context = {'layout':layout,'form': form}
    return render(request, template_name,context)
        #return render(request, 'map.html', {'geojson': geojson,'my_variable':'Moshiur Rahman'})    

def save_geojson_to_folder(geojson_data, folder_path, file_name):
    # Convert the GeoJSON data to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Save the GeoDataFrame to a GeoJSON file in the folder
    gdf.to_file(os.path.join(folder_path, file_name), driver='GeoJSON')  

def get_geojson_data(request):
        # get the data you need, for example:
        shapefile = gpd.read_file('assets/geofiles/division/division.shp')
        shapefile = shapefile.loc[shapefile['GeoCode'] == '20']
        #console(shapefile.head())
        my_geojson_str = shapefile.to_crs(epsg=4326).to_json()     
        column_names = list(shapefile.columns)
        print(column_names)
        return JsonResponse(my_geojson_str,safe=False)