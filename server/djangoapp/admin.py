from django.contrib import admin
from .models import CarModel, CarMake



class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')
    list_filter = ('car_make', 'car_type')
    search_fields = ('name', 'car_make__name', 'year')

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Register models with their respective admin classes
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)