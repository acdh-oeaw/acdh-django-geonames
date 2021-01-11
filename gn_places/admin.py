# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   GeoNamesPlace,
)


@admin.register(GeoNamesPlace)
class GeoNamesPlaceAdmin(admin.ModelAdmin):
    pass



