from datetime import datetime

from django_filters import rest_framework as filters
from django.db.models import QuerySet

from core.models import Property, Booking


class PropertyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Property
        fields = []


class BookingFilter(filters.FilterSet):
    property_name = filters.CharFilter(field_name='property__name', lookup_expr='icontains')
    date_start = filters.CharFilter(method='filter_date_start')

    class Meta:
        model = Booking
        fields = []

    @staticmethod
    def filter_date_start(queryset: QuerySet, name: str, value: str) -> QuerySet:
        try:
            date_start = datetime.strptime(value, "%m-%d-%Y")
            return queryset.filter(date_start=date_start)
        except ValueError:
            return queryset


