from django.contrib import admin
from .models import Shapefile

# Register your models here.


@admin.register(Shapefile)
class ShapefileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
    # list_editable = ['name']
    # list_per_page = 50
    # list_filter = ['name']
