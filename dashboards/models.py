from django.db import models
import os
#import geopandas as gpd
# Create your models here.


def get_upload_path(instance, filename):
    """Function to generate a new filename for uploaded files"""
    name, ext = os.path.splitext(filename)
    
    # shapefile = gpd.read_file(os.path.join("uploads", str(instance.id), filename))
    # my_geojson_str = shapefile.to_crs(epsg=4326).to_json()
    
    # print(my_geojson_str)
    
    # folder_path = 'assets/geofiles/'+instance.name
    # file_name = instance.name+'.json'
    
    # filepath = os.path.join(folder_path, file_name)
    # with open(filepath, 'w') as f:
    #     f.write(my_geojson_str)

    
    base_path = os.path.join('assests', 'geofiles', instance.name)
    # # path="static/documents/JRC/Public/document.pdf"
    new_name = f'geo_{instance.name}{ext}'
    return os.path.join(base_path, new_name)


class Shapefile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path, max_length=500, null=True, blank=True)
