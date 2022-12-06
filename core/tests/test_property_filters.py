import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_filter_property_by_name():
    palace_hotel = Property.objects.create(name="Hotel Palace", base_price=3000)
    Property.objects.create(name="Hotel Coventry", base_price=4000)

    url = reverse('core:property-list')
    client = APIClient()
    search_name = "alace"
    response = client.get(f"{url}?name={search_name}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['name'] == palace_hotel.name
