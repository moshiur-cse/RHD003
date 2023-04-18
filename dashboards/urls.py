from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView
from . import views
app_name = 'dashboards'
urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),    
    #path('map/', DashboardsView.as_view(template_name = 'pages/maps/map.html'), name='map'),
    path('Web-map/',views.web_map, name='web_map'),
    path('map/', views.map, name='map'),
    path('get_geojson_data/', views.get_geojson_data, name='get_geojson_data'),
    
    
]