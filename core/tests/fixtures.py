import pytest

from core.models import Property, PricingRule


@pytest.fixture
def load_case_1():
    hotel_palace = Property.objects.create(name="Hotel Palace", base_price=10)
    PricingRule.objects.create(
        property=hotel_palace,
        price_modifier=-10,
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def load_case_2():
    hotel_palace = Property.objects.create(name="Hotel Palace", base_price=10)
    PricingRule.objects.create(
        property=hotel_palace,
        price_modifier=-10,
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )
    PricingRule.objects.create(
        property=hotel_palace,
        price_modifier=-20,
        min_stay_length=30,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def load_case_3():
    hotel_palace = Property.objects.create(name="Hotel Palace", base_price=10)
    PricingRule.objects.create(
        property=hotel_palace,
        price_modifier=-10,
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )
    PricingRule.objects.create(
        property=hotel_palace,
        price_modifier=None,
        min_stay_length=None,
        fixed_price=20,
        specific_day='2022-01-04'
    )