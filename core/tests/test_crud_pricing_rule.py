import json

import pytest
from django.urls.base import reverse
from rest_framework import status
from core.models import Property, PricingRule
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_read_pricing_rule():
    prop_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    prop_2 = Property.objects.create(name="Hotel Coventry", base_price=4000)
    PricingRule.objects.create(
        property=prop_1,
        price_modifier=-20,
        min_stay_length=2,
        fixed_price=None,
        specific_day=None
    )
    PricingRule.objects.create(
        property=prop_2,
        price_modifier=-10,
        min_stay_length=1,
        fixed_price=None,
        specific_day=None
    )

    url = reverse('core:pricing-rule-list')
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data
    assert data['count'] == 2


@pytest.mark.django_db
def test_create_pricing_rule():
    prop_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    url = reverse('core:pricing-rule-list')
    client = APIClient()
    data = {'property': prop_1.id,
            'price_modifier': -20,
            'min_stay_length': 2,
            'fixed_price': None,
            'specific_day': None}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['property'] == prop_1.name


@pytest.mark.django_db
def test_update_pricing_rule():
    prop_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    prop_2 = Property.objects.create(name="Hotel Coventry", base_price=4000)
    pricing_1 = PricingRule.objects.create(
        property=prop_1,
        price_modifier=-20,
        min_stay_length=2,
        fixed_price=None,
        specific_day=None
    )
    pricing_2 = PricingRule.objects.create(
        property=prop_2,
        price_modifier=-10,
        min_stay_length=1,
        fixed_price=None,
        specific_day=None
    )

    url = reverse('core:pricing-rule-detail', kwargs={'pk': pricing_1.id})
    client = APIClient()
    data = {'property': prop_2.id}
    response = client.patch(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    pricing_1.refresh_from_db()
    assert pricing_1.property.id == prop_2.id


@pytest.mark.django_db
def test_delete_pricing_rule():
    prop_1 = Property.objects.create(name="Hotel Palace", base_price=3000)
    prop_2 = Property.objects.create(name="Hotel Coventry", base_price=4000)
    pricing_1 = PricingRule.objects.create(
        property=prop_1,
        price_modifier=-20,
        min_stay_length=2,
        fixed_price=None,
        specific_day=None
    )
    pricing_2 = PricingRule.objects.create(
        property=prop_2,
        price_modifier=-10,
        min_stay_length=1,
        fixed_price=None,
        specific_day=None
    )

    url = reverse('core:pricing-rule-detail', kwargs={'pk': pricing_1.id})
    client = APIClient()
    response = client.delete(url, content_type="application/json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PricingRule.objects.filter(id=pricing_1.id).exists() is False
