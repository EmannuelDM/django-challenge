from django.contrib import admin

from core.models import Property, PricingRule, Booking


class PropertyAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    list_display = [
        'name',
        'base_price',
    ]
    list_filter = [
        'base_price',
    ]


admin.site.register(Property, PropertyAdmin)


class PricingRuleAdmin(admin.ModelAdmin):
    search_fields = [
        'property',
    ]
    list_display = [
        'property',
        'min_stay_length',
        'specific_day',
    ]
    list_filter = [
        'specific_day',
        'min_stay_length',
    ]


admin.site.register(PricingRule, PricingRuleAdmin)


class BookingAdmin(admin.ModelAdmin):
    search_fields = [
        'property',
    ]
    list_display = [
        'property',
        'date_start',
        'date_end',
        'final_price'
    ]
    list_filter = [
        'date_start',
        'final_price',
    ]


admin.site.register(Booking, BookingAdmin)
