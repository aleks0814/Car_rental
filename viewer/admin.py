from django.contrib import admin
from viewer.models import CarBrand, CarCategory, CarModel, Rental, Car, Booking, Client
from .models import Task


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'surname',
                'email'
            )
        }),
    )

    list_display = ('name', 'surname', 'email')
    ordering = ('-surname',)


class CarModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'car_brand',
                'car_category',
                'capacity',
                'picture',
            )
        }),
    )
    list_display = ('name', 'car_brand', 'car_category', 'capacity', 'combine_car_brand_and_name', 'picture')
    list_display_links = ('name', 'car_brand', 'car_category', 'combine_car_brand_and_name', 'picture')
    list_filter = ('car_brand', 'car_category')
    search_fields = ('name', 'car_brand__name')
    ordering = ('car_brand',)

    def combine_car_brand_and_name(self, obj):
        return f'{obj.car_brand} {obj.name}'


class CarAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'car_model',
                'rental',
                'transmission',
                'air_conditioning',
                'price_per_day',
                'avability'
            )
        }),
    )
    list_display = ('car_model', 'rental', 'transmission', 'air_conditioning', 'price_per_day', 'avability',)
    list_display_links = (
        'car_model', 'rental', 'transmission', 'air_conditioning', 'price_per_day', 'avability')
    list_filter = ('rental', 'avability', 'transmission', 'air_conditioning')
    search_fields = (
        'car_model__name', 'rental__name', 'car_model__name', 'car_model__car_brand__name',
        'car_model__car_category__name')
    ordering = ('-avability',)


class RentalAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'address',
                'number_of_cars',
            )
        }),
    )
    list_display = ('name', 'address', 'number_of_cars',)
    list_display_links = ('name', 'address', 'number_of_cars',)
    ordering = ('name',)


class BookingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'car',
                'approved',
                'date_of_rental',
                'date_of_return',
                'days_to_return',
                'number_of_days',
                'insurance',
                'total_cost',
            )
        }),
    )
    list_display = (
        'user', 'car', 'approved', 'date_of_rental', 'date_of_return', 'days_to_return', 'insurance', 'total_cost')
    list_display_links = ('user', 'car',)


admin.site.register(CarBrand)
admin.site.register(CarCategory)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Task)
