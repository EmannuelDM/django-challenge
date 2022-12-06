import json

import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property, Booking
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_read_booking():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')
    Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')

    url = reverse('core:booking-list')
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data
    assert data['count'] == 2


@pytest.mark.django_db
def test_create_booking():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    url = reverse('core:booking-list')
    client = APIClient()
    data = {'property': palace_property.id, 'date_start': '12-20-2022', 'date_end': '12-24-2022'}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['property'] == palace_property.name


@pytest.mark.django_db
def test_update_booking():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    booking_1 = Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')
    Booking.objects.create(property=palace_property, date_start='2022-12-22', date_end='2022-12-24')
    url = reverse('core:booking-detail', kwargs={'pk': booking_1.id})
    client = APIClient()
    data = {'date_start': '12-21-2022'}
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    booking_1.refresh_from_db()
    assert booking_1.date_start.strftime("%m-%d-%Y") == data['date_start']


@pytest.mark.django_db
def test_delete_booking():
    palace_property = Property.objects.create(name="Hotel Palace", base_price=3000)
    booking_1 = Booking.objects.create(property=palace_property, date_start='2022-12-20', date_end='2022-12-24')
    Booking.objects.create(property=palace_property, date_start='2022-12-22', date_end='2022-12-24')

    url = reverse('core:booking-detail', kwargs={'pk': booking_1.id})
    client = APIClient()
    response = client.delete(url, content_type="application/json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Booking.objects.filter(id=booking_1.id).exists() is False

