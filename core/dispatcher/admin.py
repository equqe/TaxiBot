from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from . import models


# Register your models here.


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Location, OSMGeoAdmin)
admin.site.register(models.City)
admin.site.register(models.Address)
admin.site.register(models.CostPerKm)
admin.site.register(models.CostPerBabyChair)
admin.site.register(models.Settings)
admin.site.register(models.OrderReview)
admin.site.register(models.OrderRevision)
