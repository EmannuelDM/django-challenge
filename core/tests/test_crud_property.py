import json

import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_read_property():
    Property.objects.create(name="Hotel Palace", base_price=3000)
    Property.objects.create(name="Hotel Coventry", base_price=4000)

    url = reverse('core:property-list')
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data
    assert data['count'] == 2


@pytest.mark.django_db
def test_create_property():

    url = reverse('core:property-list')
    client = APIClient()
    data = {'name': 'Hotel Palace',
            'base_price': 3000}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_update_property():
    property_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    Property.objects.create(name="Hotel Coventry", base_price=4000)

    url = reverse('core:property-detail', kwargs={'pk': property_1.id})
    client = APIClient()
    data = {'name': 'Hotel Kingston'}
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    property_1.refresh_from_db()
    assert property_1.name == data['name']


@pytest.mark.django_db
def test_delete_property():
    prop_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    Property.objects.create(name="Hotel Coventry", base_price=4000)

    url = reverse('core:property-detail', kwargs={'pk': prop_1.id})
    client = APIClient()
    response = client.delete(url, content_type="application/json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Property.objects.filter(id=prop_1.id).exists() is False
