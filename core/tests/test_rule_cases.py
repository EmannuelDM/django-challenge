import json

import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property, Booking
from rest_framework.test import APIClient

from core.tests.fixtures import load_case_1, load_case_2, load_case_3


@pytest.mark.django_db
def test_case_1_create(load_case_1):
    palace_property = Property.objects.get(name="Hotel Palace")
    url = reverse('core:booking-list')
    client = APIClient()
    data = {'property': palace_property.id, 'date_start': '01-01-2022', 'date_end': '01-10-2022'}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['final_price'] == 90


@pytest.mark.django_db
def test_case_2_create(load_case_2):
    palace_property = Property.objects.get(name="Hotel Palace")
    url = reverse('core:booking-list')
    client = APIClient()
    data = {'property': palace_property.id, 'date_start': '01-01-2022', 'date_end': '01-10-2022'}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['final_price'] == 90


@pytest.mark.django_db
def test_case_3_create(load_case_3):
    palace_property = Property.objects.get(name="Hotel Palace")
    url = reverse('core:booking-list')
    client = APIClient()
    data = {'property': palace_property.id, 'date_start': '01-01-2022', 'date_end': '01-10-2022'}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['final_price'] == 101


@pytest.mark.django_db
def test_case_3_update(load_case_3):
    palace_property = Property.objects.get(name="Hotel Palace")
    booking = Booking.objects.create(
        property=palace_property,
        date_start='2022-01-08',
        date_end='2022-01-10',
        final_price=15)
    url = reverse('core:booking-detail', kwargs={'pk': booking.id})
    client = APIClient()
    data = {'property': palace_property.id, 'date_start': '01-01-2022', 'date_end': '01-10-2022'}
    response = client.put(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['final_price'] == 101
    booking.refresh_from_db()
    assert booking.final_price == 101
