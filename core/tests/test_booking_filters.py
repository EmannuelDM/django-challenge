import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property, Booking
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_filter_booking_by_property_name():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    coventry_property = Property.objects.create(name="Hotel Coventry", base_price=2000)
    booking_palace = Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')
    Booking.objects.create(property=coventry_property, date_start='2022-12-20', date_end='2022-12-24')

    url = reverse('core:booking-list')
    client = APIClient()
    search_name = "alac"
    response = client.get(f"{url}?property_name={search_name}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['property'] == booking_palace.property.name


@pytest.mark.django_db
def test_filter_booking_by_property_name():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    coventry_property = Property.objects.create(name="Hotel Coventry", base_price=2000)
    booking_palace = Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')
    Booking.objects.create(property=coventry_property, date_start='2022-12-23', date_end='2022-12-24')

    url = reverse('core:booking-list')
    client = APIClient()
    search_start_date = "12-20-2022"
    response = client.get(f"{url}?date_start={search_start_date}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['property'] == booking_palace.property.name

